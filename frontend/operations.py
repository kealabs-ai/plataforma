from flask import Blueprint, render_template

bp = Blueprint('operations', __name__, template_folder='templates')

@bp.route('/milk_production')
def milk_production():
    return render_template('operations/milk_production.html')