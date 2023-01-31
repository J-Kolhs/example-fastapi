"""Add user table

Revision ID: d7bd6ab76bca
Revises: d8ada559887b
Create Date: 2023-01-30 23:50:24.280671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7bd6ab76bca'
down_revision = 'd8ada559887b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable = False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
