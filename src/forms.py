from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class CalcForm(FlaskForm):
	class Meta:
		csrf = False

	a = DecimalField('Число А')  #, validators=[DataRequired()])
	b = DecimalField('Число Б')  #, validators=[DataRequired()])
	op = SelectField(
		'Что сделать?',
		choices=[
			(1, 'Умножить'),
			(2, 'Разделить'),
			(3, 'Сложить'),
			(4, 'Вычесть'),
		],
		coerce=int
	)


class RegistrationForm(FlaskForm):
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password_2 = PasswordField('Еще раз пароль', validators=[
		DataRequired(), EqualTo('password', message='Пароли не совпадают')
	])
	name = StringField('Имя')


class LoginForm(FlaskForm):
	next = HiddenField()
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
