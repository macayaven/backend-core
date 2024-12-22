"""Initial migration

Revision ID: acc2a672e03a
Revises: 57ed3b8a2478
Create Date: 2024-12-22 15:47:10.717770

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "acc2a672e03a"
down_revision: Union[str, None] = "57ed3b8a2478"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
