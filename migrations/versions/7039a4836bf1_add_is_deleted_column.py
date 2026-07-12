"""add is_deleted column

Revision ID: 7039a4836bf1
Revises: 51ea3c5ff5e7
Create Date: 2026-07-12

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7039a4836bf1"
down_revision: Union[str, Sequence[str], None] = "51ea3c5ff5e7"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "books",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.alter_column(
        "books",
        "is_deleted",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column("books", "is_deleted")