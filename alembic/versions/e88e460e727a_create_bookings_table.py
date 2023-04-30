"""Create bookings table

Revision ID: e88e460e727a
Revises: b0219664b581
Create Date: 2023-02-15 14:27:50.105742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e88e460e727a'
down_revision = 'b0219664b581'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
        sa.Column('meeting_name', sa.String(), nullable = False),
        sa.Column('meeting_start', sa.TIMESTAMP(timezone = True), nullable = False),
        sa.Column('meeting_end', sa.TIMESTAMP(timezone = True), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable = False),
        sa.Column('owner_id', sa.Integer(), nullable = False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key('bookings_users_fkey',
                                            source_table='bookings',
                                            referent_table='users',
                                            local_cols=['owner_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")
    
    op.create_foreign_key('bookings_rooms_fkey',
                                            source_table='bookings',
                                            referent_table='rooms',
                                            local_cols=['room_id'],
                                            remote_cols=['id'],
                                            ondelete="CASCADE")
    

    pass

def downgrade() -> None:
    op.drop_constraint(constraint_name='bookings_users_fkey', table_name='bookings', type_='foreignkey')    
    op.drop_constraint(constraint_name='bookings_rooms_fkey', table_name='bookings', type_='foreignkey')
    op.drop_table('bookings')
    pass