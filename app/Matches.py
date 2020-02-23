from .summoner import Summoner

class Matches:

    def __init__(self, summoner):
        self.summoner = summoner

    # Return essential Match History Info:
    # Win or Fail, KDA, items, other players
    # List of Matches, each match a dictionary
    def getMatchHistory(self):
        matches = self.getMatchlist(self)
        matchlist = []
        for i in range(matches):
            match = matches[i]
            match_info = {'Outcome': match.get('win')}
            matchlist.append(match_info)
        return matchlist

    # Helper for Match History
    # Returns List[last 10 matches] which contain lane and gameId
    def getMatchlist(self, region):
        matchlist = self.watcher.match.matchlist_by_account(region, self.getAccountId(), end_index=10)
        return matchlist
