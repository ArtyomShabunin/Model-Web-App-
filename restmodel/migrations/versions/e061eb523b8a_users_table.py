"""users table

Revision ID: e061eb523b8a
Revises: e86c13eef824
Create Date: 2020-11-18 14:59:34.874568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e061eb523b8a'
down_revision = 'e86c13eef824'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('achive', sa.Column('datetime', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_achive_datetime'), 'achive', ['datetime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_achive_datetime'), table_name='achive')
    op.drop_column('achive', 'datetime')
    # ### end Alembic commands ###
