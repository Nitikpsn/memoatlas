from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, db
from ..forms.register_form import RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, send them to the workspace
    if current_user.is_authenticated:
        return redirect(url_for('notes.workspace'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # find the user by email
        user = User.query.filter_by(email=email).first()

        # check if user exists and password is correct
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))

        # log the user in
        login_user(user, remember=remember)

        # go to the page they were trying to visit, or the workspace
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('notes.workspace'))

    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('notes.workspace'))

    form = RegisterForm()
    if form.validate_on_submit():
        # check if email is already taken
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address already exists.', 'danger')
            return redirect(url_for('auth.register'))

        # check if username is already taken
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        # create the new user
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
