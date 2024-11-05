"""Add recruiter suggestions

Revision ID: add_recruiter_suggestions
Revises: update_existing_users
Create Date: 2024-11-05 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_recruiter_suggestions'
down_revision = 'update_existing_users'
branch_labels = None
depends_on = None

def upgrade():
    # Add is_recruiter column to user table
    op.add_column('user', sa.Column('is_recruiter', sa.Boolean(), nullable=True))
    
    # Create suggested_question table
    op.create_table('suggested_question',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('correct_answer', sa.Text(), nullable=False),
        sa.Column('wrong_answers', sa.JSON(), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('suggested_question')
    op.drop_column('user', 'is_recruiter')
