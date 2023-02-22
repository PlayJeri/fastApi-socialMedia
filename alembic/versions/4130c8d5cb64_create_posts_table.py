"""create posts table

Revision ID: 4130c8d5cb64
Revises: 
Create Date: 2023-02-21 18:03:11.375107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4130c8d5cb64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
