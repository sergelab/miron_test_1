from flask import Flask, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from typing import Optional

from .forms import CalcForm


app = Flask(__name__)
app.config.from_mapping(
	DEBUG=False,
	SECRET_KEY='dev111',
	DEBUG_TB_PROFILER_ENABLED=True
)
DebugToolbarExtension(app)


@app.route('/')
def index():
	return render_template("index.j2")


@app.route('/more')
def more():
	return render_template("more.j2")


@app.route('/page')
def page_1():
	return render_template("page_1.j2")


def calculation(a: int, b: int, op: int) -> Optional[int]:
	print(a, b)
	if op == 1:
		return a * b
	elif op == 2:
		if b == 0:
			flash('На 0 делить нельзя', 'danger')
			return None
		return a / b
	elif op == 3:
		return a + b
	elif op == 4:
		return a - b
	else:
		flash('Такая операция не обнаружена')
		return None


@app.route('/calculator', methods=['GET', 'POST'])
def calc():
	form = CalcForm()
	result = None

	if form.validate_on_submit():
		result = calculation(form.a.data, form.b.data, form.op.data)

	return render_template("calc.j2", form=form, result=result)
