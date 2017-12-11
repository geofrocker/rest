"""empty message

Revision ID: e18b4fbc0896
Revises: a107a373fa33
Create Date: 2017-12-01 20:13:15.797834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e18b4fbc0896'
down_revision = 'a107a373fa33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Recipe', 'upvotes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Recipe', sa.Column('upvotes', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
