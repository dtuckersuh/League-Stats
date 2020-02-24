from .summoner import Summoner

class Matches:

    def __init__(self, summoner):
        self.summoner = summoner

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

    # Translates boolean game outcome to "Victory" or "Defeat"
    def outcomeTranslate(self, stats):
        if stats.get('win'):
            return 'Victory'
        else:
            return 'Defeat'
