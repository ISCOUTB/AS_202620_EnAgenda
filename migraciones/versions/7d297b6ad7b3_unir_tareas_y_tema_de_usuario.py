"""Unir tareas y tema de usuario

Revision ID: 7d297b6ad7b3
Revises: c4d5e6f7a801, d91f6a2c804e
Create Date: 2026-11-23 05:38:51.686639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d297b6ad7b3'
down_revision: Union[str, Sequence[str], None] = ('c4d5e6f7a801', 'd91f6a2c804e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
