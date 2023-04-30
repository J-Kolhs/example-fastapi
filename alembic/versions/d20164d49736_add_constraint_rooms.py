"""Add unique constraint on room name

Revision ID: d20164d49736
Revises: bbb5bf091d4e
Create Date: 2023-02-26 02:16:25.969997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd20164d49736'
down_revision = 'bbb5bf091d4e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("rooms_unique_room_name", "rooms", ["room_name"])


def downgrade() -> None:
    op.drop_constraint('rooms_unique_room_name', 'rooms', type_='unique')