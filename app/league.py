from app import app
import re

class League:

    def __init__(self, summoner):
        self.summoner = summoner
 
    def by_summoner(self, region, summoner_id):
        stats = self.watcher.league.by_summoner(region, summoner_id)
        ranked_solo = None
        for queueType in stats:
            if queueType.get('queueType') == "RANKED_SOLO_5x5":
                ranked_solo = queueType
        return ranked_solo

    
