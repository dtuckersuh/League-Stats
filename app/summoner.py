from app import app
from riotwatcher import RiotWatcher, ApiError
import json

class Summoner:

    watcher = RiotWatcher('RGAPI-6810e04d-cb23-471c-abae-a0bf45414b90')
    region = 'na1'

    def __init__(self, username):
        self.__username = username
        self.summoner = self.watcher.summoner.by_name(self.region, username)

    @property
    def username(self):
        return self.__username

    def getLevel(self):
        return self.summoner.get('summonerLevel')

    def getSummonerId(self):
        return self.summoner.get('id')

    def getAccountId(self):
        return self.summoner.get('accountId')

    # Return Champion Name and Mastery Points
    # Dict['Champion Name': Mastery Points]
    def getTopFiveChamps(self):
        with open("./en_US/champion.json", "r", encoding="utf8") as read_file:
            champ_file = json.load(read_file)
        champ_data = champ_file.get('data')
        top_five = {}
        champ_keys = []
        champ_names = []
        points = []
        mastery_list = self.watcher.champion_mastery.by_summoner(
            self.region, self.getSummonerId())
        # Get Champion Info for Top 5 champs in mastery points
        for i in range(5):
            champ_keys.append(mastery_list[i].get('championId'))
            points.append(mastery_list[i].get('championPoints'))

        # Search champion.json file for champion
        for key in champ_keys:
            champ_names.append(self.getChampion(key))

        # Fill dictionary with <Champion, Mastery Points> pairs
        for i in range(5):
            top_five[champ_names[i]] = points[i]
        return top_five
    
    # Return List[match_info]
    # match_info = champion:outcome
    def getMatchHistory(self):
        matches = self.getMatchlist()
        matchlist = []
        for match in matches:
            champion = match.get('champion')
            inner_match = self.watcher.match.by_id(self.region, match.get('gameId'))
            # List of players
            participantIdentities = inner_match.get('participantIdentities')
            # Get user id
            participant_id = None
            for participant in participantIdentities:
                if participant.get('player').get('summonerId') == self.getSummonerId():
                    participant_id = participant.get('participantId')

            # Get user stats
            participants = inner_match.get('participants')
            my_stats = {}
            for participant in participants:
                if participant.get('participantId') == participant_id:
                    my_stats = participant.get('stats')
            # Add match to list
            match_info = {'outcome': self.outcomeTranslate(my_stats),
                          'champion': self.getChampion(champion)}
            matchlist.append(match_info)
        return matchlist

    # Helper for Match History
    # Returns List[last 10 matches] which contain lane and gameId
    def getMatchlist(self):
        matchlist = self.watcher.match.matchlist_by_account(self.region, self.getAccountId(), end_index=10)
        matchlist = matchlist.get('matches')
        return matchlist

    def getChampion(self, id):
        with open("./en_US/champion.json", "r", encoding="utf8") as read_file:
            champ_file = json.load(read_file)
        champ_data = champ_file.get('data')
        # Search champion.json file for champion
        for champ in champ_data.items():
            attribute = champ[1]
            if (int(attribute.get('key'))) == id:
                return attribute.get('id')
        return None

    # Translates boolean game outcome to "Victory" or "Defeat"
    def outcomeTranslate(self, stats):
        if stats.get('win'):
            return 'Victory'
        else:
            return 'Defeat'
