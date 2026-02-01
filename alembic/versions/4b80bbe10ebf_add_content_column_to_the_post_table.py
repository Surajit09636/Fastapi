"""add content column to the post table

Revision ID: 4b80bbe10ebf
Revises: dd59250edc53
Create Date: 2026-02-01 15:41:01.445964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b80bbe10ebf'
down_revision: Union[str, Sequence[str], None] = 'dd59250edc53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
