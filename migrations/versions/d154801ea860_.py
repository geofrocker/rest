"""empty message

Revision ID: d154801ea860
Revises: 19f16524cd21
Create Date: 2017-11-27 11:08:46.079465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd154801ea860'
down_revision = '19f16524cd21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Review',
    sa.Column('review_id', sa.String(length=120), nullable=False),
    sa.Column('content', sa.String(length=120), nullable=True),
    sa.Column('recipe_id', sa.String(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['User.username'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.recipe_id'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Review')
    # ### end Alembic commands ###