import pyodbc

from settings import Settings


class DB:

    def __init__(self) -> None:
        self.settings = Settings()
        super().__init__()

    def _conn_str_(self, ):
        server = self.settings.server
        database = self.settings.db
        driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
        return driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;'

    def orders_summary(self):
        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = 'exec sp_abb_orders_detail @summary=1;'

        try:
            for row in cursor.execute(cmd):
                result.append(self._extract_row(row))
        except Exception as e:
            print(str(e))

        return result

    def order_summary(self, lateral):
        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = 'exec sp_abb_orders_detail @lateral=\'%s\', @summary=1;' % lateral

        try:
            for row in cursor.execute(cmd):
                result.append(self._extract_row(row))
        except Exception as e:
            print(str(e))

        return result

    def order_detail(self, lateral):
        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = 'exec sp_abb_orders_detail @lateral=\'%s\' ;' % lateral

        try:
            for row in cursor.execute(cmd):
                result.append(self._extract_row(row))
        except Exception as e:
            print(str(e))

        return result

    def _extract_row(self, row):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r
