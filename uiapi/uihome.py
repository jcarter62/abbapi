from abb import Sites, AllSitesMRR
from wmisdb import DB
import json

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
            if m is None:
                flow = 0.00
                state = ''
                timestamp = ''
                if s['abb']['urlname'] > '':
                    url_abb = s['abb']['url']
                if s['hmi']['urlname'] > '':
                    url_hmi = s['hmi']['url']
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


            # find any orders for this lateral/site.
            site_orders = 0.0
            for o in orders:
                if o['latname'].upper() == disp_name.upper():
                    site_orders = o['flow']

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
            }

            if not record['disp_abb']:
                record['flowfmt'] = '-.-'
            else:
                record['flowfmt'] = ('%10.2f' % record['flow']).lstrip(' ')  # + 'cfs'

            result.append(record)

        self.total_flow = 0.0
        for r in result:
            self.total_flow += r['flow']

        self.mrr_flow = 0.0
        for m in mrr:
            self.mrr_flow += m['tflow']

        return result

    def _get_mrr_(self, name, mrr):
        for m in mrr:
            if name == m['site']:
                return m
        return None
