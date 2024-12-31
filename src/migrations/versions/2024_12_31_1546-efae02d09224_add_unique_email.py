"""add unique email

Revision ID: efae02d09224
Revises: 9fedbbb85966
Create Date: 2024-12-31 15:46:24.930661

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "efae02d09224"
down_revision: Union[str, None] = "9fedbbb85966"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
