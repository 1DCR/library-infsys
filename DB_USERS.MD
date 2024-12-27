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