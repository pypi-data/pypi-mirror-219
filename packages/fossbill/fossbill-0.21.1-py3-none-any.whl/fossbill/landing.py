from flask import (
    Blueprint, g, render_template
)

bp = Blueprint('landing', __name__)

@bp.route('/')
def home():
    if g.user is None:
        return welcome()
    else:
        return dashboard()

def dashboard():
    return render_template('landing/dashboard.html')

def welcome():
    return render_template('landing/welcome.html')
