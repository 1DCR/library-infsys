from flask import request
import json
from string import Template

from database.select import select_list
from dataclasses import dataclass


@dataclass
class QueryResponse:
    result: tuple
    schema: list
    message: str
    status: bool


def query_execute(db_config, user_input_data, sql_provider):
    message = ''
    action = request.args.get('action')
    sql_name = f'{action}.sql'
    _sql = sql_provider.get(sql_name, user_input_data)
    result, schema = select_list(db_config, _sql)

    if not len(result):
        message = 'По вашему запросу ничего не найдено'
        return QueryResponse(result=result, schema=schema, message=message, status=False)

    with open('data/queries_result_text.json', encoding='utf-8') as f:
        queries_result_text = json.load(f)
    message = Template(queries_result_text[action]).substitute(user_input_data)

    return QueryResponse(result=result, schema=schema, message=message, status=True)