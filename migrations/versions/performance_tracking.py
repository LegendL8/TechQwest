"""Add user performance tracking with defaults

Revision ID: performance_tracking
Revises: 
Create Date: 2024-11-05 11:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'performance_tracking'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # First ensure the user table exists
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('skill_level', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('correct_streak', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_correct', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_attempted', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    op.drop_table('user')
