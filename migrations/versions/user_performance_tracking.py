"""Add user performance tracking columns

Revision ID: user_performance_tracking
Revises: 
Create Date: 2024-11-05 11:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'user_performance_tracking'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('skill_level', sa.Float(), nullable=True, server_default='1.0'))
    op.add_column('user', sa.Column('correct_streak', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('user', sa.Column('total_correct', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('user', sa.Column('total_attempted', sa.Integer(), nullable=True, server_default='0'))

def downgrade():
    op.drop_column('user', 'skill_level')
    op.drop_column('user', 'correct_streak')
    op.drop_column('user', 'total_correct')
    op.drop_column('user', 'total_attempted')
