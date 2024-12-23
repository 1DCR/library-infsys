import os
from flask import render_template, Blueprint, current_app, request, flash, redirect, url_for

from database.sql_provider import SQLProvider
from catalog.model import get_books


blueprint_catalog = Blueprint('catalog_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_catalog.route('/', methods=['GET'])
def catalog_index():
    query_result = get_books(current_app.config['db_config'], provider)
    # books = [
    #     {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман"},
    #     {"title": "Преступление и наказаниеееееееееееееееееееееееееееееееееееееееееееееееееееееее", "author": "Федор Достоевский", "genre": "Роман"},
    #     {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Фантастика"},
    #     {"title": "Отцы и дети", "author": "Иван Тургенев", "genre": "Классика"}
    #     ]
    return render_template('catalog.html', books=query_result.result)