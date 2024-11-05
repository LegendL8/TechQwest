from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import Question, DailyQuestion, UserResponse, db

bp = Blueprint('questions', __name__)

@bp.route('/')
@bp.route('/daily')
@login_required
def daily():
    today = datetime.utcnow().date()
    daily_q = DailyQuestion.query.filter_by(date=today).first()
    if not daily_q:
        return render_template('questions/daily.html', question=None)
    
    question = daily_q.question
    user_response = UserResponse.query.filter_by(
        user_id=current_user.id,
        question_id=question.id
    ).first()
    
    return render_template('questions/daily.html',
                         question=question,
                         user_response=user_response)

@bp.route('/answer', methods=['POST'])
@login_required
def answer():
    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    
    question = Question.query.get_or_404(question_id)
    is_correct = answer == question.correct_answer
    
    response = UserResponse(
        user_id=current_user.id,
        question_id=question_id,
        answer=answer,
        is_correct=is_correct
    )
    
    # Update user's skill level based on performance
    current_user.update_skill_level(is_correct, question.difficulty)
    
    db.session.add(response)
    db.session.commit()
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question.correct_answer
    })

@bp.route('/history')
@login_required
def history():
    responses = UserResponse.query.filter_by(
        user_id=current_user.id
    ).order_by(UserResponse.created_at.desc()).all()
    return render_template('questions/history.html', 
                         responses=responses,
                         skill_level=current_user.skill_level)

@bp.route('/learning-path')
@login_required
def learning_path():
    # Get category performance statistics
    category_performance = current_user.get_category_performance()
    
    # Get recommended questions
    recommended_questions = current_user.get_recommended_questions()
    
    return render_template('questions/learning_path.html',
                         category_performance=category_performance,
                         recommended_questions=recommended_questions)
