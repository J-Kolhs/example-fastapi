"""Create companies table

Revision ID: b571132e33a2
Revises: 030721dad716
Create Date: 2023-04-15 19:40:41.574938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b571132e33a2'
down_revision = '030721dad716'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('companies_name', sa.String(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable = False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('companies')
