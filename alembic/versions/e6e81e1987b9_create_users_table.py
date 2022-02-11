"""Create users table

Revision ID: e6e81e1987b9
Revises: a4a780d49047
Create Date: 2022-02-10 12:52:02.574224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6e81e1987b9'
down_revision = 'a4a780d49047'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))


def downgrade():
    op.drop_table("users")
