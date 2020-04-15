"""empty message

Revision ID: 4bbaff2cf26e
Revises: 1911110c21eb
Create Date: 2020-04-14 21:30:58.223308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4bbaff2cf26e'
down_revision = '1911110c21eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('method_results', sa.Column('relevance_rating_description', sa.Float(), nullable=True))
    op.drop_column('method_results', 'relevance_rating_desciption')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('method_results', sa.Column('relevance_rating_desciption', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('method_results', 'relevance_rating_description')
    # ### end Alembic commands ###
