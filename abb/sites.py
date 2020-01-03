import os
import json
from typing import List, Any


class Sites:
    names: List[Any]
    sites: object

    def __init__(self):
        filename = os.getenv('DATAFILE')
        with open(filename, 'r') as f:
            self.sites = json.load(f)

        self.names = list()
        for s in self.sites['sites']:
            if s['abb']['urlname'] > '':
                this_name = s['name']
                self.names.append(this_name)
        return

    def find(self, by_address=None, by_abbname=None, by_sortname=None):
        '''
        :param by_address:
        :param by_abbname:
        :param by_sortname:
        :return: object
        '''
        result = None
        if by_address != None:
            url = 'http://' + by_address
            for s in self.sites['sites']:
                if s['abb']['address'] == url:
                    result = s
                    break
        elif by_abbname != None:
            for s in self.sites['sites']:
                if by_abbname.upper() == s['abb']['urlname'].upper():
                    result = s
                    break
        elif by_sortname != None:
            for s in self.sites['sites']:
                if by_sortname.upper() == s['name'].upper():
                    result = s
                    break
        return result


