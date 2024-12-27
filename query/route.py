import os
from flask import render_template, Blueprint, current_app, request, flash, redirect, url_for

from database.sql_provider import SQLProvider
from access import group_required
from query.model import query_execute


blueprint_query = Blueprint('query_bp', __name__, template_folder ='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
@group_required()
def query_handle():
    action = request.args.get('action')

    return render_template('query_form.html', query_name=action,
                           query_info=current_app.config['query_config'][action])


@blueprint_query.route('/view', methods=['POST'])
@group_required()
def query_view():
    user_input_data = request.form.to_dict()
    query_result = query_execute(current_app.config['db_config'], provider, user_input_data)

    if not query_result.status:
        flash(query_result.message, 'danger')
        return redirect(url_for('query_bp.query_handle') + '/?action=' + user_input_data['query_name'])

    return render_template('dynamic_query.html', query_result_message=query_result.message,
                           columns=query_result.schema, data=query_result.result)