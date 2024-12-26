from flask import Flask, render_template, session, redirect, flash
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


@app.route('/')
def main_menu():
    is_authorized = 'user_id' in session
    user = session.get('user_group') or session.get('user_name')

    if 'user_group' in session:
        return render_template('internal_main_menu.html', user=user, is_authorized=is_authorized,
                           queries=app.config['query_config'], reports=app.config['report_config'])

    return redirect('/catalog')


@app.route('/logout')
@login_required
def logout_func():
    session.clear()
    flash('Вы вышли из системы', 'warning')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
