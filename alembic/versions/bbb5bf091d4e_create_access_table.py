"""create access table

Revision ID: bbb5bf091d4e
Revises: eb8fbcba7818
Create Date: 2023-02-25 18:00:53.331012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbb5bf091d4e'
down_revision = 'eb8fbcba7818'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'access',
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('user_id', sa.Integer(), nullable = False),
        sa.Column('room_id', sa.Integer(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable = False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_unique_constraint("access_unique_user_room", "access", ["user_id", "room_id"])

    op.create_foreign_key('access_users_fkey',
                                            source_table='access',
                                            referent_table='users',
                                            local_cols=['user_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")
    op.create_foreign_key('access_rooms_fkey',
                                            source_table='access',
                                            referent_table='rooms',
                                            local_cols=['room_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint(constraint_name='access_users_fkey', table_name='access', type_='foreignkey' )
    op.drop_constraint(constraint_name='access_rooms_fkey', table_name='access', type_='foreignkey' )
    op.drop_constraint(constraint_name='access_unique_user_room', table_name='access', type_='unique')
    op.drop_table('access')