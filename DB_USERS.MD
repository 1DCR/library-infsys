**ПОЛЬЗОВАТЕЛИ И ИХ ПРИВЕЛЕГИИ В БАЗЕ ДАННЫХ**

ПОЛЬЗОВАТЕЛИ:

    CREATE USER 'director'@'localhost' IDENTIFIED BY 'director_password';
    CREATE USER 'head_librarian'@'localhost' IDENTIFIED BY 'head_librarian_password';
    CREATE USER 'librarian'@'localhost' IDENTIFIED BY 'librarian_password';
    CREATE USER 'external_user'@'localhost' IDENTIFIED BY 'external_user_password';
    CREATE USER 'auth'@'localhost' IDENTIFIED BY 'auth_password';
    CREATE USER 'guest'@'localhost' IDENTIFIED BY 'guest_password';

ПРИВЕЛЕГИИ:

    GRANT SELECT ON labn1.book_shipments_report TO 'director'@'localhost';
    GRANT SELECT ON labn1.book_shipments_report_content TO 'director'@'localhost';
    GRANT SELECT ON labn1.shipments_report TO 'director'@'localhost';
    GRANT SELECT ON labn1.shipments_report_content TO 'director'@'localhost';
    

    GRANT SELECT ON labn1.book_shipments_report TO 'head_librarian'@'localhost';
    GRANT SELECT ON labn1.book_shipments_report_content TO 'head_librarian'@'localhost';
    GRANT SELECT ON labn1.shipments_report TO 'head_librarian'@'localhost';
    GRANT SELECT ON labn1.shipments_report_content TO 'head_librarian'@'localhost';
    GRANT EXECUTE ON PROCEDURE labn1.GenerateShipmentsReport TO 'head_librarian'@'localhost';
    GRANT EXECUTE ON PROCEDURE labn1.GenerateBookShipmentsReport TO 'head_librarian'@'localhost';
    
    
    GRANT SELECT ON labn1.book TO 'librarian'@'localhost';
    GRANT SELECT ON labn1.book_set TO 'librarian'@'localhost';
    GRANT SELECT ON labn1.publish_house TO 'librarian'@'localhost';
    GRANT SELECT ON labn1.user_order TO 'librarian'@'localhost';
    GRANT SELECT ON labn1.user_order_content TO 'librarian'@'localhost';
    

    GRANT INSERT ON labn1.user_order TO 'external_user'@'localhost';
    GRANT INSERT ON labn1.user_order_content TO 'external_user'@'localhost';
    GRANT SELECT ON labn1.library_catalog TO 'external_user'@'localhost';
    GRANT SELECT ON labn1.book TO 'external_user'@'localhost';
    GRANT SELECT ON labn1.publish_house TO 'external_user'@'localhost';
    

    GRANT SELECT ON labn1.internal_user TO 'auth'@'localhost';
    GRANT SELECT ON labn1.external_user TO 'auth'@'localhost';


    GRANT SELECT ON labn1.library_catalog TO 'guest'@'localhost';
    GRANT SELECT ON labn1.book TO 'guest'@'localhost';
    GRANT SELECT ON labn1.publish_house TO 'guest'@'localhost';

ПРОЦЕДУРА 1:

    DELIMITER $$
    CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerateBookShipmentsReport`(
        IN report_year INT,
        IN report_month INT
    )
    BEGIN
        DECLARE report_id INT;
        DECLARE report_date DATE;
    
        SET report_date = MAKEDATE(report_year, 1) + INTERVAL (report_month - 1) MONTH;
    	
    	INSERT INTO book_shipments_report (report_date)
    	VALUES (report_date);
    
    	SET report_id = LAST_INSERT_ID();
    
    	INSERT INTO book_shipments_report_content (book_id, book_title, book_authorName, book_genre, book_price, book_total_amount, book_report_id)
    	SELECT 
    		bsl.bookId,
            b.title,
            b.authorName,
            b.genre,
            bsl.price,
            SUM(bsl.amount) AS totalAmount,
    		report_id
    	FROM 
    		book_set_list bsl
    	JOIN 
    		book_set bs ON bsl.bookSet = bs.idBook_set
    	JOIN
    		book b ON bsl.bookId = b.idBook
    	WHERE 
    		MONTH(bs.bs_date) = report_month AND YEAR(bs.bs_date) = report_year
    	GROUP BY 
    		bsl.bookId, b.title, b.authorName, b.genre, bsl.price;
    END$$
    DELIMITER ;

ПРОЦЕДУРА 2:

	DELIMITER $$
	CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerateShipmentsReport`(
	    IN report_year INT,
	    IN report_month INT
	)
	BEGIN
	    DECLARE report_id INT;
	    DECLARE report_date DATE;
	
	    SET report_date = MAKEDATE(report_year, 1) + INTERVAL (report_month - 1) MONTH;
	    
	    INSERT INTO shipments_report (report_date)
	    VALUES (report_date);
	
	    SET report_id = LAST_INSERT_ID();
	    
	    INSERT INTO shipments_report_content (
	        publish_house_id, 
	        publish_house_name, 
	        publish_house_phoneNumber, 
	        total_amount, 
	        total_book_amount, 
	        total_book_price, 
	        shipments_report_id
	    )
	    SELECT
	        ph.idPublish_house AS publish_house_id,
	        ph.name AS publish_house_name,
	        ph.phoneNumber AS publish_house_phoneNumber,
	        COUNT(DISTINCT bs.idBook_set) AS total_amount,
	        SUM(bsl.amount) AS total_book_amount,
	        SUM(bsl.price * bsl.amount) AS total_book_price,
	        report_id
	    FROM 
	        book_set bs
	    JOIN 
	        book_set_list bsl ON bs.idBook_set = bsl.bookSet
	    JOIN 
	        publish_house ph ON bs.provider = ph.idPublish_house
	    WHERE 
	        MONTH(bs.bs_date) = report_month AND YEAR(bs.bs_date) = report_year
	    GROUP BY 
	        ph.idPublish_house, ph.name, ph.phoneNumber;
	END$$
	DELIMITER ;

ПРОЦЕДУРА 3:

	DELIMITER $$
	CREATE DEFINER=`root`@`localhost` PROCEDURE `updateLib`(input_date DATE)
	BEGIN
		DECLARE b_id, b_count, b_price INTEGER;
		DECLARE done integer DEFAULT 0;
		DECLARE C1 CURSOR FOR 
			SELECT bookId, amount, price FROM book_set_list bsl
			JOIN book_set bs ON bs.idBook_set = bsl.bookSet
			WHERE bs.bs_date=input_date;
		DECLARE EXIT HANDLER FOR SQLSTATE '02000' SET done=1;
		OPEN C1;
	    WHILE done = 0 DO
	        FETCH C1 INTO b_id, b_count, b_price;
	        IF EXISTS (SELECT 1 FROM library_catalog WHERE lBook = b_id AND price = b_price) THEN
	            UPDATE library_catalog SET amount = amount + b_count
	            WHERE lBook = b_id AND price = b_price;
	        ELSE
	            INSERT INTO library_catalog (lBook, price, amount) VALUES (b_id, b_price, b_count);
	        END IF;
	    END WHILE;
	
	END$$
	DELIMITER ;

