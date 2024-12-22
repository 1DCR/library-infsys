SELECT
    book_id AS 'ID книги',
    book_title AS 'Название книги',
    book_authorName AS 'Автор книги',
    book_genre AS 'Жанр книги',
    book_price AS 'Цена книги (руб.)',
    book_total_amount AS 'Общее количество книг'
FROM
	book_shipments_report_content bsrc
JOIN
	book_shipments_report bsr ON bsr.id_book_report = bsrc.book_report_id
WHERE
	YEAR(bsr.report_date) = $year AND MONTH(bsr.report_date) = $month