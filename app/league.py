from app import app

class League:

    def __init__(self, summoner):
        self.summoner = summoner

    def by_summoner(self, region, summoner_id):
        stats = self.watcher.league.by_summoner(region, summoner_id)
        return stats[0]

    
