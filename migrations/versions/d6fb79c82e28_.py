"""empty message

Revision ID: d6fb79c82e28
Revises: be980a27016b
Create Date: 2021-11-02 15:12:25.158244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6fb79c82e28'
down_revision = 'be980a27016b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('base_xp', sa.String(length=50), nullable=True),
    sa.Column('hp', sa.String(length=50), nullable=True),
    sa.Column('defense', sa.String(length=50), nullable=True),
    sa.Column('attack', sa.String(length=50), nullable=True),
    sa.Column('url', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('all_caught_pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('all_caught_pokemon')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
