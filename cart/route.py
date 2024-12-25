import os
from flask import render_template, Blueprint, current_app, request, flash, jsonify, session
from pyexpat.errors import messages

from access import login_required
from database.sql_provider import SQLProvider
from cart.model import get_books_from_session


blueprint_cart = Blueprint('cart_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_cart.route('/', methods=['GET'])
@login_required
def cart_index():
    result = get_books_from_session()
    return render_template('cart.html', books=result.books['books'],
                           total_price=result.books['total_price'], message=result.message)


