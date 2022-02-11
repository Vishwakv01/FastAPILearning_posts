"""add foreignkey to posts table

Revision ID: ac527e244a83
Revises: e6e81e1987b9
Create Date: 2022-02-10 13:25:33.389831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac527e244a83'
down_revision = 'e6e81e1987b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users",
                        local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", column_name="user_id")
    pass
