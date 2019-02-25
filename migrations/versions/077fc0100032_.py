"""empty message

Revision ID: 077fc0100032
Revises: 
Create Date: 2019-02-25 18:39:51.613438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '077fc0100032'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('apikey', sa.String(length=120), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_apikey'), 'user', ['apikey'], unique=True)
    op.create_index(op.f('ix_user_date_created'), 'user', ['date_created'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reminder_date_created'), 'reminder', ['date_created'], unique=False)
    op.create_index(op.f('ix_reminder_description'), 'reminder', ['description'], unique=True)
    op.create_index(op.f('ix_reminder_item'), 'reminder', ['item'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reminder_item'), table_name='reminder')
    op.drop_index(op.f('ix_reminder_description'), table_name='reminder')
    op.drop_index(op.f('ix_reminder_date_created'), table_name='reminder')
    op.drop_table('reminder')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_date_created'), table_name='user')
    op.drop_index(op.f('ix_user_apikey'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###