"""default created updated at

Revision ID: fe9731c112f0
Revises: 53eb75b221e1
Create Date: 2025-12-25 14:45:17.702436+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fe9731c112f0'
down_revision: Union[str, Sequence[str], None] = '53eb75b221e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'tournament', 'created_at',
        existing_server_default=None,
        server_default=sa.text('NOW()')
    )
    op.alter_column(
        'tournament', 'updated_at',
        existing_server_default=None,
        server_default=sa.text('NOW()')
    )
    op.alter_column(
        'event', 'created_at',
        existing_server_default=None,
        server_default=sa.text('NOW()')
    )
    op.alter_column(
        'event', 'updated_at',
        existing_server_default=None,
        server_default=sa.text('NOW()')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'tournament', 'created_at',
        server_default=None,
        existing_server_default=sa.text('NOW()')
    )
    op.alter_column(
        'tournament', 'updated_at',
        server_default=None,
        existing_server_default=sa.text('NOW()')
    )
    op.alter_column(
        'event', 'created_at',
        server_default=None,
        existing_server_default=sa.text('NOW()')
    )
    op.alter_column(
        'event', 'updated_at',
        server_default=None,
        existing_server_default=sa.text('NOW()')
    )
