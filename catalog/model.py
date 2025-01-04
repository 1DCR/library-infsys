from flask import session

from database.select import select_dict
from dataclasses import dataclass


@dataclass
class QueryResponse:
    result: list
    message: str
    status: bool


@dataclass
class CartResponse:
    message: str
    status: bool


def get_books(db_config, sql_provider):
    message = ''
    _sql = sql_provider.get('get_catalog_books.sql')
    result = select_dict(db_config, _sql)

    if not (total := len(result)):
        message = 'Кажется, каталог сейчас пуст...'
    else:
        message = f'Всего уникальных книг в каталоге: {total}'

    return QueryResponse(result=result, message=message, status=True)


def add_to_cart(db_config, sql_provider, data):
    """SESSION['cart'] = {'BOOKS' :
                                    {XX : {'TITLE' : BOOK_TITLE, 'AUTHOR' : NAME, 'PH' : PH_NAME, 'PRICE' : XXX, 'AMOUNT' : XX},
                                     XX : {'TITLE' : BOOK_TITLE, 'AUTHOR' : NAME, 'PH' : PH_NAME, 'PRICE' : XXX, 'AMOUNT' : XX},
                                      X : {                                 .      .      .                                   }
                                     },
                            'BOOKS_COUNT' : XX,
                            'TOTAL_PRICE' : XXXXX}"""

    message = ''
    catalog_book_id = data.get('catalog_book_id')
    _sql = sql_provider.get('get_catalog_book_info.sql', data)
    catalog_book_info = select_dict(db_config, _sql)

    if not len(catalog_book_info):
        message = 'Кажется, такой книги больше нет в каталоге. Или никогда не было...'
        return CartResponse(message=message, status=False)

    catalog_book_info = catalog_book_info[0]

    if 'cart' not in session:
        current_cart = {'books': {}, 'total_price': 0, 'books_count': 0}
    else:
        current_cart = session.get('cart')

    current_cart['books'][catalog_book_id] = {'title': catalog_book_info['title'],
                                              'author': catalog_book_info['author_name'],
                                              'publish_house': catalog_book_info['publish_house_name'],
                                              'price': catalog_book_info['price'],
                                              'amount': 1}
    current_cart['total_price'] += catalog_book_info['price']
    current_cart['books_count'] += 1

    session['cart'] = current_cart
    session.permanent = True

    return CartResponse(message=message, status=True)