import os
from flask import render_template, Blueprint, current_app, request, flash, redirect
import json
from string import Template

from database.sql_provider import SQLProvider
from access import group_required
from query.model import query_execute


blueprint_query = Blueprint('query_bp', __name__, template_folder = 'templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
@group_required
def query_handle():
    action = request.args.get('action')

    if action == 'publish_house_contract':
        return render_template('publish_house_contract.html')
    elif action == 'publish_house_city':
        return render_template('publish_house_city.html')
    elif action == 'publish_house_batch':
        return render_template('publish_house_batch.html')


@blueprint_query.route('/', methods=['POST'])
#@group_required
def query_index():
    action = request.args.get('action')
    user_input_data = request.form.to_dict()
    query_result = query_execute(current_app.config['db_config'], user_input_data, provider, action)

    if not query_result.status:
        flash(query_result.message, 'danger')
        return redirect(request.url)

    with open('data/queries_result_text.json', encoding='utf-8') as f:
        queries_result_text = json.load(f)
    query_info = Template(queries_result_text[action]).substitute(user_input_data)

    return render_template('dynamic.html', query_info=query_info, columns=query_result.schema, data=query_result.result)