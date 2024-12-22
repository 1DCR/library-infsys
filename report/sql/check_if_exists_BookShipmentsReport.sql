SELECT *
FROM book_shipments_report
WHERE YEAR(report_date) = $year AND MONTH(report_date) = $month