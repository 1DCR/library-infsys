from flask import current_app
from string import Template

from database.select import select_dict
from dataclasses import dataclass


@dataclass
class QueryResponse:
    result: list
    message: str
    status: bool


def get_books(db_config, sql_provider):
    message = ''
    _sql = sql_provider.get('get_catalog_books.sql')
    result = select_dict(db_config, _sql)

    if not len(result):
        message = 'Кажется, каталог пуст...'
        return QueryResponse(result=result, message=message, status=False)

    return QueryResponse(result=result, message=message, status=True)