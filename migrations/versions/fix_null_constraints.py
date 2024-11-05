"""Fix null constraints and add defaults

Revision ID: fix_null_constraints
Revises: remove_recruiter_functionality
Create Date: 2024-11-05 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'fix_null_constraints'
down_revision = 'remove_recruiter_functionality'
branch_labels = None
depends_on = None

def upgrade():
    # Update any NULL values to defaults
    op.execute(text("""
        UPDATE "user" 
        SET skill_level = COALESCE(skill_level, 1.0),
            correct_streak = COALESCE(correct_streak, 0),
            total_correct = COALESCE(total_correct, 0),
            total_attempted = COALESCE(total_attempted, 0)
        WHERE skill_level IS NULL 
           OR correct_streak IS NULL 
           OR total_correct IS NULL 
           OR total_attempted IS NULL
    """))
    
    # Add NOT NULL constraints
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('skill_level',
                            existing_type=sa.Float(),
                            nullable=False,
                            server_default='1.0')
        batch_op.alter_column('correct_streak',
                            existing_type=sa.Integer(),
                            nullable=False,
                            server_default='0')
        batch_op.alter_column('total_correct',
                            existing_type=sa.Integer(),
                            nullable=False,
                            server_default='0')
        batch_op.alter_column('total_attempted',
                            existing_type=sa.Integer(),
                            nullable=False,
                            server_default='0')

def downgrade():
    # Remove NOT NULL constraints and server defaults
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('skill_level',
                            existing_type=sa.Float(),
                            nullable=True,
                            server_default=None)
        batch_op.alter_column('correct_streak',
                            existing_type=sa.Integer(),
                            nullable=True,
                            server_default=None)
        batch_op.alter_column('total_correct',
                            existing_type=sa.Integer(),
                            nullable=True,
                            server_default=None)
        batch_op.alter_column('total_attempted',
                            existing_type=sa.Integer(),
                            nullable=True,
                            server_default=None)
