"""empty message

Revision ID: 22fc0bff1707
Revises: a3f472b7bcb8
Create Date: 2021-02-11 13:17:31.285017

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "22fc0bff1707"
down_revision = "a3f472b7bcb8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
