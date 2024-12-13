from database.select import select_list
from dataclasses import dataclass

@dataclass
class QueryResponse:
    result: tuple
    schema: list
    error_message: str
    status: bool


def query_execute(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('publish_house_contract.sql', user_input_data)
    print('sql=', _sql)
    result, schema = select_list(db_config, _sql)
    return QueryResponse(result=result, schema=schema, error_message=error_message, status=True)
