"""auth session

Revision ID: 8db36ad8d0f2
Revises: 224ef692d5ec
Create Date: 2023-06-12 15:57:27.580021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8db36ad8d0f2'
down_revision = '224ef692d5ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authsession',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('last_activity', sa.DateTime(), nullable=False),
    sa.Column('host', sa.String(), nullable=True),
    sa.Column('real_ip', sa.String(), nullable=True),
    sa.Column('accept_language', sa.String(), nullable=True),
    sa.Column('user_agent', sa.String(), nullable=True),
    sa.Column('detected_os', sa.String(), nullable=True),
    sa.Column('firebase_token', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authsession_id'), 'authsession', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_authsession_id'), table_name='authsession')
    op.drop_table('authsession')
    # ### end Alembic commands ###
