from functools import wraps

from flask import session, redirect, request, current_app
from werkzeug.exceptions import Unauthorized, Forbidden


def unauthorized_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')

    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            raise Unauthorized

    return wrapper


def group_required(specify_endpoint=True):
    def wrapper(func):

        @wraps(func)
        def decorator(*args, **kwargs):
            full_endpoint = request.endpoint
            bp, action = full_endpoint.split('.')

            user_role = session.get('user_group', 'guest')
            access = current_app.config['db_access'][user_role]

            if not specify_endpoint:
                if bp in access:
                    return func(*args, **kwargs)
            else:
                access_list = access.get(bp, [])
                if 'all' in access_list or action in access_list:
                    return func(*args, **kwargs)

            if user_role == 'guest':
                raise Unauthorized
            else:
                raise Forbidden

        return decorator

    return wrapper
