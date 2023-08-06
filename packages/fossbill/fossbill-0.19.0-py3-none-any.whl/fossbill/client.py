from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required
from fossbill.database import get_db, paginatestmt, pagination, filterstmt
from sqlalchemy import insert, select, func
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('client', __name__, url_prefix='/clients')

@bp.route('/')
@login_required
def index():
    engine, metadata = get_db()
    clients = metadata.tables['client']
    stmt = select(clients).where(
        clients.c.user_id == g.user.id,
    )
    stmt, filtered = filterstmt(stmt, request)
    stmt, countstmt = paginatestmt(stmt, request)
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            count = conn.execute(countstmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = f"Something went wrong."
        clients = []
        count = 0
    else:
        clients = result.fetchall()
        count = count.fetchone().count

    return render_template(
        'client/index.html',
        clients=clients,
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

            stmt = insert(metadata.tables['client']).values(
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
                flash(_("Client created."))
                return redirect(url_for("client.index"))

            flash(error)

    return render_template('client/create.html')

def get_client(id, user_id):
    engine, metadata = get_db()
    clients = metadata.tables['client']
    stmt = select(clients).where(
        clients.c.id == id,
        clients.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, f"Something went wrong.")
    else:
        client = result.fetchone()

    if client is None:
        abort(404, f"Client id {id} doesn't exist.")

    return client

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    client = get_client(id, g.user.id)

    if request.method == 'POST':
        error = None

        if not request.form['label']:
            error = _('Label is required.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()
            clients = metadata.tables['client']

            stmt = clients.update().values(
                address=request.form['address'],
                email=request.form['email'],
                label=request.form['label'],
            ).where(
                clients.c.id == id,
                clients.c.user_id == g.user.id,
            )
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                flash(_("Client updated."))
                return redirect(url_for("client.index"))

    return render_template('client/update.html', client=client)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    engine, metadata = get_db()
    clients = metadata.tables['client']

    stmt = clients.delete().where(
        clients.c.id == id,
        clients.c.user_id == g.user.id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
        return redirect(url_for('client.index'))
    else:
        flash(_("Client deleted."))
        return redirect(url_for('client.index'))

def get_clients(user_id):
    engine, metadata = get_db()
    clients = metadata.tables['client']
    stmt = select(clients).where(
        clients.c.user_id == user_id,
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, f"Something went wrong.")
    else:
        return result.fetchall()
