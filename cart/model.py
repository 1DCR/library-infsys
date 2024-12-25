from flask import session
from dataclasses import dataclass


@dataclass
class Response:
    books: dict
    message: str
    status: bool


def get_books_from_session():
    message = ''
    books = session.get('cart', default={})

    if not len(books):
        message = 'Ваша корзина пуста'
        return Response(books=books, message=message, status=False)

    return Response(books=books, message=message, status=True)

