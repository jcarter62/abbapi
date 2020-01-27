from abb import DbClient
from arrow import Arrow
import math


class Plot:

    def __init__(self, site: str = '') -> None:
        self.client = DbClient().client
        self.db = self.client['abb']
        self.dbdata = self.db['data']
        self.site = ''
        self.data = []
        self.days = 2

        if site > '':
            self.site = site
            self.set_name(site=site)

        return


    def data_obj(self, row) -> object:
        return {
            'state': row['state'],
            'local': row['local'],
            't0': row['t0'],
            'tflow': row['tflow']
        }

    def determine_max_min(self, rows) -> object:
        dmax = -999
        dmin = 999
        davg = 0
        total_flow = 0
        n = 0
        for r in rows:
            rflow = r['tflow']
            if rflow > dmax:
                dmax = rflow
            if rflow < dmin:
                dmin = rflow
            n = n + 1
            total_flow = total_flow + rflow
        if n > 0:
            davg = total_flow / n
        return {
            'max': round(dmax, 2),
            'min': round(dmin, 2),
            'avg': round(davg, 2),
            'n': n
        }

    def yesterday(self):
        days = self.days
        hours = -1 * (24 * days)
        return Arrow.utcnow().shift(hours=hours).timestamp

    def set_name(self, site: str = ''):
        self.site = site.lower()
        detail = []

        set1 = self.dbdata.find({'site': site, 't0': {'$gt': self.yesterday()}})
        qtrhrs = set1.distinct('qtrhr')

        result = []
        for qh in sorted(qtrhrs):
            #
            qset = self.dbdata.find({'site': site, 'qtrhr': qh})
            detail = []
            for row in qset:
                reading = self.data_obj(row)
                detail.append(reading)

            minmax = self.determine_max_min(detail)

            qtrhour = {
                'ts': Arrow.fromtimestamp(timestamp=qh).for_json(),
                'dt': Arrow.fromtimestamp(timestamp=qh),
                'min': minmax['min'],
                'max': minmax['max'],
                'avg': minmax['avg'],
            }
            result.append(qtrhour)

        #
        # Prepare for plot
        #
        dev_x = []
        dev_y = []
        labels = []
        for r in result:
            time = r['dt'].strftime('%y-%m-%d %H:%M')
            dev_x.append(time)
            labels.append(time)
            dev_y.append(r['avg'])

        n = labels.__len__()
        i = n-1
        div_factor = math.floor(n / 10)
        while i > 0:
            if i % div_factor != 0:
                labels[i] = ''
            i = i - 1

        result = {
            'x': dev_x,
            'y': dev_y,
            'labels': labels
        }
        self.data = result
