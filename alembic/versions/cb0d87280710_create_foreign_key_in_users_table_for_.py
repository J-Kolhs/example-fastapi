"""Create foreign key in Users table for company_id

Revision ID: cb0d87280710
Revises: b571132e33a2
Create Date: 2023-04-15 19:51:21.923101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0d87280710'
down_revision = 'b571132e33a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'company_name')
    op.add_column('users', sa.Column('company_id', sa.Integer()), nullable=False)
    op.create_foreign_key('users_companies_fkey',
                                            source_table='users',
                                            referent_table='companies',
                                            local_cols=['company_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")



def downgrade() -> None:
    op.add_column('users', sa.Column('company_name', sa.String(), nullable=False, server_default='None'))
    op.drop_column('users', 'company_id')
    op.drop_constraint(constraint_name='users_companies_fkey', table_name='users', type_='foreignkey' )