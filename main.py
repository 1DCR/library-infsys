from flask import Flask, render_template, session, redirect, flash
import json

from auth.route import blueprint_auth
from query.route import blueprint_query
from access import login_required

app = Flask(__name__)

app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')

with open('data/db_config.json') as f:
    app.config['db_config'] = json.load(f)

with open('data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

@app.route('/')
def main_menu():
    is_authorized = False
    if 'user_group' in session:
        is_authorized = True
        user_role = session.get('user_group')
        message = f'Вы авторизованы как {user_role}.'
    else:
        message = 'Вам необходимо авторизоваться.'
    return render_template('main_menu.html', message=message, is_authorized=is_authorized)

@app.route('/logout')
@login_required
def logout_func():
    session.clear()
    flash('Вы вышли из системы')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)