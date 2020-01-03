from .sitemrr import SiteMRR
from .sites import Sites


class AllSitesMRR:

    def __init__(self):
        self.sites = Sites()
        self.data = []
        sitemrr = SiteMRR()
        for s in self.sites.names:
            sitemrr.set_name(name=s)
            if sitemrr.record is None:
                pass
            else:
                self.data.append(sitemrr.record)

        self.data.sort(key=lambda x: x['site'])

        return
