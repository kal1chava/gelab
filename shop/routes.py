from flask import render_template, flash, url_for, redirect
from shop.forms import RegisterForm, LoginForm, ItemForm
from shop import app, db
from shop.models import User, Item
from flask_login import login_user, logout_user, current_user


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('items'))
    else:
        for field, error in form.errors.items():
            flash(f'{field} - {error}')

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('items'))
        else:
            flash('Wrong Credentials')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("successfully logged out")
    return redirect(url_for("login"))


@app.route("/add-item", methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            item = Item(title=form.title.data,
                        description=form.description.data,
                        price=form.price.data,
                        owner=current_user.id)

            db.session.add(item)
            db.session.commit()
            return redirect(url_for('items'))
    else:
        flash('Login required')
        return redirect(url_for('login'))
    return render_template('item.html', form=form)


@app.route('/')
@app.route('/items')
def items():
    items_list = Item.query.all()

    return render_template('items.html', items=items_list)


@app.route('/user-items/<int:user_id>')
def user_items(user_id):
    if not current_user.is_authenticated:
        flash('Login required')
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    return render_template('items.html', items=user.items, user=user)