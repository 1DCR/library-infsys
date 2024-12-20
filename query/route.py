import os
from flask import render_template, Blueprint, current_app, request, flash, redirect

from database.sql_provider import SQLProvider
from access import group_required
from query.model import query_execute


blueprint_query = Blueprint('query_bp', __name__, template_folder ='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
@group_required
def query_handle():
    action = request.args.get('action')
    query_info = current_app.config['query_config'][action]

    return render_template('query_form.html', query_name=action, query_info=query_info)


@blueprint_query.route('/', methods=['POST'])
@group_required
def query_index():
    action = request.args.get('action')
    user_input_data = request.form.to_dict()
    query_result = query_execute(current_app.config['db_config'], provider, action, user_input_data)

    if not query_result.status:
        flash(query_result.message, 'danger')
        return redirect(request.url)

    return render_template('dynamic.html', query_info=query_result.message, columns=query_result.schema, data=query_result.result)