import os
from string import Template

class SQLProvider:

    def __init__(self, file_path):
        self.scripts = {}
        for file in os.listdir(file_path):
            _sql = open(f'{file_path}/{file}', encoding='utf-8').read()
            self.scripts[file] = Template(_sql)

    def get(self, file, input_data={}):
        sql = self.scripts[file].safe_substitute(input_data)
        return sql

    def gen_multi_insert_template(self, file, repeat_count, input_data={}):
        """
        Генерирует SQL-INSERT с размноженными VALUES для дальнейшей подстановки.
        :param file: Имя SQL-файла.
        :param repeat_count: Количество повторений для VALUES.
        :param input_data: Данные для подстановки (опционально).
        :return: Шаблон сгенерированного SQL-запрос (Template).
        """
        sql = self.get(file)

        insert_statement, values_part = sql.split("VALUES", 1)
        values_part = Template(values_part.strip().rstrip(';'))

        repeated_values = ''

        repeated_values = ",".join(values_part.safe_substitute(input_values) for input_values in input_data)


        new_sql = f"{insert_statement}VALUES\n{repeated_values};"

        return new_sql