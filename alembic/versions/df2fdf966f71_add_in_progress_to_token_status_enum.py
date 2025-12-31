"""add in_progress to token status enum

Revision ID: df2fdf966f71
Revises: 4973b6fc7023
Create Date: 2025-12-31 18:28:19.166967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df2fdf966f71'
down_revision: Union[str, Sequence[str], None] = '4973b6fc7023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TYPE tokenstatus ADD VALUE IF NOT EXISTS 'in_progress';"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
