"""Create post table

Revision ID: e6d5fbc84522
Revises: 
Create Date: 2026-08-08 15:59:05.922793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6d5fbc84522'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #for tmr : drop all the tables and we simulating how to add the tables one by one.
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable= False),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Post')
    pass
