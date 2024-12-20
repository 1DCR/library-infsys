from datetime import datetime
from flask import request, current_app
from string import Template

from pymysql import OperationalError

from database.select import call_proc, select_list, select_dict
from dataclasses import dataclass


@dataclass
class ReportCreateResponse:
    message: str
    status: bool

@dataclass
class ReportGetResponse:
    result: tuple
    schema: list
    message: str
    status: bool


def is_month_ended(year, month):
    current_date = datetime.now()
    return current_date.year > year or (current_date.year == year and current_date.month > month)


def report_create(db_config, user_input_data, sql_provider):
    message = ''

    if not is_month_ended(user_input_data['year'], user_input_data['month']):
        message = 'Нельзя создавать отчет за еще не закончившийся период'
        return ReportCreateResponse(message=message, status=False)

    action = request.args.get('action')
    report_info = current_app.config['report_config'][action]

    check_if_exists_sql_name = report_info['check_if_exists_sql_name']
    _sql = sql_provider.get(check_if_exists_sql_name, user_input_data)
    check_result = select_dict(db_config, _sql)

    if len(check_result):
        message = f'Отчет за {user_input_data["month"]} меcяц {user_input_data["year"]} уже существует'
        return ReportCreateResponse(message=message, status=False)

    try:
        result = call_proc(db_config, report_info['procedure_name'], user_input_data['year'], user_input_data['month'])
    except OperationalError:
        message = 'Ошибка на стороне базы данных. Попробуйте позже'
        return ReportCreateResponse(message=message, status=False)

    message = f'Отчет за {user_input_data["month"]} меcяц {user_input_data["year"]} года успешно создан'
    return ReportCreateResponse(message=message, status=True)


def report_get(db_config, user_input_data, sql_provider):
    message = ''
    action = request.args.get('action')
    report_info = current_app.config['report_config'][action]
    sql_name = report_info['sql_name']
    _sql = sql_provider.get(sql_name, user_input_data)
    result, schema = select_list(db_config, _sql)

    if not len(result):
        message = f'Отчет за {user_input_data["month"]} меcяц {user_input_data["year"]} года не найден'
        return ReportGetResponse(result=result, schema=schema, message=message, status=False)

    report_result_text = report_info['result_text']
    message = Template(report_result_text).substitute(user_input_data)

    return ReportGetResponse(result=result, schema=schema, message=message, status=True)