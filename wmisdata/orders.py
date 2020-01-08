import pyodbc
from appsettings import Settings


class Orders:

    def __init__(self) -> None:
        self.settings = Settings()
        super().__init__()

    def _conn_str_(self, ):
        server = self.settings.sqlserver
        database = self.settings.sqldb
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

    def del1stchar(self, s):
        result = s
        while result[0] == '0':
            result = result[1:]
        return result

    def order_summary(self, lateral):
        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        lat = self.del1stchar(lateral)
        cmd = 'exec sp_abb_orders_detail @lateral=\'%s\', @summary=1;' % lat

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
        lat = self.del1stchar(lateral)
        cmd = 'exec sp_abb_orders_detail @lateral=\'%s\' ;' % lat
        total_row = None
        last_row = None
        total_flow = 0.0

        try:
            rows = cursor.execute(cmd)
            for row in rows:
                rowdata = self._extract_row(row)
                if rowdata['isactive'] == '1':
                    total_flow = total_flow + float(rowdata['flow'])
                last_row = rowdata
                result.append(rowdata)
        except Exception as e:
            print(str(e))

        if last_row is not None:
            total_row = last_row.copy()
            total_row['account'] = 'Total'
            total_row['account_name'] = ''
            total_row['turnout_id'] = ''
            total_row['fieldname'] = ''
            total_row['flow'] = total_flow
            total_row['isactive'] = ''
            result.append(total_row)

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

