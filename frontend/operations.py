from flask import Blueprint, render_template

bp = Blueprint('operations', __name__, template_folder='templates')

@bp.route('/milk_production')
def milk_production():
    return render_template('operations/milk_production.html')

@bp.route('/beef_cattle')
def beef_cattle():
    return render_template('operations/beef_cattle.html')

@bp.route('/floriculture')
def floriculture():
    return render_template('operations/floriculture.html')

@bp.route('/landscaping')
def landscaping():
    return render_template('operations/landscaping.html')