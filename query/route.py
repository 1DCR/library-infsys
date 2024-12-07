import os
from dataclasses import dataclass
from flask import render_template, Blueprint, current_app, request
from database.select import select_list
from database.sql_provider import SQLProvider
from access import login_required, group_required

blueprint_query = Blueprint('query_bp', __name__, template_folder = 'templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@dataclass
class QueryResponse:
    result: tuple
    error_message: str
    status: bool


@blueprint_query.route('/', methods=['GET'])
@group_required
def query_input_form():
    return render_template('publish_house_contract_input.html')

@blueprint_query.route('/')
#@group_required
def query_index(db_config, user_input_data, sql_provider):
    error_message = ''
    if 'prod_category' not in user_input_data:
        print('user_input_data=', user_input_data)
        error_message = 'category not found'
        result = ()
        return QueryResponse(result, error_message=error_message, status=False)
    _sql = sql_provider.get('publish_house_contract.sql', prod_category=user_input_data['prod_category'])
    print('sql=', _sql)
    result, schema = select_list(db_config, _sql)
    return QueryResponse(result=result, error_message=error_message, status=True)

@blueprint_query.route('/', methods=['POST'])
#@group_required
def product_result_handle():
    user_input_data = request.form
    user_info_result = query_index(current_app.config['db_config'], user_input_data, provider)
    if user_info_result.status:
        products = user_info_result.result
        if len(products) == 0:
            return "Нет результатов"
        prod_title = products[0][0] if products[0] else 'Результаты'
        return render_template('dynamic.html', prod_title=prod_title, products=products)
    else:
        return f'Что-то не так со вводом: {user_info_result.error_message}'
