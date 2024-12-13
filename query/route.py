import os
from flask import render_template, Blueprint, current_app, request

from database.sql_provider import SQLProvider
from access import login_required, group_required
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
    user_input_data = request.form.to_dict()
    query_result = query_execute(current_app.config['db_config'], user_input_data, provider)

    return render_template('dynamic.html', query_name='publish_house', columns=query_result.schema, data=query_result.result)
