from flask import Blueprint, render_template
from flask_login import login_required
from models import Question, UserResponse, Category, db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/')
@login_required
def index():
    # Overall question performance
    question_stats = db.session.query(
        Question,
        func.count(UserResponse.id).label('total_attempts'),
        func.sum(func.cast(UserResponse.is_correct, db.Integer)).label('correct_attempts')
    ).join(UserResponse).group_by(Question.id).all()
    
    # Category performance
    category_stats = db.session.query(
        Category.name,
        func.count(UserResponse.id).label('total_attempts'),
        func.sum(func.cast(UserResponse.is_correct, db.Integer)).label('correct_attempts')
    ).join(Question, Question.category_id == Category.id)\
     .join(UserResponse)\
     .group_by(Category.name).all()
    
    # Daily success rate for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_stats = db.session.query(
        func.date(UserResponse.created_at).label('date'),
        func.count(UserResponse.id).label('total_attempts'),
        func.sum(func.cast(UserResponse.is_correct, db.Integer)).label('correct_attempts')
    ).filter(UserResponse.created_at >= thirty_days_ago)\
     .group_by(func.date(UserResponse.created_at))\
     .order_by(func.date(UserResponse.created_at)).all()
    
    return render_template('analytics/index.html',
                         question_stats=question_stats,
                         category_stats=category_stats,
                         daily_stats=daily_stats)
