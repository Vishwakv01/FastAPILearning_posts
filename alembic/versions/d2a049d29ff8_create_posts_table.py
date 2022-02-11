"""Create posts table

Revision ID: d2a049d29ff8
Revises: 
Create Date: 2022-02-10 10:27:21.061405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a049d29ff8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                            sa.Column("title", sa.String(), nullable=False))
    pass



def downgrade():
    op.drop_table("posts")
    pass
