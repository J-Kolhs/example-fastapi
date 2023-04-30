"""Add roles to users table

Revision ID: 030721dad716
Revises: d20164d49736
Create Date: 2023-04-13 11:35:13.399907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030721dad716'
down_revision = 'd20164d49736'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('roles', sa.String(), nullable=False, server_default='BASIC'))
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False, server_default='None'))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False, server_default='None'))
    op.add_column('users', sa.Column('company_name', sa.String(), nullable=False, server_default='None'))


def downgrade() -> None:
    op.drop_column('users', 'roles')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'company_name')
