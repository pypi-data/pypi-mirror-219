from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String,
    ForeignKey, Date, DateTime, Boolean, UniqueConstraint, Identity,
    CheckConstraint, func, select, literal_column, Text, JSON,
)
import click
from flask import current_app, g, Blueprint
from alembic.config import Config
from alembic import command
import os

def filterstmt(stmt, request):
    stmt = select(stmt.alias())
    filtered = False
    for key, value in request.args.items(multi=True):
        if len(value) == 0:
            continue
        splitted = key.split("__")
        unit = "str"
        match len(splitted):
            case 2:
                key, kind = splitted
            case 3:
                key, unit, kind = splitted
            case _:
                continue
        match unit:
            case "price":
                value = float(value) * 100
        filtered = True
        match kind:
            case 'select_custom':
                rules = value.split("__and__")
                for rule in rules:
                    splitted = rule.split("__")
                    match len(splitted):
                        case 2:
                            key, kind = splitted
                        case _:
                            continue
                    match kind:
                        case 'null':
                            stmt = stmt.where(literal_column(key) == None)
                        case 'not_null':
                            stmt = stmt.where(literal_column(key).is_not(None))
            case 'ilike':
                stmt = stmt.where(literal_column(key).ilike("%" + value + "%"))
            case 'eq':
                stmt = stmt.where(literal_column(key) == value)
            case 'le':
                stmt = stmt.where(literal_column(key) <= value)
            case 'ge':
                stmt = stmt.where(literal_column(key) >= value)
    return stmt, filtered

def paginatestmt(stmt, request):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 15))

    return (
        stmt.limit(limit).offset((page-1) * limit),
        select(func.count()).select_from(stmt.subquery())
    )

def pagination(count, request):
    current = int(request.args.get('page', 1))
    maximum = int(max(count / int(request.args.get('limit', 15)), 1))
    mindisplayed = max(min(current - 10, maximum - 20), 1)
    maxdisplayed = min(mindisplayed + 20, maximum)
    return {
        'cur': current,
        'max': maximum,
        'mindisplayed': mindisplayed,
        'maxdisplayed': maxdisplayed,
    }

def get_db():
    if 'engine' not in g:
        g.database_url = current_app.config['DATABASE']
        g.engine = create_engine(
            g.database_url,
            echo=current_app.config.get('SQLALCHEMY_ECHO', False),
        )

    if 'metadata' not in g:
        g.metadata = MetaData()

        user = Table('user', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50), unique=True, nullable=False),
            Column('password', String(120), nullable=False),
            Column('stripe_customer', String(256), nullable=True),
            Column('admin', Boolean(), nullable=False, default=False),
            Column('due_at', Date, nullable=True),
            Column('created_at', Date, nullable=False, server_default=func.current_date()),
        )

        product = Table('product', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('label', String(120), nullable=False),
            Column('price', Integer, nullable=False),
            Column('tax_rate', Integer, nullable=False),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
        )

        client = Table('client', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('address', String(500), nullable=False),
            Column('email', String(70), nullable=False),
            Column('label', String(40), nullable=False),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
        )

        client = Table('bill', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('client_id', Integer, ForeignKey("client.id"), nullable=True, index=True),
            Column('comment', String(500), nullable=True),
            Column('date', Date, nullable=False),
            Column('bill_number', Integer, nullable=True, index=True),
            Column('quote_number', Integer, nullable=True, index=True),
            Column('recipient', String(500), nullable=True),
            Column('source', String(500), nullable=True),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
            Column('bill_mentions', String(500), nullable=True),
            Column('quote_mentions', String(500), nullable=True),
            Column('paid', Boolean(), nullable=False, server_default='FALSE'),
            UniqueConstraint('user_id', 'bill_number'),
            UniqueConstraint('user_id', 'quote_number'),
        )

        client = Table('bill_row', g.metadata,
            Column('bill_id', Integer, ForeignKey("bill.id"), nullable=False, index=True),
            Column('id', Integer, primary_key=True),
            Column('label', String(120), nullable=False),
            Column('price', Integer, nullable=False),
            Column('quantity', Integer, nullable=False),
            Column('tax_rate', Integer, nullable=False),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
        )

        client = Table('user_pref', g.metadata,
            Column('bill_mentions', String(500), nullable=True),
            Column('currency', String(10), nullable=True),
            Column('email', String(254), unique=True, nullable=True),
            Column('id', Integer, primary_key=True),
            Column('locale', String(10), nullable=False, default='en_US'),
            Column('quote_mentions', String(500), nullable=True),
            Column('smtp_host', String(30), nullable=True),
            Column('smtp_password', String(30), nullable=True),
            Column('smtp_port', Integer, nullable=True),
            Column('smtp_security', String(10), nullable=True),
            Column('smtp_username', String(30), nullable=True),
            Column('smtp_reply_to', String(254), nullable=True),
            Column('smtp_cc', String(508), nullable=True),
            Column('source', String(500), nullable=True),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
        )

        client = Table('user_password_reset_token', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
            Column('token', String(128), nullable=False, unique=True),
            Column('expire_at', DateTime, nullable=False, server_default=func.now()),
        )

        payment = Table('payment', g.metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False, index=True),
            Column('date', Date, nullable=False),
            Column('valid_for_service_thru', Date, nullable=False),
            Column('amount', Integer, nullable=False),
            Column('currency', String(10), nullable=True),
            Column('payload', JSON, nullable=True),
            Column('card_brand', String(20), nullable=True),
            Column('card_last4', String(4), nullable=True),
            Column('receipt_url', String(500), nullable=True),
        )

    return (g.engine, g.metadata)

bp = Blueprint('db', __name__)

def get_alembic_config():
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), 'alembic.ini')
    alembic_cfg = Config(alembic_cfg_path)
    alembic_cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), 'alembic'))
    return alembic_cfg

@bp.cli.command('branches')
def branches():
    command.branches(get_alembic_config())

@bp.cli.command('check')
def check():
    command.check(get_alembic_config())

@bp.cli.command('current')
def current():
    command.current(get_alembic_config())

@bp.cli.command('downgrade')
@click.argument('rev')
def downgrade(rev):
    command.downgrade(get_alembic_config(), rev)

@bp.cli.command('ensure_version')
def ensure_version():
    command.ensure_version(get_alembic_config())

@bp.cli.command('heads')
def heads():
    command.heads(get_alembic_config())

@bp.cli.command('history')
def history():
    command.history(get_alembic_config())

@bp.cli.command('list_templates')
def list_templates():
    command.list_templates(get_alembic_config())

@bp.cli.command('merge')
def merge():
    command.merge(get_alembic_config())

@bp.cli.command('revision')
@click.option('-m', '--message')
@click.option('--autogenerate', is_flag=True)
def revision(message, autogenerate):
    command.revision(get_alembic_config(), message=message, autogenerate=autogenerate)

@bp.cli.command('show')
@click.argument('rev', default='head')
def show(rev):
    command.show(get_alembic_config(), rev)

@bp.cli.command('upgrade')
@click.argument('rev')
def upgrade(rev):
    command.upgrade(get_alembic_config(), rev)
