"""add content column to posts

Revision ID: a3bd0f291b1d
Revises: 4130c8d5cb64
Create Date: 2023-02-21 18:11:22.548039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3bd0f291b1d'
down_revision = '4130c8d5cb64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
