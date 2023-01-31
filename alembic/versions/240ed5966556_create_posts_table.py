"""Create Posts Table

Revision ID: 240ed5966556
Revises: 
Create Date: 2023-01-30 23:36:49.726403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240ed5966556'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
        sa.Column('title', sa.String(), nullable = False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
