SELECT
    book_id AS 'ID книги',
    title AS 'Название',
    publish_house_name AS 'Название издательства',
    book_price AS 'Цена книги'
FROM
    user_order_content
JOIN book ON user_order_content.book_id = book.idBook
WHERE
    order_id = '$order_id'