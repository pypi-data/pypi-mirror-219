import functools
from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from fossbill.database import get_db
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import gettext
import os
import uuid
import smtplib
from email.message import EmailMessage
import datetime
import binascii

bp = Blueprint('auth', __name__, url_prefix='/auth')

def csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = binascii.hexlify(os.urandom(64)).decode()
    return """<input
        type='hidden'
        name='_csrf_token'
        value='{}' />""".format(session['_csrf_token'])

@bp.before_app_request
def csrf_required():
    if current_app.config.get('TESTING'):
        return
    if request.method != 'POST':
        return
    if not request.form.get('_csrf_token'):
         abort(403)
    if request.form.get('_csrf_token') != session.get('_csrf_token'):
         abort(403)

def setup(app):
    app.jinja_env.globals['csrf_token'] = csrf_token

def get_system_smtp_server():
    if current_app.config['SMTP_SECURITY'] == "TLS":
        server = smtplib.SMTP_SSL(
            host=current_app.config['SMTP_HOST'],
            port=current_app.config['SMTP_PORT'],
            timeout=10
        )
    else:
        server = smtplib.SMTP(
            host=current_app.config['SMTP_HOST'],
            port=current_app.config['SMTP_PORT'],
            timeout=10
        )
        if current_app.config['SMTP_SECURITY'] == "STARTTLS":
            server.starttls()

    server.login(
        current_app.config['SMTP_USERNAME'],
        current_app.config['SMTP_PASSWORD']
    )

    return server

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        engine, metadata = get_db()
        error = None

        if not username:
            error = _('Username is required.')
        elif not password:
            error = _('Password is required.')

        if error is None:
            try:
                with engine.connect() as conn:
                    stmt = insert(metadata.tables['user']).values(
                        username=username,
                        password=generate_password_hash(password)
                    )
                    result = conn.execute(stmt)

                    stmt = insert(metadata.tables['user_pref']).values(
                        user_id=result.inserted_primary_key[0],
                        locale=g.locale,
                    )
                    result = conn.execute(stmt)

                    conn.commit()
            except IntegrityError as e:
                error = f"User {username} is already registered."
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        engine, metadata = get_db()
        error = None

        users = metadata.tables['user']

        stmt = select(users).where(users.c.username == username)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        user = result.fetchone()

        if user is None:
            error = _('Incorrect username.')
        elif not check_password_hash(user.password, password):
            error = _('Incorrect password.')

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('landing.home'))

        flash(error)

    return render_template('auth/login.html')

def send_user_password_reset_token(reset_token, user_pref):
    body = render_template(
        'auth/reset_password_email.plain',
        token=reset_token.token
    )

    msg = EmailMessage()
    msg["From"] = current_app.config['SMTP_USERNAME']
    msg["To"] = user_pref.email
    msg["Subject"] = _("Fossbill - User password reset")
    msg.set_content(body)

    server = get_system_smtp_server()
    server.send_message(msg)
    server.quit()

@bp.route('/ask_reset_password', methods=('GET', 'POST'))
def ask_reset_password():
    if request.method == 'POST':
        error = None

        if not request.form['email']:
            error = _('Email is required.')

        if error is not None:
            flash(error)
        else:
            engine, metadata = get_db()

            user_prefs = metadata.tables['user_pref']

            try:
                with engine.connect() as conn:
                    stmt = select(user_prefs).where(
                        user_prefs.c.email == request.form['email']
                    )
                    result = conn.execute(stmt)
                    user_pref = result.fetchone()

                if user_pref:
                    reset_token = build_user_password_reset_token(user_pref)
                    send_user_password_reset_token(reset_token, user_pref)
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                error = f"Something went wrong."
            except smtplib.SMTPException as e:
                current_app.logger.error(str(e))
                flash(_("We failed to send the mail: " + str(e)))
            else:
                flash(_("If the email matched, a password reset token has been generated."))

            return redirect(url_for("auth.login"))

    return render_template('auth/ask_reset_password.html')

@bp.route('/use_reset_password', methods=('GET', 'POST'))
def use_reset_password():
    if request.method == 'POST':
        error = None

        if not request.form['token']:
            error = _('Token is required.')

        if not request.form['password']:
            error = _('Password is required.')

        if error is not None:
            flash(error)
             # to not redirect
            return render_template('auth/use_reset_password.html')
        else:
            engine, metadata = get_db()

            user_password_reset_tokens = metadata.tables['user_password_reset_token']
            users = metadata.tables['user']

            try:
                with engine.connect() as conn:
                    stmt = select(user_password_reset_tokens).where(
                        user_password_reset_tokens.c.token == request.form['token']
                    )
                    result = conn.execute(stmt)
                    reset_token = result.fetchone()
                    if None == reset_token :
                        flash(_("Invalid token."))
                        return redirect(url_for("auth.login"))

                    if reset_token.expire_at < datetime.datetime.now():
                        flash(_("Token already expired."))
                        return redirect(url_for("auth.login"))

                    stmt = select(users).where(
                        users.c.id == reset_token.user_id
                    )
                    result = conn.execute(stmt)
                    user = result.fetchone()

                    stmt = users.update().values(
                        password=generate_password_hash(request.form['password'])
                    ).where(
                        users.c.id == user.id,
                    )
                    result = conn.execute(stmt)

                    stmt = user_password_reset_tokens.delete().where(
                        user_password_reset_tokens.c.token == request.form['token'],
                    )
                    result = conn.execute(stmt)

                    conn.commit()
            except SQLAlchemyError as e:
                current_app.logger.error(str(e))
                flash(_("Something went wrong."))
            else:
                flash(_("Password updated."))

            return redirect(url_for("auth.login"))

    if not request.args.get('token'):
        flash(_('Token is required.'))
        return redirect(url_for("auth.login"))

    return render_template('auth/use_reset_password.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def is_user_pref_smtp_enough():
    if not g.user_pref:
        return False

    if not g.user_pref.smtp_security:
        return False
    if not g.user_pref.smtp_host:
        return False
    if not g.user_pref.smtp_port:
        return False
    if not g.user_pref.smtp_username:
        return False
    if not g.user_pref.smtp_password:
        return False

    return True

def user_pref_smtp_enough(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_user_pref_smtp_enough():
            flash(_("We need more of your SMTP configuration."), 'important')
            return redirect(url_for("me.update"))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('landing.home'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        g.user_pref = None
        return

    engine, metadata = get_db()

    users = metadata.tables['user']
    stmt = select(users).where(users.c.id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    g.user = result.fetchone()

    user_prefs = metadata.tables['user_pref']
    stmt = select(user_prefs).where(user_prefs.c.user_id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    g.user_pref = result.fetchone()

    # To be retro-compatible
    if g.user_pref:
        return
    with engine.connect() as conn:
        stmt = insert(user_prefs).values(user_id=user_id)
        result = conn.execute(stmt)
        conn.commit()

    # Retry
    stmt = select(user_prefs).where(user_prefs.c.user_id == user_id)
    with engine.connect() as conn:
        result = conn.execute(stmt)
    g.user_pref = result.fetchone()

@bp.before_app_request
def setup_locale():
    if g.user_pref is not None:
        g.locale = g.user_pref.locale
    else:
        g.locale = request.accept_languages.best_match(["en_US", "fr_FR"])
    if not g.locale:
        g.locale = 'en_US'

    localedir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/locale"
    translation = gettext.translation("messages", localedir, languages=[g.locale, "en_US"])
    translation.install()
    current_app.jinja_env.install_gettext_translations(translation)

def build_user_password_reset_token(user_pref):
    engine, metadata = get_db()
    user_password_reset_tokens = metadata.tables['user_password_reset_token']

    with engine.connect() as conn:
        stmt = insert(user_password_reset_tokens).values(
            token=str(uuid.uuid4()),
            user_id=user_pref.user_id,
            expire_at=datetime.datetime.now() + datetime.timedelta(minutes=10),
        )
        result = conn.execute(stmt)

        stmt = select(user_password_reset_tokens).where(
            user_password_reset_tokens.c.id == result.inserted_primary_key[0]
        )
        result = conn.execute(stmt)
        conn.commit()

        return result.fetchone()
