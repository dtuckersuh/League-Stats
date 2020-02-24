from riotwatcher import RiotWatcher, ApiError

class StaticData:
    def __init__(self, watcher, region):
        self.watcher = RiotWatcher('RGAPI-69aa00df-641a-490e-bc2b-ac4d40c9971b')
        self.region = 'na1'

    @property
    def watcher(self):
        return self.__watcher

    @property
    def region(self):
        return self.__region
 