from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required
from fossbill.database import get_db, paginatestmt, pagination, filterstmt
from sqlalchemy import insert, select, desc
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('customer', __name__, url_prefix='/customers')

@bp.route('/')
@login_required
def index():
    engine, metadata = get_db()
    customers = metadata.tables['customer']
    stmt = select(customers).where(
        customers.c.user_id == g.user.id,
    ).order_by(desc(customers.c.id))
    stmt, filtered = filterstmt(stmt, request)
    stmt, countstmt = paginatestmt(stmt, request)
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            count = conn.execute(countstmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = f"Something went wrong."
        customers = []
        count = 0
    else:
        customers = result.fetchall()
        count = count.fetchone().count

    return render_template(
        'customer/index.html',
        customers=customers,
        pagination=pagination(count, request),
        filtered=filtered,
    )

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None

        if not request.form['label']:
            error = _('Label is required.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()

            stmt = insert(metadata.tables['customer']).values(
                address=request.form['address'],
                email=request.form['email'],
                label=request.form['label'],
                user_id=g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                flash(_("Customer created."))
                if request.form.get('create_another'):
                    return redirect(url_for("customer.create", create_another=True))
                else:
                    return redirect(url_for("customer.index"))

            flash(error)

    return render_template('customer/create.html')

def get_customer(id, user_id):
    engine, metadata = get_db()
    customers = metadata.tables['customer']
    stmt = select(customers).where(
        customers.c.id == id,
        customers.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, f"Something went wrong.")
    else:
        customer = result.fetchone()

    if customer is None:
        abort(404, f"Customer id {id} doesn't exist.")

    return customer

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    customer = get_customer(id, g.user.id)

    if request.method == 'POST':
        error = None

        if not request.form['label']:
            error = _('Label is required.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            customers = metadata.tables['customer']

            stmt = customers.update().values(
                address=request.form['address'],
                email=request.form['email'],
                label=request.form['label'],
            ).where(
                customers.c.id == id,
                customers.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                flash(_("Customer updated."))
                return redirect(url_for("customer.index"))

    return render_template('customer/update.html', customer=customer)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    engine, metadata = get_db()
    customers = metadata.tables['customer']

    stmt = customers.delete().where(
        customers.c.id == id,
        customers.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
        return redirect(url_for('customer.index'))
    else:
        flash(_("Customer deleted."))
        return redirect(url_for('customer.index'))

def get_customers(user_id):
    engine, metadata = get_db()
    customers = metadata.tables['customer']
    stmt = select(customers).where(
        customers.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, f"Something went wrong.")
    else:
        return result.fetchall()
