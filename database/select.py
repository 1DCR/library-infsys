from pymysql import OperationalError

from database.DBcm import DBContextManager


def select_list(db_config : dict, _sql):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            schema = []
            for item in cursor.description:
                schema.append(item[0])
            return result, schema


def select_dict(db_config : dict, _sql):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def call_proc(db_config: dict, procedure_name, *args):
    result = ()
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            try:
                cursor.callproc(procedure_name, args)
                result = cursor.fetchall()
                return result
            except OperationalError as err:
                print(f"Error: {err}")
                raise err
