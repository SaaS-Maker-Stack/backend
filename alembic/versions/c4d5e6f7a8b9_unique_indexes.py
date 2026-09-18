"""Replace unique constraints + plain indexes with unique indexes

The models declare `unique=True, index=True`, which SQLAlchemy renders as a
single unique index. The early migrations created a UniqueConstraint plus a
non-unique index instead, so `alembic check` reported drift on every fresh
project. Same guarantees, one object per column.

Revision ID: c4d5e6f7a8b9
Revises: b2c3d4e5f6a7
Create Date: 2026-09-18
"""

from collections.abc import Sequence

from alembic import op

revision: str = "c4d5e6f7a8b9"
down_revision: str | Sequence[str] | None = "b2c3d4e5f6a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_COLUMNS = [
    # (table, column, unique constraint name, index name)
    ("users", "email", "users_email_key", "ix_users_email"),
    ("organizations", "slug", "organizations_slug_key", "ix_organizations_slug"),
    (
        "refresh_tokens",
        "token_hash",
        "refresh_tokens_token_hash_key",
        "ix_refresh_tokens_token_hash",
    ),
]


def upgrade() -> None:
    for table, column, constraint, index in _COLUMNS:
        op.drop_constraint(constraint, table, type_="unique")
        op.drop_index(index, table_name=table)
        op.create_index(index, table, [column], unique=True)


def downgrade() -> None:
    for table, column, constraint, index in _COLUMNS:
        op.drop_index(index, table_name=table)
        op.create_index(index, table, [column], unique=False)
        op.create_unique_constraint(constraint, table, [column])
