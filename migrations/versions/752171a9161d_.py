"""empty message

Revision ID: 752171a9161d
Revises: d6fb79c82e28
Create Date: 2021-11-02 16:07:49.725091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '752171a9161d'
down_revision = 'd6fb79c82e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('all_caught_pokemon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('all_caught_pokemon',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pokemon_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], name='all_caught_pokemon_pokemon_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='all_caught_pokemon_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='all_caught_pokemon_pkey')
    )
    # ### end Alembic commands ###
