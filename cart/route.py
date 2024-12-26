import os
from flask import render_template, Blueprint, current_app, request, flash, jsonify, session, redirect

from access import login_required
from database.sql_provider import SQLProvider
from cart.model import get_cart_from_session, change_amount, remove_book, clear, create_order


blueprint_cart = Blueprint('cart_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_cart.route('/', methods=['GET'])
@login_required
def cart_index():
    result = get_cart_from_session()
    return render_template('cart.html', books=result.cart.get('books', {}),
                           total_price=result.cart.get('total_price', {}), cart_count=result.cart_count, message=result.message)


@blueprint_cart.route('/change', methods=['POST'])
@login_required
def change_amount_handle():
    action_info = request.args.to_dict()
    status, message = change_amount(current_app.config['db_config'], provider, action_info)
    if not status:
        flash(message, 'warning')
    return redirect('/cart')


@blueprint_cart.route('/remove', methods=['POST'])
@login_required
def remove_handle():
    action_info = request.args.to_dict()
    remove_book(action_info)
    return redirect('/cart')


@blueprint_cart.route('/clear', methods=['POST'])
@login_required
def clear_handle():
    clear()
    return redirect('/cart')


@blueprint_cart.route('/order', methods=['POST'])
@login_required
def order_handle():
    create_order(current_app.config['db_config'], provider)
    return redirect('/cart')