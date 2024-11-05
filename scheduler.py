from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from models import Question, DailyQuestion, User, db
from sqlalchemy import func
import random

def select_daily_question():
    # Get all questions that haven't been used recently
    recent_questions = DailyQuestion.query.order_by(
        DailyQuestion.date.desc()
    ).limit(30).all()
    recent_ids = [dq.question_id for dq in recent_questions]
    
    # Get average user skill level
    avg_skill = db.session.query(func.avg(User.skill_level)).scalar() or 2.5
    
    # Select questions around the average skill level (±1 difficulty level)
    min_difficulty = max(1, int(avg_skill - 1))
    max_difficulty = min(5, int(avg_skill + 1))
    
    available_questions = Question.query.filter(
        ~Question.id.in_(recent_ids),
        Question.difficulty.between(min_difficulty, max_difficulty)
    ).all()
    
    if not available_questions:
        # Fallback to any question if no questions match criteria
        available_questions = Question.query.filter(
            ~Question.id.in_(recent_ids)
        ).all()
    
    if not available_questions:
        available_questions = Question.query.all()
    
    if available_questions:
        selected_question = random.choice(available_questions)
        
        new_daily = DailyQuestion(
            question_id=selected_question.id,
            date=datetime.utcnow().date()
        )
        db.session.add(new_daily)
        db.session.commit()

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        select_daily_question,
        'cron',
        hour=0,
        minute=0
    )
    scheduler.start()
    return scheduler
