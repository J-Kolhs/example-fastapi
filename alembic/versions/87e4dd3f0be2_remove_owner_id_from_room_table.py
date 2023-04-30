"""Remove owner_id from Room table

Revision ID: 87e4dd3f0be2
Revises: cb0d87280710
Create Date: 2023-04-22 13:12:47.474530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87e4dd3f0be2'
down_revision = 'cb0d87280710'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(constraint_name='rooms_users_fkey', table_name='rooms', type_='foreignkey' )
    op.drop_column('rooms', 'owner_id')


def downgrade() -> None:
    op.add_column('rooms', sa.Column('owner_id', sa.Integer()), nullable=False)
    op.create_foreign_key('rooms_users_fkey',
                                        source_table='rooms',
                                        referent_table='users',
                                        local_cols=['owner_id'],
                                        remote_cols=['id'],
                                        ondelete="CASCADE")