"""add last few columns to posts table

Revision ID: df86d8dcc59a
Revises: a911d2bbcfaa
Create Date: 2023-02-21 18:29:16.597258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df86d8dcc59a'
down_revision = 'a911d2bbcfaa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),
        nullable=False, server_default='TRUE'),
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.text('NOW()')))
    )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
