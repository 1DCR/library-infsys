select idBook_set as 'ID', bs_date as 'Дата', totalCost as 'Общая сумма поставки (руб.)'
from book_set
join publish_house ph on provider = ph.idPublish_house
where name = '$publish_house_name'