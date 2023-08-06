"""bills date to created_at

Revision ID: 7899e98936b3
Revises: 21487ff4ab8c
Create Date: 2023-07-15 08:19:00.422178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7899e98936b3'
down_revision = '21487ff4ab8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('bill', 'date', new_column_name='created_at')


def downgrade() -> None:
    op.alter_column('bill', 'created_at', new_column_name='date')
