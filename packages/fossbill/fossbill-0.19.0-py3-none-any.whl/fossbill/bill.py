from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required, user_pref_smtp_enough
from fossbill.database import get_db, paginatestmt, pagination, filterstmt
from fossbill.client import get_client, get_clients
from fossbill.product import get_product, get_products
from fossbill.me import get_user_smtp_server
from fossbill.payment import user_subscription_valid
from sqlalchemy import insert, select, join, func, literal_column, desc, case
from sqlalchemy.exc import SQLAlchemyError
import datetime
from flask_weasyprint import render_pdf, HTML
from email.message import EmailMessage
import smtplib

bp = Blueprint('bill', __name__, url_prefix='/bills')

def bills_view():
    engine, metadata = get_db()

    bills = metadata.tables['bill']
    bill_rows = metadata.tables['bill_row']

    jstmt = join(
        bills,
        bill_rows,
        bills.c.id == bill_rows.c.bill_id,
        isouter=True
    )
    return select(
        bills,
        func.coalesce(
            func.sum(bill_rows.c.price * bill_rows.c.quantity),
            0
        ).label('gross_amount'),
        func.coalesce(
            func.sum(bill_rows.c.price * bill_rows.c.quantity * (bill_rows.c.tax_rate / 100)),
            0
        ).label('tax_amount'),
        func.coalesce(
            func.sum(bill_rows.c.price * bill_rows.c.quantity * (1 + (bill_rows.c.tax_rate / 100))),
            0
        ).label('amount'),
    ).select_from(jstmt).group_by(bills.c.id)

def tostatstmt(stmt):
    alias = stmt.alias()
    return select(
        func.sum(literal_column('id')).label('count'),
        func.sum(literal_column('gross_amount')).label('gross_amount'),
        func.sum(literal_column('tax_amount')).label('tax_amount'),
        func.sum(literal_column('amount')).label('amount'),
    ).select_from(alias)

def bill_rows_view():
    engine, metadata = get_db()

    bill_rows = metadata.tables['bill_row']

    return select(
        bill_rows,
        (bill_rows.c.price * bill_rows.c.quantity).label('gross_amount'),
        (bill_rows.c.price * bill_rows.c.quantity * (bill_rows.c.tax_rate / 100)).label('tax_amount'),
        (bill_rows.c.price * bill_rows.c.quantity * (1 + (bill_rows.c.tax_rate / 100))).label('amount'),
    )

@bp.route('/')
@login_required
def index():
    engine, metadata = get_db()
    bills = metadata.tables['bill']
    stmt = bills_view().where(bills.c.user_id == g.user.id).order_by(desc(bills.c.date))

    stmt, filtered = filterstmt(stmt, request)
    statstmt = tostatstmt(stmt)
    stmt, countstmt = paginatestmt(stmt, request)

    defaultstats = {
        'count': 0,
        'gross_amount': 0,
        'tax_amount': 0,
        'amount': 0,
    }

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            count = conn.execute(countstmt)
            stats = conn.execute(statstmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
        bills = []
        count = 0
        stats = defaultstats
    else:
        bills = result.fetchall()
        count = count.fetchone().count
        stats = stats.fetchone()
        # ugly hack
        if not stats.count:
            stats = defaultstats

    return render_template(
        'bill/index.html',
        bills=bills,
        pagination=pagination(count, request),
        filtered=filtered,
        stats=stats,
    )

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@user_subscription_valid
def create():
    if request.method == 'POST':
        error = None

        if request.form.get('client_id'):
            try:
                int(request.form['client_id'])
            except ValueError as ve:
                error = _('Client id should be an integer.')

        if error is not None:
            flash(error)
        else:
            client_id = None
            recipient = ""

            if request.form.get('client_id'):
                client = get_client(request.form['client_id'], g.user.id)
                client_id = client.id
                recipient = client.address

            engine, metadata = get_db()

            stmt = insert(metadata.tables['bill']).values(
                client_id=client_id,
                date=datetime.date.today(),
                recipient=recipient,
                source=g.user_pref.source,
                bill_mentions=g.user_pref.bill_mentions,
                quote_mentions=g.user_pref.quote_mentions,
                user_id=g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                flash(_("Something went wrong."))
            else:
                flash(_("Bill created."))
                return redirect(url_for("bill.update", id=result.inserted_primary_key[0]))

    return render_template('bill/create.html', clients=get_clients(g.user.id))

def get_new_bill_number(user_id):
    engine, metadata = get_db()
    bills = metadata.tables['bill']
    stmt = select(func.max(bills.c.bill_number)).where(
        bills.c.user_id == user_id,
        bills.c.bill_number != None,
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt).scalar()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")

    if result == None:
        result = 0

    return result+1

def get_new_quote_number(user_id):
    engine, metadata = get_db()
    bills = metadata.tables['bill']
    stmt = select(func.max(bills.c.quote_number)).where(
        bills.c.user_id == user_id,
        bills.c.quote_number != None,
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt).scalar()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")

    if result == None:
        result = 0

    return result+1

def get_bill(id, user_id):
    engine, metadata = get_db()
    bills = metadata.tables['bill']
    stmt = bills_view().where(
        bills.c.id == id,
        bills.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        bill = result.fetchone()

    if bill is None:
        abort(404, f"Bill {id} doesn't exist.")

    return bill

def get_bill_row(id, user_id):
    engine, metadata = get_db()
    bill_rows = metadata.tables['bill_row']
    stmt = select(bill_rows).where(
        bill_rows.c.id == id,
        bill_rows.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        bill_row = result.fetchone()

    if bill_row is None:
        abort(404, f"Bill {id} doesn't exist.")

    return bill_row

def get_bill_rows(bill_id, user_id):
    engine, metadata = get_db()
    bill_rows = metadata.tables['bill_row']
    stmt = bill_rows_view().where(
        bill_rows.c.bill_id == bill_id,
        bill_rows.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        bill_rows = result.fetchall()

    return bill_rows

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    bill = get_bill(id, g.user.id)

    if request.method == 'POST':
        error = None

        form = dict(request.form)

        if None == bill.quote_number and None == bill.bill_number:
            if form.get('client_id'):
                try:
                    int(form['client_id'])
                except ValueError as ve:
                    error = _('Client id should be an integer.')
                else:
                    get_client(form['client_id'], g.user.id) # to check
            else:
                form['client_id'] = None

            if None == form.get('date'):
                error = _('Date is required.')
            else:
                form['date'] = datetime.datetime.strptime(form['date'], "%Y-%m-%d")

            if None == form.get('recipient'):
                error = _('Recipient is required.')

            if None == form.get('source'):
                error = _('Source is required.')
        else:
            form['client_id'] = None
            form['date'] = None
            form['recipient'] = None
            form['source'] = None

        if None == bill.quote_number:
            if None == form.get('quote_mentions'):
                error = _('Quote mentions are required.')
        else:
            form['quote_mentions'] = None

        if None == bill.bill_number:
            if None == form.get('bill_mentions'):
                error = _('Bill mentions are required.')
        else:
            form['bill_mentions'] = None

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            bills = metadata.tables['bill']

            to_update_values = {
                'client_id': form.get('client_id'),
                'date': form.get('date'),
                'recipient': form.get('recipient'),
                'source': form.get('source'),
                'quote_mentions': form.get('quote_mentions'),
                'bill_mentions': form.get('bill_mentions'),
                'comment': form.get('comment'),
            }
            to_update_values = {k: v for k, v in to_update_values.items() if v is not None}

            stmt = bills.update().values(**to_update_values).where(
                bills.c.id == id,
                bills.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                flash(_("Something went wrong."))
            else:
                flash(_("Bill updated."))
                return redirect(url_for("bill.update", id=id))

    if None == bill.quote_number and None == bill.bill_number:
        return render_template(
            'bill/update.html',
            bill=bill,
            bill_rows=get_bill_rows(bill.id, g.user.id),
            clients=get_clients(g.user.id),
        )
    elif None == bill.bill_number:
        return render_template(
            'bill/update_quote.html',
            bill=bill,
            bill_rows=get_bill_rows(bill.id, g.user.id),
            clients=get_clients(g.user.id),
            products=get_products(g.user.id),
        )
    else:
        return render_template(
            'bill/update_bill.html',
            bill=bill,
            bill_rows=get_bill_rows(bill.id, g.user.id),
            clients=get_clients(g.user.id),
            products=get_products(g.user.id),
        )

@bp.route('/<int:id>/mark_paid', methods=['POST'])
@login_required
def mark_paid(id):
    bill = get_bill(id, g.user.id)
    if None == bill.bill_number:
        flash(_("This bill is not finished."))
        return redirect(url_for('bill.update', id=id))
    if bill.paid:
        flash(_("This bill already is paid."))
        return redirect(url_for('bill.update', id=id))

    engine, metadata = get_db()
    bills = metadata.tables['bill']

    try:
        with engine.connect() as conn:
            stmt = bills.update().values(
                paid=True,
            ).where(
                bills.c.id == id,
                bills.c.user_id == g.user.id,
            )
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
    else:
        flash(_("Bill marked as paid."))
        return redirect(url_for('bill.update', id=id))

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    bill = get_bill(id, g.user.id)
    if not None == bill.quote_number:
        flash(_("This bill is not a draft."))
        return redirect(url_for('bill.update', id=id))

    engine, metadata = get_db()
    bills = metadata.tables['bill']
    bill_rows = metadata.tables['bill_row']

    try:
        with engine.connect() as conn:
            stmt = bill_rows.delete().where(
                bill_rows.c.bill_id == id,
                bill_rows.c.user_id == g.user.id,
            )
            result = conn.execute(stmt)

            stmt = bills.delete().where(
                bills.c.id == id,
                bills.c.user_id == g.user.id,
            )
            result = conn.execute(stmt)

            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
    else:
        flash(_("Bill deleted."))
        return redirect(url_for('bill.index'))

@bp.route('/<int:id>/rows/create', methods=['GET', 'POST'])
@login_required
def create_row(id):
    bill = get_bill(id, g.user.id)

    if request.method == 'POST':
        error = None

        if not None == bill.quote_number:
            flash(_("This bill is not a draft."))
            return redirect(url_for('bill.update', id=id))

        if request.form.get('product_id'):
            try:
                int(request.form['product_id'])
            except ValueError as ve:
                error = _('Product id should be an integer.')

            if error is None:
                product = get_product(request.form['product_id'], g.user.id)
                label = product.label
                price = product.price
                tax_rate = product.tax_rate
        elif request.form.get('label') or request.form.get('price'):
            label = request.form['label']
            if not label:
                error = _('Label is required.')

            if not request.form['price']:
                error = _('Price is required.')

            if not request.form['tax_rate']:
                error = _('Tax rate is required.')

            if error is None:
                try:
                    price = float(request.form['price'])*100
                except ValueError as ve:
                    error = _('Price should be a float.')

                try:
                    tax_rate = float(request.form['tax_rate'])
                except ValueError as ve:
                    error = _('Tax rate should be a float.')

            if error is None:
                if tax_rate < 0:
                    error = _('Tax rate should be higher than 0.')
                elif tax_rate > 100:
                    error = _('Tax rate should be lower than 100.')
        else:
            error = _('Either give a product id or all.')

        if not request.form['quantity']:
            error = _('Quantity is required.')

        if error is None:
            try:
                quantity = int(request.form['quantity'])
            except ValueError as ve:
                error = _('Quantity should be an integer.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            stmt = insert(metadata.tables['bill_row']).values(
                user_id=g.user.id,
                bill_id=id,
                label=label,
                price=price,
                quantity=quantity,
                tax_rate=tax_rate,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                flash(_("Something went wrong."))
            else:
                flash(_("Bill row created."))
                return redirect(url_for(
                    'bill.update',
                    id=id,
                    _anchor="bill_row_"+str(result.inserted_primary_key[0]))
                )

        return redirect(url_for(
            'bill.update',
            id=id,
        ))

    return render_template(
        'bill/create_row.html',
        bill=bill,
        products=get_products(g.user.id),
    )

@bp.route('/<int:bill_id>/rows/<int:id>/update', methods=['get', 'POST'])
@login_required
def update_row(bill_id, id):
    bill = get_bill(bill_id, g.user.id)
    bill_row = get_bill_row(id, g.user.id)

    if request.method == 'POST':
        if not None == bill.quote_number:
            flash(_("This bill is not a draft."))
            return redirect(url_for('bill.update', id=bill_row.bill_id))

        error = None

        if not request.form['label']:
            error = _('Label is required.')

        if not request.form['price']:
            error = _('Price is required.')

        if not request.form['quantity']:
            error = _('Quantity is required.')

        if not request.form['tax_rate']:
            error = _('Tax rate is required.')

        if error is None:
            try:
                float(request.form['price'])*100
            except ValueError as ve:
                error = _('Price should be a float.')

            try:
                int(request.form['quantity'])
            except ValueError as ve:
                error = _('Quantity should be an integer.')

            try:
                tax_rate = float(request.form['tax_rate'])
            except ValueError as ve:
                error = _('Tax rate should be a float.')

        if error is None:
            if tax_rate < 0:
                error = _('Tax rate should be higher than 0.')
            elif tax_rate > 100:
                error = _('Tax rate should be lower than 100.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            bill_rows = metadata.tables['bill_row']
            stmt = bill_rows.update().values(
                label=request.form['label'],
                price=float(request.form['price'])*100,
                quantity=request.form['quantity'],
                tax_rate=request.form['tax_rate'],
            ).where(
                bill_rows.c.id == id,
                bill_rows.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                flash(_("Something went wrong."))
            else:
                flash(_("Bill row updated."))
                return redirect(url_for(
                    'bill.update',
                    id=bill.id,
                    _anchor="bill_row_"+str(id))
                )

        return redirect(url_for('bill.update', id=bill.id))

    return render_template(
        'bill/update_row.html',
        bill=bill,
        bill_row=bill_row,
    )


@bp.route('/<int:id>/delete_row', methods=['POST'])
@login_required
def delete_row(id):
    bill_row = get_bill_row(id, g.user.id)
    bill = get_bill(bill_row.bill_id, g.user.id)

    if not None == bill.quote_number:
        flash(_("This bill is not a draft."))
        return redirect(url_for('bill.update', id=bill_row.bill_id))

    engine, metadata = get_db()
    bill_rows = metadata.tables['bill_row']

    stmt = bill_rows.delete().where(
        bill_rows.c.id == id,
        bill_rows.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    flash(_("Bill row deleted."))
    return redirect(url_for(
        'bill.update',
        id=bill_row.bill_id,
        _anchor="bill_rows"
    ))

@bp.route('/<int:id>/create_quote', methods=['POST'])
@login_required
def create_quote(id):
    bill = get_bill(id, g.user.id)

    if bill.quote_number or bill.bill_number:
        flash(_("This bill is not a draft."))
        return redirect(url_for('bill.update', id=id))

    bill_rows = get_bill_rows(id, g.user.id)

    engine, metadata = get_db()
    bills = metadata.tables['bill']

    stmt = bills.update().values(
        quote_number=get_new_quote_number(g.user.id),
    ).where(
        bills.c.id == id,
        bills.c.user_id == g.user.id,
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    flash(_("Quote finished."))
    return redirect(url_for('bill.update', id=id))

@bp.route('/<int:id>/create_bill', methods=['POST'])
@login_required
def create_bill(id):
    bill = get_bill(id, g.user.id)

    if not None == bill.bill_number:
        flash(_("This bill already is finished."))
        return redirect(url_for('bill.update', id=id))

    engine, metadata = get_db()
    bills = metadata.tables['bill']

    stmt = bills.update().values(
        bill_number=get_new_bill_number(g.user.id),
    ).where(
        bills.c.id == id,
        bills.c.user_id == g.user.id,
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
    else:
        flash(_("Bill finished."))

    return redirect(url_for('bill.update', id=id))

@bp.route('/<int:id>/view_draft', methods=['GET'])
@login_required
def view_draft(id):
    bill = get_bill(id, g.user.id)

    return render_template(
        'bill/generated_draft.html',
        bill=bill,
        bill_rows=get_bill_rows(bill.id, g.user.id),
    )

@bp.route('/<int:id>/view_quote', methods=['GET'])
@login_required
def view_quote(id):
    bill = get_bill(id, g.user.id)

    return render_template(
        'bill/generated_quote.html',
        bill=bill,
        bill_rows=get_bill_rows(bill.id, g.user.id),
    )

@bp.route('/<int:id>/view_bill', methods=['GET'])
@login_required
def view_bill(id):
    bill = get_bill(id, g.user.id)

    return render_template(
        'bill/generated_bill.html',
        bill=bill,
        bill_rows=get_bill_rows(bill.id, g.user.id),
    )

@bp.route('/<int:id>/view_draft.pdf', methods=['GET'])
@login_required
def view_draft_pdf(id):
    return render_pdf(
        url_for('bill.view_draft', id=id),
        download_filename="fossbill_draft_{}.pdf".format(id)
    )

@bp.route('/<int:id>/view_quote.pdf', methods=['GET'])
@login_required
def view_quote_pdf(id):
    return render_pdf(
        url_for('bill.view_quote', id=id),
        download_filename="fossbill_quote_{}.pdf".format(id)
    )

@bp.route('/<int:id>/view_bill.pdf', methods=['GET'])
@login_required
def view_bill_pdf(id):
    return render_pdf(
        url_for('bill.view_bill', id=id),
        download_filename="fossbill_quote_{}.pdf".format(id)
    )

@bp.route('/<int:id>/send_quote_email', methods=['GET', 'POST'])
@login_required
@user_pref_smtp_enough
def send_quote_email(id):
    bill = get_bill(id, g.user.id)

    if None == bill.quote_number:
        flash(_("This quote is not generated."))
        return redirect(url_for('bill.update', id=id))

    client = None
    if bill.client_id:
        client = get_client(bill.client_id, g.user.id)

    if request.method == 'POST':
        error = None
        if not request.form['email']:
            error = _('Email is required.')

        if not request.form['subject']:
            error = _('Subject is required.')

        if not request.form['body']:
            error = _('Body is required.')

        if error is None:
            pdf = render_template(
                'bill/generated_quote.html',
                bill=bill,
                bill_rows=get_bill_rows(bill.id, g.user.id),
            )

            msg = EmailMessage()
            msg["From"] = g.user_pref.smtp_username
            msg["To"] = request.form['email']
            msg["Subject"] = request.form['subject']

            if g.user_pref.smtp_reply_to:
                msg["Reply-To"] = g.user_pref.smtp_reply_to
            if g.user_pref.smtp_cc:
                msg["Cc"] = g.user_pref.smtp_cc

            msg.set_content(request.form['body'])
            msg.add_attachment(
                HTML(string=pdf).write_pdf(),
                filename="invoice_{}.pdf".format(id),
                maintype='application',
                subtype='pdf'
            )

            try:
                server = get_user_smtp_server(g.user_pref)
                server.send_message(msg)
                server.quit()
            except smtplib.SMTPException as e:
                current_app.logger.error(str(e))
                error = _("We failed to send the mail: " + str(e))
            else:
                flash(_("Email sent."))
                return redirect(url_for("bill.update", id=id))

        flash(error)

    default_body = render_template(
        'bill/quote_email.plain',
        bill=bill,
    )

    default_subject = "{} #{}".format(_("Quote"), bill.quote_number)

    return render_template(
        'bill/send_quote_email.html',
        bill=bill,
        client=client,
        default_body=default_body,
        default_subject=default_subject,
    )

@bp.route('/<int:id>/send_bill_email', methods=['GET', 'POST'])
@login_required
@user_pref_smtp_enough
def send_bill_email(id):
    bill = get_bill(id, g.user.id)

    if None == bill.bill_number:
        flash(_("This bill is not generated."))
        return redirect(url_for('bill.update', id=id))

    client = None
    if bill.client_id:
        client = get_client(bill.client_id, g.user.id)

    if request.method == 'POST':
        error = None
        if not request.form['email']:
            error = _('Email is required.')

        if not request.form['subject']:
            error = _('Subject is required.')

        if not request.form['body']:
            error = _('Body is required.')

        if error is None:
            pdf = render_template(
                'bill/generated_bill.html',
                bill=bill,
                bill_rows=get_bill_rows(bill.id, g.user.id),
            )

            msg = EmailMessage()
            msg["From"] = g.user_pref.smtp_username
            msg["To"] = request.form['email']
            msg["Subject"] = request.form['subject']

            if g.user_pref.smtp_reply_to:
                msg["Reply-To"] = g.user_pref.smtp_reply_to
            if g.user_pref.smtp_cc:
                msg["Cc"] = g.user_pref.smtp_cc

            msg.set_content(request.form['body'])
            msg.add_attachment(
                HTML(string=pdf).write_pdf(),
                filename="invoice_{}.pdf".format(id),
                maintype='application',
                subtype='pdf'
            )

            try:
                server = get_user_smtp_server(g.user_pref)
                server.send_message(msg)
                server.quit()
            except smtplib.SMTPException as e:
                current_app.logger.error(str(e))
                error = _("We failed to send the mail: " + str(e))
            else:
                flash(_("Email sent."))
                return redirect(url_for("bill.update", id=id))

        flash(error)

    default_body = render_template(
        'bill/bill_email.plain',
        bill=bill,
    )

    default_subject = "{} #{}".format(_("Bill"), bill.bill_number)

    return render_template(
        'bill/send_bill_email.html',
        bill=bill,
        client=client,
        default_body=default_body,
        default_subject=default_subject,
    )


@bp.route('/<int:id>/finish_draft', methods=['GET'])
@login_required
def finish_draft(id):
    bill = get_bill(id, g.user.id)
    return render_template(
        'bill/finish_draft.html',
        bill=bill,
    )
