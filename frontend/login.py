from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('login', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Aqui você pode adicionar a lógica de autenticação
        return redirect(url_for('dashboard'))  # Ajuste conforme sua rota de dashboard
    return render_template('login.html')

@bp.route('/dash_visitor')
def dash_visitor():
    return render_template('dash_visitor.html')