from app import app
from .league import League
from .champion import Champion
from riotwatcher import RiotWatcher, ApiError
import json
import os
import re

class Summoner:

    watcher = RiotWatcher('RGAPI-415b6f2d-617e-4c86-85fc-de87ed865ac8')
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

    def getProfileIcon(self):
        id = self.summoner.get('profileIconId')
        with open("./en_US/profileicon.json", "r", encoding="utf8") as read_file:
            icons = json.load(read_file)
        icon_data = icons.get('data')
        profile_icon = icon_data.get(str(id))
        image = profile_icon.get('image')
        return "http://ddragon.leagueoflegends.com/cdn/10.5.1/img/profileicon/" + image.get('full')

    def getTierIcon(self):
        tier = self.getProfileRank().get('tier')
        tier = tier.lower()
        tier = tier.capitalize()
        icon = "Emblem_" + tier + ".png"
        path = 'images/' + icon
        return path

    # Return Player Rank Info
    def getProfileRank(self):
        stats = League.by_summoner(self, self.region, self.getSummonerId())
        # Rank
        tier = stats.get('tier').title()
        rank = stats.get('rank')
        # LP / Wins Losses
        lp = stats.get('leaguePoints')
        wins = stats.get('wins')
        losses = stats.get('losses')
        # Win Ratio
        win_ratio = (wins / (wins + losses)) * 100
        win_ratio = round(win_ratio, 2)
        return dict({
            'tier': tier,
            'rank': rank,
            'lp': lp,
            'wins': wins,
            'losses': losses,
            'win_ratio': win_ratio
        })

    # Return Champion Name and Mastery Points
    # Dict['Champion Name': Mastery Points]
    def getTopFiveChamps(self):
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

        # Iteratively add champion to champ_names
        for key in champ_keys:
            champ_names.append(self.getChampion(key))

        # Fill dictionary with <Champion, Mastery Points> pairs
        for i in range(5):
            top_five[champ_names[i]] = points[i]
        return top_five

    # Return List[match_info]
    # match_info is a dictionary
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

    # Given champion.json file and champion id
    # Return champion corresponding to id
    def getChampion(self, id):
        # Search champion.json file for champion
        with open("./en_US/champion.json", "r", encoding="utf8") as read_file:
            champ_file = json.load(read_file)
        champ_data = champ_file.get('data')
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
            