from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for,
    session, send_file
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required, user_pref_smtp_enough
from fossbill.database import get_db
from fossbill.auth import setup_locale
from fossbill.auth import load_logged_in_user
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import smtplib
from email.message import EmailMessage
import tarfile
import io
import csv

bp = Blueprint('me', __name__, url_prefix='/me')

def get_user_smtp_server(user_pref):
    if user_pref.smtp_security == "TLS":
        server = smtplib.SMTP_SSL(
            host=user_pref.smtp_host,
            port=user_pref.smtp_port,
            timeout=10
        )
    else:
        server = smtplib.SMTP(
            host=user_pref.smtp_host,
            port=user_pref.smtp_port,
            timeout=10
        )
        if user_pref.smtp_security == "STARTTLS":
            server.starttls()

    server.login(user_pref.smtp_username, user_pref.smtp_password)

    return server

@bp.route('/test_email', methods=['POST'])
@login_required
@user_pref_smtp_enough
def test_email():
    body = render_template('me/test_email.plain')

    msg = EmailMessage()
    msg["From"] = g.user_pref.smtp_username
    msg["To"] = g.user_pref.email
    msg["Subject"] = _("Test email from Fossbill")
    msg.set_content(body)

    if g.user_pref.smtp_reply_to:
        msg["Reply-To"] = g.user_pref.smtp_reply_to
    if g.user_pref.smtp_cc:
        msg["Cc"] = g.user_pref.smtp_cc

    try:
        server = get_user_smtp_server(g.user_pref)
        server.send_message(msg)
        server.quit()
    except smtplib.SMTPException as e:
        flash(_("We failed to send the mail: " + str(e)))
        return redirect(url_for("me.update"))

    flash(_("We sent an email to you."))
    return redirect(url_for("me.update"))

@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():
    if request.method == 'POST':
        error = None

        smtp_host = request.form.get('smtp_host', None)
        if not smtp_host:
            smtp_host = None

        smtp_username = request.form.get('smtp_username', None)
        if not smtp_username:
            smtp_username = None

        smtp_password = request.form.get('smtp_password', None)
        if not smtp_password:
            smtp_password = None

        smtp_port = request.form.get('smtp_port', None)
        if not smtp_port:
            smtp_port = None
        else:
            try:
                int(smtp_port)
            except ValueError as ve:
                error = _('SMTP Port should be an integer.')

        smtp_security = request.form.get('smtp_security', None)
        if not smtp_security:
            smtp_security = None
        else:
            available_protocols = ['TLS', 'STARTTLS']
            if not smtp_security in available_protocols:
                error = _('SMTP Security should be one of {available_protocols}.').format(
                    available_protocols=', '.join(available_protocols)
                )

        smtp_reply_to = request.form.get('smtp_reply_to', None)
        if not smtp_reply_to:
            smtp_reply_to = None

        smtp_cc = request.form.get('smtp_cc', None)
        if not smtp_cc:
            smtp_cc = None

        quote_mentions = request.form.get('quote_mentions', None)
        if not quote_mentions:
            quote_mentions = None

        bill_mentions = request.form.get('bill_mentions', None)
        if not bill_mentions:
            bill_mentions = None

        available_locales = ['en_US', 'fr_FR']
        if not request.form.get('locale') in available_locales:
            error = _('Locale should be one of {available_locales}.').format(
                available_locales = ', '.join(available_locales)
            )

        email = request.form.get('email', None)
        if not email:
            email = None

        currency = request.form.get('currency', None)
        if not currency:
            currency = None

        source = request.form.get('source', None)
        if not source:
            source = None

        if error is None:
            engine, metadata = get_db()
            user_prefs = metadata.tables['user_pref']

            stmt = user_prefs.update().values(
                bill_mentions=bill_mentions,
                currency=currency,
                email=email,
                locale=request.form['locale'],
                quote_mentions=quote_mentions,
                smtp_host=smtp_host,
                smtp_password=smtp_password,
                smtp_port=smtp_port,
                smtp_security=smtp_security,
                smtp_username=smtp_username,
                smtp_reply_to=smtp_reply_to,
                smtp_cc=smtp_cc,
                source=source,
            ).where(
                user_prefs.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except IntegrityError as e:
                error = f"Email {email} is already used."
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                load_logged_in_user() # refresh stripe_customer
                setup_locale() # refresh locale
                flash(_("User updated."))
                return redirect(url_for("me.update"))

        flash(error)

    return render_template('me/update.html')


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    engine, metadata = get_db()

    try:
        with engine.connect() as conn:
            for table_name in ['user_pref', 'bill_row', 'bill', 'client', 'product', 'payment']:
                table = metadata.tables[table_name]
                stmt = table.delete().where(
                    table.c.user_id == g.user.id,
                )
                result = conn.execute(stmt)

            stmt = metadata.tables['user'].delete().where(
                metadata.tables['user'].c.id == g.user.id,
            )
            result = conn.execute(stmt)

            conn.commit()

            session.clear()

            return redirect(url_for("landing.home"))
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    return redirect(url_for("me.update"))

@bp.route('/delete_bills', methods=['POST'])
@login_required
def delete_bills():
    engine, metadata = get_db()

    try:
        with engine.connect() as conn:
            for table_name in ['bill_row', 'bill']:
                table = metadata.tables[table_name]
                stmt = table.delete().where(
                    table.c.user_id == g.user.id,
                )
                result = conn.execute(stmt)

            conn.commit()
            flash(_("All bills has been deleted."))
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))

    return redirect(url_for("me.update"))

@bp.route('/import_export_user')
@login_required
def import_export_user():
    return render_template('me/import_export_user.html')

@bp.route('/import_user', methods=['POST'])
@login_required
def import_user():
    error = None
    if 'file' not in request.files or request.files['file'].filename == '':
        error = _('File is required.')

    if error is None:
        file = tarfile.open(fileobj=request.files['file'].stream)

        try:
            import_user_tar_file(file)
        except KeyError as e:
            error = _("The file format seems incorrect.")
        except SQLAlchemyError as e:
            current_app.logger.error(str(e))
            error = _("Something went wrong.")
        else:
            flash(_("User data imported."))
            return redirect(url_for("landing.home"))

    flash(error)
    return redirect(url_for("me.import_export_user"))

def import_user_tar_file(file):
    engine, metadata = get_db()
    with engine.connect() as conn:
        for table_name in ['bill_row', 'bill', 'client', 'product']:
            table = metadata.tables[table_name]
            stmt = table.delete().where(
                table.c.user_id == g.user.id,
            )
            conn.execute(stmt)

        clientfile = io.TextIOWrapper(file.extractfile('client.csv'))
        clientreader = csv.reader(clientfile)
        clientids = {}
        for row in clientreader:
            stmt = insert(metadata.tables['client']).values(
                address=row[1],
                email=row[2],
                label=row[3],
                user_id=g.user.id,
            )
            result = conn.execute(stmt)
            clientids[row[0]] = result.inserted_primary_key[0]

        productfile = io.TextIOWrapper(file.extractfile('product.csv'))
        productreader = csv.reader(productfile)
        for row in productreader:
            stmt = insert(metadata.tables['product']).values(
                label=row[0],
                price=row[1],
                tax_rate=row[2],
                user_id=g.user.id,
            )
            conn.execute(stmt)

        billfile = io.TextIOWrapper(file.extractfile('bill.csv'))
        billreader = csv.reader(billfile)
        billids = {}
        for row in billreader:
            stmt = insert(metadata.tables['bill']).values(
                client_id=clientids[row[1]] or None,
                comment=row[2],
                date=row[3],
                bill_number=row[4] or None,
                quote_number=row[5] or None,
                recipient=row[6],
                source=row[7],
                bill_mentions=row[7],
                quote_mentions=row[9],
                paid=row[10] == 'False',
                user_id=g.user.id,
            )
            result = conn.execute(stmt)
            billids[row[0]] = result.inserted_primary_key[0]

        billrowfile = io.TextIOWrapper(file.extractfile('bill_row.csv'))
        billrowreader = csv.reader(billrowfile)
        for row in billrowreader:
            stmt = insert(metadata.tables['bill_row']).values(
                bill_id=billids[row[0]],
                label=row[1],
                price=row[2],
                quantity=row[3],
                tax_rate=row[4],
                user_id=g.user.id,
            )
            conn.execute(stmt)

        conn.commit()

@bp.route('/export_user')
@login_required
def export_user():
    tarfilebuf = io.BytesIO()
    file = tarfile.open(fileobj=tarfilebuf, mode='w:bz2')

    add_tarfile_from_table(file, 'client', ['id', 'address', 'email', 'label'])
    add_tarfile_from_table(file, 'product', ['label', 'price', 'tax_rate'])
    add_tarfile_from_table(file, 'bill', [
        'id',
        'client_id',
        'comment',
        'date',
        'bill_number',
        'quote_number',
        'recipient',
        'source',
        'bill_mentions',
        'quote_mentions',
        'paid'
    ])
    add_tarfile_from_table(file, 'bill_row', [
        'bill_id',
        'label',
        'price',
        'quantity',
        'tax_rate',
    ])

    file.close()

    tarfilebuf.seek(0)

    return send_file(tarfilebuf, download_name="fossbill_export.tar.bz2")

def add_tarfile_from_table(file, table, columns):
    engine, metadata = get_db()
    with engine.connect() as conn:
        filebuf = io.BytesIO()
        textbuf = io.TextIOWrapper(filebuf)
        writer = csv.writer(textbuf)
        stmt = select(metadata.tables[table]).where(
            metadata.tables[table].c.user_id == g.user.id,
        )
        result = conn.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            writer.writerow([getattr(row, column) for column in columns])
        textbuf.flush()
        filebuf.seek(0)
        info = tarfile.TarInfo('{}.csv'.format(table))
        info.size=filebuf.getbuffer().nbytes
        file.addfile(tarinfo=info, fileobj=filebuf)
