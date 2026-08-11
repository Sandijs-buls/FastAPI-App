"""Add last few columns to post table

Revision ID: 91dd49feffbb
Revises: feea603be2ce
Create Date: 2026-08-11 20:25:20.953875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91dd49feffbb'
down_revision: Union[str, Sequence[str], None] = 'feea603be2ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at ')
    pass
