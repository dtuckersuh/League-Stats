from .summoner import Summoner
import json

class Champion:
    def __init__(self, summoner):
        self.summoner = summoner
        
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

        # Iteratively add champion to champ_names
        for key in champ_keys:
            champ_names.append(self.getChampion(champ_data, key))

        # Fill dictionary with <Champion, Mastery Points> pairs
        for i in range(5):
            top_five[champ_names[i]] = points[i]
        return top_five
    
    # Given champion.json file and champion id
    # Return champion corresponding to id
    def getChampion(self, file, id):
        # Search champion.json file for champion
        for champ in file.items():
            attribute = champ[1]
            if (int(attribute.get('key'))) == id:
                return attribute.get('id')
        return None

    def getChampionIcon(self, name):
        return 'http://ddragon.leagueoflegends.com/cdn/10.7.1/img/champion/' + name + '.png'
    
