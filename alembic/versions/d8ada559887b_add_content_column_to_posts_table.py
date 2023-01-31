"""add content column to posts table

Revision ID: d8ada559887b
Revises: 240ed5966556
Create Date: 2023-01-30 23:45:15.800129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8ada559887b'
down_revision = '240ed5966556'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
