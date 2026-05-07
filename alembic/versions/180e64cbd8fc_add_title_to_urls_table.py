"""add title to urls table

Revision ID: 180e64cbd8fc
Revises: 
Create Date: 2026-05-07 05:08:53.876515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '180e64cbd8fc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adds the title column to the existing urls table in PostgreSQL.
    # nullable=True → existing rows get NULL automatically; no data loss, no downtime.
    op.add_column('urls', sa.Column('title', sa.String(), nullable=True))


def downgrade() -> None:
    # Exact reverse of upgrade — removes the column.
    # Runs when you do: alembic downgrade -1
    op.drop_column('urls', 'title')