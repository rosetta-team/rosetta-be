"""empty message

Revision ID: da35377fe679
Revises: 41fc11abae0d
Create Date: 2020-04-11 17:34:12.227018

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da35377fe679'
down_revision = '41fc11abae0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('method_results', sa.Column('relevance_rating_desciption', sa.Float(), nullable=True))
    op.add_column('method_results', sa.Column('weighted_relevancy_rating', sa.Float(), nullable=True))
    op.drop_column('method_results', 'relevance_rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('method_results', sa.Column('relevance_rating', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('method_results', 'weighted_relevancy_rating')
    op.drop_column('method_results', 'relevance_rating_desciption')
    # ### end Alembic commands ###
