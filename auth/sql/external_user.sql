SELECT user_id, name, login, password_hash
FROM external_user
WHERE login = '$login'
