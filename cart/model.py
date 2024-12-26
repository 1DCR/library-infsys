from flask import session
from dataclasses import dataclass

from pyexpat.errors import messages

from database.select import select_dict, insert_order_transaction

MAX_AMOUNT = 20

@dataclass
class CartResponse:
    cart: dict
    cart_count: int
    message: str
    status: bool

@dataclass
class OrderResponse:
    message: str
    status: bool


def get_cart_from_session():
    message = ''
    current_cart = session.get('cart', {})

    if not len(current_cart):
        message = 'Ваша корзина пуста'
        return CartResponse(cart=current_cart, cart_count=0, message=message, status=False)

    cart_count = 0
    for book_id in current_cart['books']:
        cart_count += current_cart['books'][book_id]['amount']

    return CartResponse(cart=current_cart, cart_count=cart_count, message=message, status=True)


def change_amount(db_config, sql_provider, action_info):
    global MAX_AMOUNT
    catalog_book_id = action_info['book_id']
    action = action_info['action']
    current_cart = session.get('cart')

    if action == 'add':
        _sql = sql_provider.get('get_available_amount.sql', action_info)
        available_amount = select_dict(db_config, _sql)

        if current_cart['books'][catalog_book_id]['amount'] == MAX_AMOUNT:
            return False, 'Больше добавить нельзя'
        if current_cart['books'][catalog_book_id]['amount'] == available_amount[0]['available_amount']:
            return False, 'Это все наши книги...'

        current_cart['books'][catalog_book_id]['amount'] += 1
        current_cart['total_price'] += current_cart['books'][catalog_book_id]['price']
    else:
        if current_cart['books'][catalog_book_id]['amount'] == 1:
            return remove_book(action_info), ''
        else:
            current_cart['books'][catalog_book_id]['amount'] -= 1
            current_cart['total_price'] -= current_cart['books'][catalog_book_id]['price']

    session['cart'] = current_cart

    return True, ''


def remove_book(action_info):
    catalog_book_id = action_info['book_id']
    current_cart = session.get('cart')

    current_cart['total_price'] -= (current_cart['books'][catalog_book_id]['price']
                                    * current_cart['books'][catalog_book_id]['amount'])
    current_cart['books'].pop(catalog_book_id)

    session['cart'] = current_cart

    return True


def clear_cart():
    session['cart'] = {'books': {}, 'total_price': 0}
    return True


def create_order(db_config, sql_provider):
    message = ''
    current_cart_info = get_cart_from_session()
    current_cart = current_cart_info.cart
    cart_count = current_cart_info.cart_count

    if not (uniq_books_count := len(current_cart['books'])):
        message = 'Что-то не так. Невозможно оформить пустой заказ'
        return OrderResponse(message=message, status=False)

    order_data = {'user_id': session['user_id'],
                  'user_name': session['user_name'],
                  'order_total_cost': current_cart['total_price'],
                  'order_book_count': cart_count}

    books_list = []
    for book in current_cart['books']:
        temp = current_cart['books'][book].copy()
        temp['book_id'] = book
        books_list.append(temp)

    _sql_entry = sql_provider.get('insert_order.sql', order_data)
    _sql_content = sql_provider.gen_multi_insert_template('insert_order_content.sql', uniq_books_count, books_list)
    order_id = insert_order_transaction(db_config, _sql_entry, _sql_content)

    clear_cart()
    message = f'Заказ №{order_id} успешно оформлен!'
    return OrderResponse(message=message, status=True)