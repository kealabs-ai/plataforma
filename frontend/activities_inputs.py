from flask import Blueprint, render_template

bp = Blueprint('activities_inputs', __name__, template_folder='templates')

@bp.route('/agricultural_inputs')
def agricultural_inputs():
    return render_template('activities_inputs/agricultural_inputs.html')

@bp.route('/field_operations')
def field_operations():
    return render_template('activities_inputs/field_operations.html')