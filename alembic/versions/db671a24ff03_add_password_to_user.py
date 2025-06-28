"""Add password to user

Revision ID: db671a24ff03
Revises: b2eaa5cd6586
Create Date: 2025-06-28 13:34:37.217511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db671a24ff03'
down_revision: Union[str, None] = 'b2eaa5cd6586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
