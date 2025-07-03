from flask import Blueprint, render_template

bp = Blueprint('dashboards', __name__, template_folder='templates')

@bp.route('/dash_general')
def dash_general():
    return render_template('dashboards/dash_general.html')

@bp.route('/dash_milk')
def dash_milk():
    return render_template('dashboards/dash_milk.html')

@bp.route('/dash_financial')
def dash_financial():
    return render_template('dashboards/dash_financial.html')