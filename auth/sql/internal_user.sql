SELECT user_id, user_group, login, password_hash
FROM internal_user
WHERE login = '$login'
