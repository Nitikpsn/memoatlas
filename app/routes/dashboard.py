from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
# @login_required  <-- Comment this out for 5 minutes just to test if the page looks good!
def index():
    return render_template('dashboard/dashboard.html')