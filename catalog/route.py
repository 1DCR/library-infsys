import os
from flask import render_template, Blueprint, current_app, request, flash, jsonify, session

from access import login_required
from database.sql_provider import SQLProvider
from catalog.model import get_books, add_to_cart


blueprint_catalog = Blueprint('catalog_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_catalog.route('/', methods=['GET'])
def catalog_index():
    query_result = get_books(current_app.config['db_config'], provider)
    cart_books_ids = list(map(int, session.get('cart', {}).get('books', {}).keys()))

    return render_template('catalog.html',
                           books=query_result.result,
                           total_books_message=query_result.message,
                           cart_books_ids=cart_books_ids)


@blueprint_catalog.route('/', methods=['POST'])
@login_required
def add_to_cart_handler():
    data = request.form.to_dict()
    result = add_to_cart(current_app.config['db_config'], provider, data)

    if not result.status:
        flash(result.message, 'danger')
        return jsonify(result), 400

    return render_template('success_button.html', catalog_book_id=data.get('catalog_book_id'))
