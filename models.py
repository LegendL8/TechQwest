from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    responses = db.relationship('UserResponse', backref='user', lazy=True)
    # Performance tracking fields with non-nullable constraints and defaults
    _skill_level = db.Column('skill_level', db.Float, nullable=False, default=1.0, server_default='1.0')
    correct_streak = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    total_correct = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    total_attempted = db.Column(db.Integer, nullable=False, default=0, server_default='0')

    @property
    def skill_level(self):
        # Always return a valid float, defaulting to 1.0 if NULL
        return float(self._skill_level if self._skill_level is not None else 1.0)

    @skill_level.setter
    def skill_level(self, value):
        self._skill_level = float(value if value is not None else 1.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_skill_level(self, is_correct, question_difficulty):
        """Update user's skill level based on their performance"""
        self.total_attempted += 1
        if is_correct:
            self.total_correct += 1
            self.correct_streak += 1
            # Increase skill level if performing well at current level
            if self.correct_streak >= 3 and self.skill_level < 5.0:
                self.skill_level = min(5.0, self.skill_level + 0.5)
        else:
            self.correct_streak = 0
            # Decrease skill level if question was too difficult
            if question_difficulty > self.skill_level + 1:
                self.skill_level = max(1.0, self.skill_level - 0.25)

    def get_category_performance(self):
        """Get performance statistics for each category"""
        category_stats = db.session.query(
            Category.name,
            func.count(UserResponse.id).label('total_attempts'),
            func.sum(func.cast(UserResponse.is_correct, db.Integer)).label('correct_attempts')
        ).join(Question, Question.category_id == Category.id)\
         .join(UserResponse, UserResponse.question_id == Question.id)\
         .filter(UserResponse.user_id == self.id)\
         .group_by(Category.name)\
         .all()
        
        return {
            stat.name: {
                'success_rate': (stat.correct_attempts / stat.total_attempts * 100 
                               if stat.total_attempts > 0 else 0),
                'total_attempts': stat.total_attempts,
                'correct_attempts': stat.correct_attempts
            }
            for stat in category_stats
        }

    def get_recommended_questions(self, limit=5):
        """Get personalized question recommendations based on weak areas"""
        # Get category performance
        category_stats = self.get_category_performance()
        
        # Find categories with low performance or no attempts
        weak_categories = []
        for category in Category.query.all():
            stats = category_stats.get(category.name, {
                'success_rate': 0,
                'total_attempts': 0
            })
            if stats['success_rate'] < 70 or stats['total_attempts'] < 3:
                weak_categories.append(category.id)
        
        # If no weak categories found, include all categories
        if not weak_categories:
            weak_categories = [c.id for c in Category.query.all()]
        
        # Get questions from categories around user's skill level
        recommended = Question.query.filter(
            Question.category_id.in_(weak_categories),
            Question.difficulty.between(
                max(1, int(self.skill_level - 1)),
                min(5, int(self.skill_level + 1))
            )
        ).order_by(func.random()).limit(limit).all()
        
        return recommended

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    questions = db.relationship('Question', backref='category', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    wrong_answers = db.Column(db.JSON, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responses = db.relationship('UserResponse', backref='question', lazy=True)

class DailyQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)
    question = db.relationship('Question')

class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
