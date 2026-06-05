from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, User, Progress
from ..forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forest.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Wrong email or password.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if next_page and not urlparse(next_page).netloc:
            return redirect(next_page)
        return redirect(url_for('forest.dashboard'))

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('forest.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        if User.query.filter_by(email=email).first():
            flash('Email already in use.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        progress = Progress(user_id=user.id, xp=0, level=1)
        db.session.add(progress)

        db.session.commit()
        flash('Account created! Welcome to the forest.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('auth.login'))