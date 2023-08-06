"""rename client to customer

Revision ID: ac14f3a73a29
Revises: ff51555aa2ba
Create Date: 2023-07-15 17:47:10.533820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac14f3a73a29'
down_revision = 'ff51555aa2ba'
branch_labels = None
depends_on = None

def upgrade() -> None:
    with op.batch_alter_table("bill") as bop:
        bop.drop_index('ix_bill_client_id')
        bop.drop_constraint('bill_client_id_fkey', type_='foreignkey')

    op.rename_table('client', 'customer')
    op.alter_column('bill', 'client_id', new_column_name='customer_id')

    with op.batch_alter_table("bill") as bop:
        bop.create_index(op.f('ix_bill_customer_id'), ['customer_id'], unique=False)
        bop.create_foreign_key('bill_customer_id_fkey', 'customer', ['customer_id'], ['id'])

def downgrade() -> None:
    with op.batch_alter_table("bill") as bop:
        bop.drop_index('ix_bill_customer_id')
        bop.drop_constraint('bill_customer_id_fkey', type_='foreignkey')

    op.rename_table('customer', 'client')
    op.alter_column('bill', 'customer_id', new_column_name='client_id')

    with op.batch_alter_table("bill") as bop:
        bop.create_index(op.f('ix_bill_client_id'), ['client_id'], unique=False)
        bop.create_foreign_key('bill_client_id_fkey', 'client', ['client_id'], ['id'])
