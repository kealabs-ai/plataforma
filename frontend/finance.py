from flask import Blueprint, render_template

bp = Blueprint('finance', __name__, template_folder='templates')

@bp.route('/expenses_vs_revenues')
def expenses_vs_revenues():
    return render_template('finance/expenses_vs_revenues.html')