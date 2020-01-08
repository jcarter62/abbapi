from abb import Sites, AllSitesMRR, SiteMRR
from wmisdata import Orders
import json
import arrow



class UISite:

    def __init__(self, sitename='') -> None:
        self.sitename = sitename
        self.data = {}
        self.load_site()

    def load_site(self):
        if self.sitename == '':
            return

        self.data = {}
        one_site = SiteMRR()
        one_site.set_name(self.sitename)
        if one_site.record is not None:
            self.data['flow'] = one_site.tflow()
            self.data['timestamp'] = one_site.local()
            self.data['data'] = one_site.record
        else:
            self.data['flow'] = None
            self.data['timestamp'] = None
            self.data['data'] = None

        self.data['site'] = self.sitename

        comb = []
        if one_site.record is not None:
            for row in one_site.record['flow']:
                tag = row['tag']
                cfs = row['value']
                acft = self.acft4tag(one_site.record['acft'], tag)
                comb.append({'tag': tag, 'acft': acft, 'cfs': cfs})

        self.data['combined'] = comb

        #
        orders = Orders()
        orders_detail = orders.order_detail(self.sitename)
        self.data['orders'] = orders_detail

    def acft4tag(self, rows, tag):
        for row in rows:
            if row['tag'] == tag:
                return row['value']
        return '-'
