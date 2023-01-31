"""Add last few columns to posts table

Revision ID: 16233c86ae88
Revises: d15f0385e50f
Create Date: 2023-01-31 00:03:47.311744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16233c86ae88'
down_revision = 'd15f0385e50f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
