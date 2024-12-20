import os
from string import Template

class SQLProvider:

    def __init__(self, file_path):
        self.scripts = {}
        for file in os.listdir(file_path):
            _sql = open(f'{file_path}/{file}', encoding='utf-8').read()
            self.scripts[file] = Template(_sql)

    def get(self, file, input_data):
        sql = self.scripts[file].substitute(input_data)
        return sql