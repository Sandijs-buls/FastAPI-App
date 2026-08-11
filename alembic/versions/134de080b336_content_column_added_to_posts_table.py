"""content column added to posts table

Revision ID: 134de080b336
Revises: e6d5fbc84522
Create Date: 2026-08-11 19:58:10.076413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '134de080b336'
down_revision: Union[str, Sequence[str], None] = 'e6d5fbc84522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'content')
    pass
