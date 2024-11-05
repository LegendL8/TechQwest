from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FieldList
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class QuestionForm(FlaskForm):
    text = TextAreaField('Question Text', validators=[DataRequired()])
    correct_answer = TextAreaField('Correct Answer', validators=[DataRequired()])
    wrong_answers = FieldList(TextAreaField('Wrong Answer'), min_entries=3)
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    difficulty = SelectField('Difficulty', 
                           choices=[(i, str(i)) for i in range(1, 6)],
                           coerce=int,
                           validators=[DataRequired()])
