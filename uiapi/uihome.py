from abb import Sites, AllSitesMRR
from wmisdb import DB
import json
import arrow


class UIHome:
    '''
    UIHome provides data required for the UI Home view.  The reason for this class is to
    abstract the complex data generation, due to multiple sources, and interpretation of the
    different data sources.

    Args:
        None

    '''

    def __init__(self):
        self.total_flow = 0.0
        self.mrr_flow = 0.0
        self.data = self.get_data()

    def get_data(self):

        result = []
        sites = Sites().sites['sites']
        mrr = AllSitesMRR().data
        db = DB()
        orders = db.orders_summary()

        for s in sites:
            name = s['name']
            disp_name = name
            if s['abb']['urlname'] == '':
                disp_name = s['hmi']['urlname']

            m = self._get_mrr_(name=name, mrr=mrr)
            url = ''
            url_abb = ''
            url_hmi = ''
            site_age = 'age0'
            if m is None:
                flow = 0.00
                state = ''
                timestamp = ''
                if s['abb']['urlname'] > '':
                    url_abb = s['abb']['url']
                if s['hmi']['urlname'] > '':
                    url_hmi = s['hmi']['url']
                tags = None
            else:
                flow = m['tflow']
                state = m['state']
                timestamp = m['local']
                # url = './site/' + s['abb']['urlname']
                url = './site/' + s['name']
                if s['hmi']['urlname'] > '':
                    url_hmi = s['hmi']['url']
                    disp_name = s['hmi']['urlname']
                if s['abb']['urlname'] > '':
                    url_abb = s['abb']['url']
                    disp_name = s['abb']['urlname']
                site_age = self.calc_age(m)
                #
                # Determine tags A,B,..D
                #
                tags = {'a':0, 'b':0, 'c':0, 'd':0}
                for f in m['flow']:
                    tag = f['tag'].lower()
                    if tag != 'total':
                        tags[tag] = 1


            # find any orders for this lateral/site.
            site_orders = 0.0
            for o in orders:
                if o['latname'].upper() == disp_name.upper():
                    if isinstance(o['flow'], type('str')):
                        flo = round(float(o['flow']), 2)
                    else:
                        flo = round(o['flow'], 2)
                    site_orders = flo

            record = {
                'name': name,
                'dispname': disp_name,
                'flow': flow,
                'flowfmt': '',
                'orders': site_orders,
                'state': state,
                'time': timestamp,
                'url': url,
                'url_abb': url_abb,
                'url_hmi': url_hmi,
                'disp_abb': (s['abb']['urlname'] > ''),
                'disp_hmi': (s['hmi']['urlname'] > ''),
                'age': site_age,
                'orders_vs_flow': '',
                'tags': tags
            }

            if not record['disp_abb']:
                record['flowfmt'] = '-.-'
            else:
                record['flowfmt'] = ('%10.2f' % record['flow']).lstrip(' ')  # + 'cfs'

            ovf = ''
            if record['flowfmt'] != '-.-':
                flowval = float(record['flowfmt'])
                orders_val = float(record['orders'])
                of_diff = flowval - orders_val
                if of_diff < 1.0:
                    ovf = 'good'
                else:
                    ovf = 'error'

            record['orders_vs_flow'] = ovf

            result.append(record)

        self.total_flow = 0.0
        for r in result:
            self.total_flow += r['flow']

        # reformat total_flow, showing only 0.XX instead of 0.XXXXXXX
        #
        self.total_flow = round(self.total_flow, 2)

        self.mrr_flow = 0.0
        for m in mrr:
            self.mrr_flow += m['tflow']

        self.mrr_flow = round(self.mrr_flow, 2)

        return result

    def calc_age(self, record) -> str:
        if record is None:
            result = ''
        else:
            current_time = arrow.utcnow().timestamp
            age = current_time - record['t0']
            if age < 120:
                result = '0'
            elif age < 240:
                result = '1'
            elif age < 360:
                result = '2'
            elif age < 480:
                result = '3'
            else:
                result = '4'
            result = 'age' + result

        return result

    def _get_mrr_(self, name, mrr):
        for m in mrr:
            if name == m['site']:
                return m
        return None
