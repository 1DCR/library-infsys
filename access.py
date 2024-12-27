from functools import wraps

from flask import session, redirect, request, current_app, jsonify, render_template


def unauthorized_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/catalog')
    return wrapper


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return 'Вам необходимо авторизоваться для работы с данным функционалом', 401
    return wrapper


def group_required(specify_request=False):

    def wrapper(func):

        @wraps(func)
        def decorator(*args, **kwargs):
            if 'user_group' in session:
                user_role = session.get('user_group')
                access = current_app.config['db_access']

                action = request.endpoint
                if not specify_request:
                    action = action.split('.')[0]

                if user_role in access and action in access[user_role]:
                    return func(*args, **kwargs)
                else:
                    return render_template('no_permission.html'), 403

            else:
                return 'Вам необходимо авторизоваться для работы с данным функционалом', 401

        return decorator

    return wrapper
