"""create rooms table

Revision ID: b0219664b581
Revises: 6c95b0688c52
Create Date: 2023-01-31 00:55:20.881770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0219664b581'
down_revision = '6c95b0688c52'
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('room_name', sa.String(), nullable = False),
        sa.Column('owner_id', sa.Integer(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable = False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key('rooms_users_fkey',
                                            source_table='rooms',
                                            referent_table='users',
                                            local_cols=['owner_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(constraint_name='rooms_users_fkey', table_name='rooms', type_='foreignkey' )
    op.drop_table('rooms')
