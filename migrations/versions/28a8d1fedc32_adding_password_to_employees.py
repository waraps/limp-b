"""Adding password to employees

Revision ID: 28a8d1fedc32
Revises: 5e47735d1f02
Create Date: 2021-03-17 18:57:29.279654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28a8d1fedc32'
down_revision = '5e47735d1f02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
