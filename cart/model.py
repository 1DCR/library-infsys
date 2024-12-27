from flask import session
from dataclasses import dataclass

from database.select import select_dict, insert_order_transaction

MAX_AMOUNT = 20

@dataclass
class CartResponse:
    cart: dict
    books_count: int
    message: str
    status: bool

@dataclass
class OrderResponse:
    message: str
    status: bool


def get_cart_from_session():
    message = ''
    current_cart = session.get('cart', {})
    books_count = current_cart.get('books_count', 0)

    if not books_count:
        message = 'Ваша корзина пуста'
        return CartResponse(cart=current_cart, books_count=books_count, message=message, status=False)

    return CartResponse(cart=current_cart, books_count=books_count, message=message, status=True)


def change_amount(db_config, sql_provider, action_info):
    global MAX_AMOUNT
    message = ''
    catalog_book_id = action_info['book_id']
    action = action_info['action']
    current_cart = session.get('cart')


    if action == 'add':
        _sql = sql_provider.get('get_available_amount.sql', action_info)
        available_amount = select_dict(db_config, _sql)

        if current_cart['books'][catalog_book_id]['amount'] == MAX_AMOUNT:
            message = 'Больше добавить нельзя'
            return CartResponse(cart=current_cart, books_count=current_cart['books_count'], message=message, status=False)
        if current_cart['books'][catalog_book_id]['amount'] == available_amount[0]['available_amount']:
            message = 'Это все наши книги...'
            return CartResponse(cart=current_cart, books_count=current_cart['books_count'], message=message, status=False)

        current_cart['books'][catalog_book_id]['amount'] += 1
        current_cart['books_count'] += 1
        current_cart['total_price'] += current_cart['books'][catalog_book_id]['price']
    else:
        if current_cart['books'][catalog_book_id]['amount'] == 1:
            return remove_book(action_info)
        else:
            current_cart['books'][catalog_book_id]['amount'] -= 1
            current_cart['books_count'] -= 1
            current_cart['total_price'] -= current_cart['books'][catalog_book_id]['price']

    session['cart'] = current_cart

    return CartResponse(cart=current_cart, books_count=current_cart['books_count'], message=message, status=True)


def remove_book(action_info):
    catalog_book_id = action_info['book_id']
    current_cart = session.get('cart')

    current_cart['books_count'] -= current_cart['books'][catalog_book_id]['amount']
    current_cart['total_price'] -= (current_cart['books'][catalog_book_id]['price']
                                    * current_cart['books'][catalog_book_id]['amount'])
    current_cart['books'].pop(catalog_book_id)

    session['cart'] = current_cart

    message = 'Книга удалена из корзины'
    return CartResponse(cart=current_cart, books_count=current_cart['books_count'], message=message, status=True)


def clear_cart():
    session['cart'] = {'books': {}, 'total_price': 0, 'books_count': 0}
    return True


def create_order(db_config, sql_provider):
    message = ''
    current_cart_info = get_cart_from_session()
    current_cart = current_cart_info.cart
    books_count = current_cart_info.books_count

    if not books_count:
        message = 'Что-то не так. Невозможно оформить пустой заказ'
        return OrderResponse(message=message, status=False)

    for book_id in current_cart['books']:
        _sql_verify = sql_provider.get('get_available_amount.sql', {'book_id': book_id})
        available_amount = select_dict(db_config, _sql_verify)[0]['available_amount']
        if current_cart['books'][book_id]['amount'] > available_amount:
            book = current_cart['books'][book_id]
            title = book['title']
            author = book['author']
            ph = book['publish_house']
            price = book['price']

            message = f'Упс... Кажется книг {title} - {author}, {ph} ({price} ₽) стало меньше ({available_amount})'
            return OrderResponse(message=message, status=False)

    order_data = {'user_id': session['user_id'],
                  'user_name': session['user_name'],
                  'order_total_cost': current_cart['total_price'],
                  'order_book_count': books_count}

    books_list = []
    uniq_books_count = 0
    for book in current_cart['books']:
        book_dict = current_cart['books'][book].copy()
        book_dict['book_id'] = book
        books_list.append(book_dict)
        uniq_books_count += 1

    _sql_entry = sql_provider.get('insert_order.sql', order_data)
    _sql_content = sql_provider.gen_multi_insert_template('insert_order_content.sql', uniq_books_count, books_list)
    order_id = insert_order_transaction(db_config, _sql_entry, _sql_content)

    clear_cart()
    message = f'Заказ №{order_id} успешно оформлен!'
    return OrderResponse(message=message, status=True)