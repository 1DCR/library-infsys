SELECT
    title,
    authorName AS author_name,
    name AS publish_house_name,
    price,
    amount AS available_amount
FROM library_catalog
JOIN book ON library_catalog.book_id = book.idBook
JOIN publish_house ON library_catalog.publish_house_id = publish_house.idPublish_house
WHERE idLibrary = '$catalog_book_id'