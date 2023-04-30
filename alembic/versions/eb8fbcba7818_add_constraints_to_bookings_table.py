"""Add a constraint to bookings table

Revision ID: eb8fbcba7818
Revises: e88e460e727a
Create Date: 2023-02-19 15:05:54.190112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import NUMRANGE


# revision identifiers, used by Alembic.
revision = 'eb8fbcba7818'
down_revision = 'e88e460e727a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        'meetingStart_before_meetingEnd',
        table_name='bookings',
        condition="meeting_start < meeting_end")
    op.create_exclude_constraint(
        "unique_bookings",
        "bookings",
        (sa.func.int4range( sa.text('0'), sa.Column('room_id'), bounds="[]"), '='),
        (sa.func.tstzrange(sa.Column('meeting_start'), sa.Column('meeting_end')),'&&')        
    )

def downgrade() -> None:
    op.drop_constraint(constraint_name='meetingStart_before_meetingEnd', table_name='bookings', type_= 'check')
    op.drop_constraint(constraint_name='unique_bookings', table_name='bookings')