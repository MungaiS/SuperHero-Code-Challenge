"""Initial migration

Revision ID: 34c003e68e38
Revises: 
Create Date: 2024-04-09 12:29:49.044582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c003e68e38'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hero_powers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strength', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('super_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('powers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('powers')
    op.drop_table('heroes')
    op.drop_table('hero_powers')
    # ### end Alembic commands ###
