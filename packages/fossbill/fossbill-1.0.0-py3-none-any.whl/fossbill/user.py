import functools
from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from fossbill.auth import login_required, build_user_password_reset_token, send_user_password_reset_token
from fossbill.database import get_db, paginatestmt, pagination, filterstmt
from sqlalchemy import insert, select, join, func, literal_column, desc, case
from sqlalchemy.exc import SQLAlchemyError
import smtplib

bp = Blueprint('user', __name__, url_prefix='/users')

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user.admin:
            abort(404)

        return view(**kwargs)

    return wrapped_view

@bp.route('/')
@admin_required
@login_required
def index():
    engine, metadata = get_db()

    users = metadata.tables['user']
    user_prefs = metadata.tables['user_pref']

    j = join(users, user_prefs, users.c.id == user_prefs.c.user_id)
    stmt = select(users, user_prefs).select_from(j)
    stmt, filtered = filterstmt(stmt, request)
    stmt, countstmt = paginatestmt(stmt, request)
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            count = conn.execute(countstmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        flash(_("Something went wrong."))
        users = []
        count = 0
    else:
        users = result.fetchall()
        count = count.fetchone().count

    return render_template(
        'user/index.html',
        users=users,
        pagination=pagination(count, request),
        filtered=filtered,
    )

def get_user_user_pref(id):
    engine, metadata = get_db()

    users = metadata.tables['user']
    user_prefs = metadata.tables['user_pref']

    j = join(users, user_prefs, users.c.id == user_prefs.c.user_id)
    stmt = select(users, user_prefs).select_from(j).where(
        users.c.id == id
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        abort(500, "Something went wrong.")
    else:
        user = result.fetchone()

    if user is None:
        abort(404, f"User {id} doesn't exist.")

    return user

@bp.route('/<int:id>/generate_reset_password', methods=['POST'])
@admin_required
@login_required
def generate_reset_password(id):
    user = get_user_user_pref(id)

    try:
        reset_token = build_user_password_reset_token(user)
        if user.email:
                send_user_password_reset_token(reset_token, user)
                flash(_("A password reset token has been generated, and sent"))
        else:
            flash(_("A password reset token has been generated."))
        flash(_(url_for("auth.use_reset_password", _external=True, token=reset_token.token)))
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))
        error = f"Something went wrong."
    except smtplib.SMTPException as e:
        current_app.logger.error(str(e))
        flash(_("We failed to send the mail: " + str(e)))

    return redirect(url_for("user.index"))
