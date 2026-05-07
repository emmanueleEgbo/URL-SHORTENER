"""create urls table

Revision ID: 5a9e8bdc43de
Revises: 
Create Date: 2026-05-07 12:29:51.764451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a9e8bdc43de'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('long_url', sa.String(), nullable=False),
        sa.Column('short_code', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('long_url')
    )

    op.create_index(
        op.f('ix_urls_id'),
        'urls',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_urls_short_code'),
        'urls',
        ['short_code'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_urls_short_code'), table_name='urls')
    op.drop_index(op.f('ix_urls_id'), table_name='urls')
    op.drop_table('urls')