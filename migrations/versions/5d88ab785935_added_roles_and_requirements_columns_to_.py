"""Added roles and requirements columns to Job model

Revision ID: 5d88ab785935
Revises: 
Create Date: 2025-02-13 10:40:56.771637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d88ab785935'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('roles', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('requirements', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_column('requirements')
        batch_op.drop_column('roles')

    # ### end Alembic commands ###
