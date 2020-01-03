from pymongo import MongoClient
import os
import json
from appsettings import Settings


class DbClient:

    def __init__(self):
        settings = Settings()
        self.host = settings.mongo_host
        self.port = settings.mongo_port
        uri = "mongodb://%s:%s" % (self.host, self.port)
        self.client = MongoClient(uri)
        self.db = self.client['abb']
        self.data = self.db['data']
        self.mrr = self.db['data_mrr']
        return


    def __del__(self):
        self.mrr = None
        self.data = None
        self.db = None
        self.client = None
        return


    def load_config(self):
        filename = os.path.join(os.path.abspath('.'), 'db.json')
        with open(filename, 'r') as f:
            db_obj = json.load(f)
        r1 = db_obj['host']
        r2 = db_obj['port']
        return r1, r2


    def close(self):
        self.mrr = None
        self.data = None
        self.db = None
        self.client = None
        return
