import os
from flask import render_template, Blueprint, current_app, request, flash, redirect, url_for

from database.sql_provider import SQLProvider
from access import group_required
from report.model import report_create, report_get


blueprint_report = Blueprint('report_bp', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@group_required()
def report_handle():
    action = request.args.get('action')

    return render_template('report_form.html', report_name=action,
                           report_info=current_app.config['report_config'][action])


@blueprint_report.route('/create', methods=['POST'])
@group_required(specify_request=True)
def report_create_index():
    user_input_data = request.form.to_dict()
    report_create_result = report_create(current_app.config['db_config_user'], provider, user_input_data)

    if not report_create_result.status:
        flash(report_create_result.message, 'danger')
        return redirect(url_for('report_bp.report_handle') + '/?action=' + user_input_data['report_name'])

    flash(report_create_result.message, 'success')
    return redirect(url_for('report_bp.report_handle') + '/?action=' + user_input_data['report_name'])


@blueprint_report.route('/view', methods=['POST'])
@group_required(specify_request=True)
def report_view_index():
    user_input_data = request.form.to_dict()
    report_get_result = report_get(current_app.config['db_config_user'], provider, user_input_data)

    if not report_get_result.status:
        flash(report_get_result.message, 'danger')
        return redirect(url_for('report_bp.report_handle') + '/?action=' + user_input_data['report_name'])

    return render_template('dynamic_report.html', report_result_message=report_get_result.message,
                           columns=report_get_result.schema, data=report_get_result.result)
