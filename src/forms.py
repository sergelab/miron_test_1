from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField
from wtforms.validators import DataRequired


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
