"""Initial database schema

Revision ID: b2eaa5cd6586
Revises: c8208f19da44
Create Date: 2025-06-28 13:33:23.535070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2eaa5cd6586'
down_revision: Union[str, None] = 'c8208f19da44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
