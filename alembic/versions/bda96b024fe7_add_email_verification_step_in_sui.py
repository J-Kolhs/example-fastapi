"""Add email verification step in SUI

Revision ID: bda96b024fe7
Revises: 87e4dd3f0be2
Create Date: 2023-04-25 11:15:58.754257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = 'bda96b024fe7'
down_revision = '87e4dd3f0be2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.Boolean, nullable=False, server_default= text('False')))

def downgrade() -> None:
    op.drop_column('users', 'is_verified')