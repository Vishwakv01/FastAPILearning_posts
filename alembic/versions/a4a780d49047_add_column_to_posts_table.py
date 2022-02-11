"""add column to posts table

Revision ID: a4a780d49047
Revises: d2a049d29ff8
Create Date: 2022-02-10 12:46:34.629379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a780d49047'
down_revision = 'd2a049d29ff8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
