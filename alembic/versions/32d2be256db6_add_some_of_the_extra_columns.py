"""add some of the extra columns

Revision ID: 32d2be256db6
Revises: ac527e244a83
Create Date: 2022-02-10 13:40:06.204401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32d2be256db6'
down_revision = 'ac527e244a83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="True", nullable=False),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),)
    pass


def downgrade():
    op.drop_column("posts", column_name="published")
    op.drop_column("posts", column_name="created_at")
    pass
