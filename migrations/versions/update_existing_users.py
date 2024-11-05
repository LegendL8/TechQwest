"""Update existing users with default values

Revision ID: update_existing_users
Revises: add_not_null_constraints
Create Date: 2024-11-05 17:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'update_existing_users'
down_revision = 'add_not_null_constraints'
branch_labels = None
depends_on = None

def upgrade():
    # Update any existing NULL values to defaults
    op.execute(text("""
        UPDATE "user" 
        SET skill_level = COALESCE(skill_level, 1.0),
            correct_streak = COALESCE(correct_streak, 0),
            total_correct = COALESCE(total_correct, 0),
            total_attempted = COALESCE(total_attempted, 0)
    """))

def downgrade():
    pass
