import pyodbc


class db_sql(object):

    __server = 'localhost'
    __database = 'SmartStorage'
    __connect = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};"
                               "Server="+__server+";"
                               "Database="+__database+";"
                               "Trusted_Connection=yes;"
                               )
    __link = __connect.cursor()

    def select_db(self, sql, data):
        db_sql.__link.execute(sql, data)
        result = db_sql.__link.fetchone()
        db_sql.__connect.commit()
        return result

    def update_db(self, sql, data):
        db_sql.__link.execute(sql, data)
        db_sql.__connect.commit()