SELECT user_id, user_group, login
FROM internal_user
WHERE login = '$login' AND password = '$password';
