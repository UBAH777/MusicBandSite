from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class CreateAccForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()], render_kw={
                       "placeholder": "Имя пользователя"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={
                             "placeholder": "Пароль"})
    email = StringField("Email: ", validators=[Email(), DataRequired()], render_kw={
                        "placeholder": "Электронная почта"})
    submit = SubmitField("создать аккаунт")


class LogInForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={
                       "placeholder": "Имя пользователя"})
    password = PasswordField(validators=[DataRequired()], render_kw={
                             "placeholder": "Пароль"})
    submit = SubmitField("войти")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                                             EqualTo('password')])
    submit = SubmitField('Save new password')


class LogoutButton(FlaskForm):
    submit = SubmitField('Выйти из учётной записи')
