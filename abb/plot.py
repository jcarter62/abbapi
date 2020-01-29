from abb import DbClient


class Plot:

    def __init__(self, site: str = '') -> None:
        self.client = DbClient().client
        self.db = self.client['abb']
        self.data = {}
        self.dbdata = self.db['graph']
        self.site = site
        self.load_plot()
        return


    def load_plot(self):
        collection = self.db['graph']
        records = collection.find({"_id": self.site})
        if records.count() > 0:
            self.data = records[0]
        return

