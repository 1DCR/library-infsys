SELECT
    idorder AS '№ заказа',
    order_total_cost AS 'Стоимость заказа',
    order_book_count AS 'Количество книг',
    order_date AS 'Дата заказа'
FROM
    user_order
WHERE
    user_id = '$user_id'