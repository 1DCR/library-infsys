from pymysql import connect
from pymysql.err import OperationalError

class DBContextManager:

    def __init__(self, db_config: dict):
        self.conn = None
        self.cursor = None
        self.config = db_config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            err_code, err_msg = err.args
            if err_code == 1049:
                print(f"Error: Database '{self.config['db']}' does not exist")
            elif err_code == 1045:
                print(f"Error: Access denied for user '{self.config['user']}': {err_msg}")
            elif err_code == 2003:
                print(f"Error: Cannot connect to server '{self.config['host']}': {err_msg}")
            elif err_code == 1054:
                print(f"Error: Unknown column: {err_msg}")
            else:
                print(f"OperationalError: {err_code} - {err_msg}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        if exc_type:
            print(exc_type)
            print(exc_val)
            raise OperationalError(exc_val)
        return True

