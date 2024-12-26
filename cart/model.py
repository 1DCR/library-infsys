from flask import session
from dataclasses import dataclass

from database.select import select_dict

MAX_AMOUNT = 20

@dataclass
class CartResponse:
    cart: dict
    cart_count: int
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

def clear():
    session['cart'] = {'books': {}, 'total_price': 0}
    return True

def create_order(db_config, sql_provider):
    pass