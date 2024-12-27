select
idPublish_house as 'ID', name as 'Название', address as 'Адрес', contactName as 'Имя представителя', phoneNumber as 'Телефон', foundYear as 'Год основания', dateContract as 'Дата заключения договора'
from publish_house
where address = '$city'