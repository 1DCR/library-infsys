SELECT
    idLibrary AS catalog_book_id,
    price,
    authorName,
    title,
    genre,
    name as publish_house_name
FROM library_catalog
JOIN book on library_catalog.book_id = book.idBook
JOIN publish_house on library_catalog.publish_house_id = publish_house.idPublish_house