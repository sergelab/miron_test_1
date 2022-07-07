from flask import abort, Flask, render_template, flash
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


def get_products():
	return [
		{'id': 1, 'title': 'Товар 1', 'description': 'Описание 1'},
		{'id': 2, 'title': 'Товар 2', 'description': 'Описание 2'},
		{'id': 3, 'title': 'Товар 3', 'description': 'Описание 3'},
		{'id': 4, 'title': 'Товар 4', 'description': 'Описание 4'},
		{'id': 5, 'title': 'Товар 5', 'description': 'Описание 5ч'}
	]


@app.route('/')
def index():
	_products = get_products()

	return render_template("index.j2", products=_products)


@app.route('/product/<int:product_id>')
def product_card(product_id: int):
	_products = get_products()
	_product = None

	for _p in _products:
		if _p.get('id') == product_id:
			_product = _p

			break

	if not _product:
		abort(404)

	return render_template("product_card.j2", product=_product)


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


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.j2'), 404
