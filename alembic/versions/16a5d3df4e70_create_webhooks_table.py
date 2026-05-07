"""create webhooks table

Revision ID: 16a5d3df4e70
Revises: 5a9e8bdc43de
Create Date: 2026-05-07 13:07:10.088828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a5d3df4e70'
down_revision: Union[str, Sequence[str], None] = '5a9e8bdc43de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'webhooks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        # JSON column stores the list of subscribed event names
        sa.Column('events', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column(
            'created_at', 
            sa.DateTime(timezone=True), 
            nullable=False,
            server_default=sa.text('now()'),
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_webhooks_id'),
        'webhooks',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_webhooks_id'), table_name='webhooks')
    op.drop_table('webhooks')