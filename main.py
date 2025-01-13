import json

from flask import Flask, render_template, session, redirect, flash

from access import login_required
from auth.route import blueprint_auth
from cart.route import blueprint_cart
from catalog.route import blueprint_catalog
from query.route import blueprint_query
from report.route import blueprint_report


app = Flask(__name__)

# app.debug = True
# app.config["EXPLAIN_TEMPLATE_LOADING"] = True

app.secret_key = 'Estimated time to guess is 283 million trillion trillion years'

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


@app.route('/')
def main_menu():
    user_group = session.get('user_group', 'guest')

    if user_group == 'guest' or user_group == 'reader':
        return redirect('/catalog')

    return render_template('internal_main_menu.html',
                           user=user_group,
                           queries=app.config['query_config'],
                           reports=app.config['report_config'])


@app.route('/logout')
@login_required
def logout_func():
    session.clear()
    flash('Вы вышли из системы', 'warning')
    return redirect('/')


@app.errorhandler(401)
def internal_error(e):
    return render_template('401.html'), 401


@app.errorhandler(403)
def internal_error(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def internal_error(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
