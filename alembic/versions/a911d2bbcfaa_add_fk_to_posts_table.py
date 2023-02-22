"""add fk to posts table

Revision ID: a911d2bbcfaa
Revises: c499b124dc26
Create Date: 2023-02-21 18:23:32.275765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a911d2bbcfaa'
down_revision = 'c499b124dc26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
