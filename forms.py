from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email

class CreateAccForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()], render_kw={"placeholder": "Имя пользователя"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    email = StringField("Email: ", validators=[Email(), DataRequired()], render_kw={"placeholder": "Электронная почта"})
    submit = SubmitField("создать аккаунт")

class LogInForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Имя пользователя"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    submit = SubmitField("войти")