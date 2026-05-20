from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
