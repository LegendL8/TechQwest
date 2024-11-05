from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Question, Category, db
from forms import QuestionForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('questions.daily'))

@bp.route('/')
def dashboard():
    questions_count = Question.query.count()
    categories = Category.query.all()
    return render_template('admin/dashboard.html',
                         questions_count=questions_count,
                         categories=categories)

@bp.route('/questions', methods=['GET', 'POST'])
def questions():
    form = QuestionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            correct_answer=form.correct_answer.data,
            wrong_answers=[ans.data for ans in form.wrong_answers],
            category_id=form.category.data,
            difficulty=form.difficulty.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully')
        return redirect(url_for('admin.questions'))
    
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template('admin/questions.html',
                         form=form,
                         questions=questions)
