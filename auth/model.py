from flask import session
from dataclasses import dataclass
from database.select import select_dict
from re import match


@dataclass
class AuthResponse:
    error_message: str
    status: bool


def check_user(db_config, provider, login_data):
    error_message = ''
    if not(bool(match(r'^[a-zA-Z\d!#$%&?]{4,}$', login_data['password']))):
        error_message = 'Неверный формат пароля. Пароль должен быть не короче 4-х символов и состоять только из букв латинского алфавита, цифр и символов !#$%&?'
        return AuthResponse(error_message=error_message, status=False)

    _sql = provider.get('internal_user.sql', login=login_data['login'], password=login_data['password'])
    user_data = select_dict(db_config, _sql)

    if not user_data:
        error_message = 'Неверный логин или пароль'
        return AuthResponse(error_message=error_message, status=False)

    session['user_id'] = user_data[0]['user_id']
    session['user_group'] = user_data[0]['user_group']

    return AuthResponse(error_message='', status=True)