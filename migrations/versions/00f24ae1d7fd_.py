"""empty message

Revision ID: 00f24ae1d7fd
Revises: c6d0a059e004
Create Date: 2021-10-28 20:37:39.880226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f24ae1d7fd'
down_revision = 'c6d0a059e004'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('icon', sa.Integer(), nullable=True))
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    op.drop_column('user', 'icon')
    # ### end Alembic commands ###
