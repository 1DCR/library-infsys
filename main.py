from flask import Flask, render_template, session, redirect, flash, url_for
import json

from auth.route import blueprint_auth
from query.route import blueprint_query
from report.route import blueprint_report
from catalog.route import blueprint_catalog
from cart.route import blueprint_cart
from access import login_required


app = Flask(__name__)

#app.debug = True
#app.config["EXPLAIN_TEMPLATE_LOADING"] = True

app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_catalog, url_prefix='/catalog')
app.register_blueprint(blueprint_cart, url_prefix='/cart')

with open('data/db_config.json') as f:
    app.config['db_config'] = json.load(f)

with open('data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

with open('data/query_config.json', encoding='utf-8') as f:
    app.config['query_config'] = json.load(f)

with open('data/report_config.json', encoding='utf-8') as f:
    app.config['report_config'] = json.load(f)

app.config['db_config_user'] = app.config['db_config']['guest']

@app.route('/')
def main_menu():
    if 'user_group' in session:
        if not (session['user_group'] == 'reader' or session['user_group'] == 'guest'):
            user = session.get('user_group')
            return render_template('internal_main_menu.html', user=user,
                               queries=app.config['query_config'], reports=app.config['report_config'])
    else:
        session['user_group'] = 'guest'

    return redirect('/catalog')


@app.route('/logout')
@login_required
def logout_func():
    session.clear()
    flash('Вы вышли из системы', 'warning')
    return redirect('/')


@app.errorhandler(403)
def internal_error(e):
    return render_template('403.html')


@app.errorhandler(404)
def internal_error(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
