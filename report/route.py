import os
from flask import render_template, Blueprint, current_app, request, flash, redirect

from database.sql_provider import SQLProvider
from access import group_required
from report.model import report_create, report_get


blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@group_required
def report_handle():
    action = request.args.get('action')
    report_info = current_app.config['report_config'][action]

    return render_template('report_form.html', query_name=action, query_info=report_info)


@blueprint_report.route('/create', methods=['POST'])
@group_required
def report_create_index():
    user_input_data = request.form.to_dict()
    report_create_result = report_create(current_app.config['db_config'], provider, user_input_data)

    if not report_create_result.status:
        flash(report_create_result.message, 'success')  # TODO: исправить flash-категории
        redirect(request.url)
    else:
        flash(report_create_result.message, 'danger')
        redirect(request.url)


@blueprint_report.route('/view', methods=['POST'])
def report_view_index():
    user_input_data = request.form.to_dict()
    report_get_result = report_get(current_app.config['db_config'], provider, user_input_data)

    if not report_get_result.status:
        flash(report_get_result.message, 'danger')
        redirect(request.url)