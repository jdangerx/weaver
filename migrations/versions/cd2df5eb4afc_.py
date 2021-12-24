"""Initial migration

Revision ID: cd2df5eb4afc
Revises: 
Create Date: 2021-12-24 13:09:45.091036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cd2df5eb4afc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("password", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("password"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
