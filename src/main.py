from flask import abort, current_app, Flask, redirect, url_for, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from typing import Optional, Union
from sqlalchemy import Column, Integer, Text
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import CalcForm, RegistrationForm, LoginForm


app = Flask(__name__)
app.config.from_mapping(
	# DEBUG=False,
	SECRET_KEY='dev111',
	DEBUG_TB_PROFILER_ENABLED=True,
	SQLALCHEMY_TRACK_MODIFICATIONS=False,
	DEBUG_TB_INTERCEPT_REDIRECTS=False,
	SQLALCHEMY_DATABASE_URI='postgresql://localhost:5432/miron_shop_test'
)
DebugToolbarExtension(app)
db = SQLAlchemy(app)
lm = LoginManager(app)


lm.login_view = 'login'


class Product(db.Model):
	__tablename__ = 'products'

	id = Column(Integer(), primary_key=True)
	title = Column(Text(), nullable=False)
	description = Column(Text())


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = Column(Integer(), primary_key=True)
	pw_hash = Column(Text, nullable=False, default='<unset>')
	username = Column(Text, nullable=False, unique=True)
	name = Column(Text)

	@property
	def password(self):
		return self.pw_hash

	@password.setter
	def password(self, value):
		if value:
			self.pw_hash = generate_password_hash(value)
		else:
			self.pw_hash = '<unset>'

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)


@lm.user_loader
def user_loader(user_id: int):
	return User.query.filter(User.id == user_id).one_or_none()


def get_products():
	return Product.query.all()


@app.route('/')
def index():
	_products = get_products()

	return render_template("index.j2", products=_products)


@app.route('/product/<int:product_id>')
def product_card(product_id: int):
	_product = Product.query.filter(Product.id == product_id).one_or_none()

	if not _product:
		abort(404)

	return render_template("product_card.j2", product=_product)


@app.route('/more')
def more():
	return render_template("more.j2")


@app.route('/page')
def page_1():
	return render_template("page_1.j2")


def calculation(a: int, b: int, op: int) -> Optional[Union[int, float]]:
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
@login_required
def calc():
	form = CalcForm()
	result = None

	if form.validate_on_submit():
		result = calculation(form.a.data, form.b.data, form.op.data)

	return render_template("calc.j2", form=form, result=result)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.j2'), 404


@app.route('/user/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(**request.args)

	if form.validate_on_submit():
		_user = User.query.filter(User.username == form.username.data).one_or_none()
		if not _user:
			flash('Пользователь не найден', 'danger')
			return redirect(url_for('login'))

		if _user.check_password(form.password.data) and login_user(_user):
			return redirect(form.next.data or url_for('index'))
		else:
			flash('Неверный пароль', 'danger')

	return render_template('login.j2', form=form)


@app.route('/user/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/user/registration', methods=['GET', 'POST'])
def registration():
	form = RegistrationForm()

	if form.validate_on_submit():
		obj = User()
		db.session.add(obj)
		form.populate_obj(obj)

		try:
			db.session.commit()
		except Exception as e:
			current_app.logger.exception(e)
			db.session.rollback()
		else:
			return redirect(url_for('index'))

	return render_template("registration.j2", form=form)


@app.route('/user/profile', methods=['GET', 'POSt'])
def profile():
	pass
