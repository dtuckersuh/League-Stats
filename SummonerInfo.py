from riotwatcher import RiotWatcher

watcher = RiotWatcher('RGAPI-6810e04d-cb23-471c-abae-a0bf45414b90')

region = 'na1'

info = watcher.summoner.by_name(region, 'suh hyungwon')

id = info.get('id')
accountId = info.get('accountId')
puuid = info.get('puuid')
name = info.get('name')
level = info.get('summonerLevel')


