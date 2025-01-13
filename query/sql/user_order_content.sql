SELECT
    user_order_content.book_id AS 'ID книги в каталоге',
    title AS 'Название',
    publish_house_name AS 'Название издательства',
    book_price AS 'Цена книги',
    book_amount AS 'Количество'
FROM
    user_order_content
JOIN library_catalog ON user_order_content.book_id = library_catalog.idLibrary
JOIN book ON library_catalog.book_id = book.idBook
WHERE
    order_id = '$order_id'