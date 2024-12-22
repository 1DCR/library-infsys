SELECT
    publish_house_id AS 'ID Издательства',
    publish_house_name AS 'Название Издательства',
    publish_house_phoneNumber AS 'Номер телефона',
    total_amount AS 'Общее число поставок',
    total_book_amount AS 'Всего книг поставлено',
    total_book_price AS 'Общая цена книг (руб.)'
FROM
	shipments_report_content src
JOIN
	shipments_report sr ON sr.id_shipments_report = src.shipments_report_id
WHERE
	YEAR(sr.report_date) = $year AND MONTH(sr.report_date) = $month