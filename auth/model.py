from flask import session, current_app
from re import match

from dataclasses import dataclass
from database.select import select_dict

from werkzeug.security import check_password_hash


@dataclass
class AuthResponse:
    error_message: str
    status: bool


def check_user(db_config, provider, login_data):
    error_message = ''
    if not(bool(match(r'^[a-zA-Z\d!#$%&?]{4,}$', login_data['password']))):
        error_message = ('Неверный формат пароля. Пароль должен быть не короче 4-х символов '
                         'и состоять только из букв латинского алфавита, цифр и символов !#$%&?')
        return AuthResponse(error_message=error_message, status=False)

    sql_name = 'external_user.sql' if login_data['role'] == 'reader' else 'internal_user.sql'

    _sql = provider.get(sql_name, login_data)
    user_data = select_dict(db_config['auth'], _sql)

    if not len(user_data):
        error_message = 'Пользователя с таким логином не существует'
        return AuthResponse(error_message=error_message, status=False)

    if not check_password_hash(user_data[0]['password_hash'], login_data['password']):
        error_message = 'Неверный пароль'
        return AuthResponse(error_message=error_message, status=False)

    session['user_id'] = user_data[0]['user_id']

    if login_data['role'] == 'reader':
        session['user_name'] = user_data[0]['name']
        session['user_group'] = login_data['role']
    else:
        session['user_group'] = user_data[0]['user_group']

    current_app.config['db_config_user'] = current_app.config['db_config'][session['user_group']]

    return AuthResponse(error_message=error_message, status=True)