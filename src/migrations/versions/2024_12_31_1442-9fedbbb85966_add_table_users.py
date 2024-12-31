"""add table users

Revision ID: 9fedbbb85966
Revises: 9ec889dbba68
Create Date: 2024-12-31 14:42:10.904307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fedbbb85966'
down_revision: Union[str, None] = '9ec889dbba68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('hashed_password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
