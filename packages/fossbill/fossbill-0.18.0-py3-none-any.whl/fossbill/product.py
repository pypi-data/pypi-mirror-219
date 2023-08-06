from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required
from fossbill.database import get_db, paginatestmt, pagination, filterstmt
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/')
@login_required
def index():
    engine, metadata = get_db()
    products = metadata.tables['product']
    stmt = select(products).where(
        products.c.user_id == g.user.id,
    )
    stmt, filtered = filterstmt(stmt, request)
    stmt, countstmt = paginatestmt(stmt, request)
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            count = conn.execute(countstmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
        products = []
        count = 0
    else:
        products = result.fetchall()
        count = count.fetchone().count

    return render_template(
        'product/index.html',
        products=products,
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

        if not request.form['price']:
            error = _('Price is required.')

        if not request.form['tax_rate']:
            error = _('Tax rate is required.')

        if error is None:
            try:
                float(request.form['price'])
            except ValueError as ve:
                error = _('Price should be a float.')

            try:
                float(request.form['tax_rate'])
            except ValueError as ve:
                error = _('Tax rate should be a float.')

        if error is None:
            if float(request.form['tax_rate']) < 0:
                error = _('Tax rate should be higher than 0.')
            elif float(request.form['tax_rate']) > 100:
                error = _('Tax rate should be lower than 100.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()

            stmt = insert(metadata.tables['product']).values(
                label=request.form['label'],
                price=float(request.form['price'])*100,
                tax_rate=float(request.form['tax_rate']),
                user_id=g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = "Something went wrong."
            else:
                flash(_("Product created."))
                return redirect(url_for("product.index"))

            flash(error)

    return render_template('product/create.html')

def get_product(id, user_id):
    engine, metadata = get_db()
    products = metadata.tables['product']
    stmt = select(products).where(
        products.c.id == id,
        products.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        product = result.fetchone()

    if product is None:
        abort(404, f"Product id {id} doesn't exist.")

    return product

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product(id, g.user.id)

    if request.method == 'POST':
        error = None

        if not request.form['label']:
            error = _('Label is required.')

        if not request.form['price']:
            error = _('Price is required.')

        if not request.form['tax_rate']:
            error = _('Tax rate is required.')

        if error is None:
            try:
                float(request.form['price'])
            except ValueError as ve:
                error = _('Price should be a float.')

            try:
                float(request.form['tax_rate'])
            except ValueError as ve:
                error = _('Tax rate should be a float.')

        if error is None:
            if float(request.form['tax_rate']) < 0:
                error = _('Tax rate should be higher than 0.')
            elif float(request.form['tax_rate']) > 100:
                error = _('Tax rate should be lower than 100.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            products = metadata.tables['product']

            stmt = products.update().values(
                label=request.form['label'],
                price=float(request.form['price'])*100,
                tax_rate=float(request.form['tax_rate']),
            ).where(
                products.c.id == id,
                products.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = "Something went wrong."
            else:
                flash(_("Product updated."))
                return redirect(url_for("product.index"))

    return render_template('product/update.html', product=product)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    engine, metadata = get_db()
    products = metadata.tables['product']

    stmt = products.delete().where(
        products.c.id == id,
        products.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = "Something went wrong."
    else:
        flash(_("Product deleted."))
        return redirect(url_for('product.index'))

def get_products(user_id):
    engine, metadata = get_db()
    products = metadata.tables['product']
    stmt = select(products).where(
        products.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        return result.fetchall()
