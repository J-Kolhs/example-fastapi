"""Add foreign key to posts table

Revision ID: d15f0385e50f
Revises: d7bd6ab76bca
Create Date: 2023-01-30 23:58:18.818893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd15f0385e50f'
down_revision = 'd7bd6ab76bca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey',
                                            source_table='posts',
                                            referent_table='users',
                                            local_cols=['owner_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint(constraint_name='posts_users_fkey', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass