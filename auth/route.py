import os
from flask import render_template, Blueprint, current_app, request, redirect, flash

from database.sql_provider import SQLProvider
from auth.model import check_user

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET'])
def login_form():
    return render_template('login.html')


@blueprint_auth.route('/', methods=['POST'])
def auth_index():
    login_data = request.form.to_dict()
    auth_result = check_user(current_app.config['db_config'], provider, login_data)

    if auth_result.status:
        flash('Вы успешно авторизовались!', 'success')
        return redirect('/')
    else:
        flash(auth_result.error_message, 'danger')
        return redirect('/auth')