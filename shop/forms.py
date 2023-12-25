from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from shop.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Emails already exists')

    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    password_repeat = PasswordField(label="Repeat Password",
                                    validators=[DataRequired(), Length(min=6), EqualTo('password')])

    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])

    submit = SubmitField(label="Login")


class ItemForm(FlaskForm):
    title = StringField(label="Title", validators=[Length(min=3, max=128), DataRequired()])
    description = TextAreaField(label="Description", validators=[Length(max=512)])
    price = DecimalField(label="Price", validators=[NumberRange(min=0), DataRequired()])

    submit = SubmitField(label="Add item")