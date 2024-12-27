import os
from flask import render_template, Blueprint, current_app, request, flash, redirect

from access import group_required
from database.sql_provider import SQLProvider
from cart.model import get_cart_from_session, change_amount, remove_book, clear_cart, create_order


blueprint_cart = Blueprint('cart_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_cart.route('/', methods=['GET'])
@group_required()
def cart_index():
    result = get_cart_from_session()

    return render_template('cart.html', books=result.cart.get('books', {}),
                           total_price=result.cart.get('total_price', {}), cart_count=result.books_count, message=result.message)


@blueprint_cart.route('/change', methods=['POST'])
@group_required()
def change_amount_handle():
    action_info = request.args.to_dict()
    result = change_amount(current_app.config['db_config_user'], provider, action_info)

    if not result.message == '':
        flash(result.message, 'warning')

    return redirect('/cart')


@blueprint_cart.route('/remove', methods=['POST'])
@group_required()
def remove_handle():
    action_info = request.args.to_dict()
    result = remove_book(action_info)
    flash(result.message, 'warning')

    return redirect('/cart')


@blueprint_cart.route('/clear', methods=['POST'])
@group_required()
def clear_handle():
    clear_cart()
    flash('Корзина очищена', 'warning')

    return redirect('/cart')


@blueprint_cart.route('/order', methods=['POST'])
@group_required()
def order_handle():
    order_result = create_order(current_app.config['db_config_user'], provider)

    if not order_result.status:
        flash(order_result.message, 'danger')
    else:
        flash(order_result.message, 'success')

    return redirect('/cart')