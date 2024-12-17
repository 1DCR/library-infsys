from database.select import select_list
from dataclasses import dataclass


@dataclass
class QueryResponse:
    result: tuple
    schema: list
    message: str
    status: bool


def query_execute(db_config, user_input_data, sql_provider, action):
    message = ''
    sql_name = f'{action}.sql'
    _sql = sql_provider.get(sql_name, user_input_data)
    result, schema = select_list(db_config, _sql)

    if not len(result):
        error_message = 'По вашему запросу ничего не найдено'
        return QueryResponse(result=result, schema=schema, message=message, status=False)

    return QueryResponse(result=result, schema=schema, message=message, status=True)
