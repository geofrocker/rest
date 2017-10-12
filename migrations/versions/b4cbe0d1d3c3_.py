"""empty message

Revision ID: b4cbe0d1d3c3
Revises: 6ccb56ae0815
Create Date: 2017-10-12 23:32:32.362676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4cbe0d1d3c3'
down_revision = '6ccb56ae0815'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Category_created_by_fkey', 'Category', type_='foreignkey')
    op.create_foreign_key(None, 'Category', 'User', ['created_by'], ['username'])
    op.drop_constraint('Recipe_created_by_fkey', 'Recipe', type_='foreignkey')
    op.create_foreign_key(None, 'Recipe', 'User', ['created_by'], ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Recipe', type_='foreignkey')
    op.create_foreign_key('Recipe_created_by_fkey', 'Recipe', 'User', ['created_by'], ['id'])
    op.drop_constraint(None, 'Category', type_='foreignkey')
    op.create_foreign_key('Category_created_by_fkey', 'Category', 'User', ['created_by'], ['id'])
    # ### end Alembic commands ###