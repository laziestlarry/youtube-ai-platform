"""Add provider to User model for social auth

Revision ID: ef6c90364780
Revises: db671a24ff03
Create Date: 2025-06-28 13:55:16.008855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef6c90364780'
down_revision: Union[str, None] = 'db671a24ff03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
