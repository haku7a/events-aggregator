"""add server_default for tickets changed_at

Revision ID: d2b48c27595e
Revises: 0f1bc297b813
Create Date: 2026-04-19 21:24:11.382129

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d2b48c27595e"
down_revision: Union[str, Sequence[str], None] = "0f1bc297b813"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("tickets", "changed_at", server_default="now()")


def downgrade() -> None:
    op.alter_column("tickets", "changed_at", server_default=None)
