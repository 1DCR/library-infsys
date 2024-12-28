from flask import current_app
from string import Template

from database.select import select_list
from dataclasses import dataclass


@dataclass
class QueryResponse:
    result: tuple
    schema: list
    message: str
    status: bool


def query_execute(db_config, sql_provider, user_input_data):
    message = ''
    query_name = user_input_data['query_name']
    query_info = current_app.config['query_config'][query_name]
    _sql = sql_provider.get(query_info['sql_name'], user_input_data)

    result, schema = select_list(db_config, _sql)

    if not len(result):
        message = 'По вашему запросу ничего не найдено'
        return QueryResponse(result=result, schema=schema, message=message, status=False)

    query_result_text = query_info['result_text']
    message = Template(query_result_text).substitute(user_input_data)

    return QueryResponse(result=result, schema=schema, message=message, status=True)