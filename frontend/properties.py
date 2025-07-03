from flask import Blueprint, render_template

bp = Blueprint('properties', __name__, template_folder='templates')

@bp.route('/crop_overview')
def crop_overview():
    return render_template('properties/crop_overview.html')

@bp.route('/soil_analysis')
def soil_analysis():
    return render_template('properties/soil_analysis.html')

@bp.route('/area_and_crop')
def area_and_crop():
    return render_template('properties/area_and_crop.html')