"""Fix skill level nulls and add property

Revision ID: fix_skill_level_nulls
Revises: fix_null_constraints
Create Date: 2024-11-05 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'fix_skill_level_nulls'
down_revision = 'fix_null_constraints'
branch_labels = None
depends_on = None

def upgrade():
    # Update any NULL values to defaults
    op.execute(text("""
        UPDATE "user" 
        SET skill_level = 1.0
        WHERE skill_level IS NULL
    """))
    
    # Make the column non-nullable with a default
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('skill_level',
                            existing_type=sa.Float(),
                            nullable=False,
                            server_default='1.0')

def downgrade():
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('skill_level',
                            existing_type=sa.Float(),
                            nullable=True,
                            server_default=None)
