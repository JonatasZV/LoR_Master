API_KEY = '?api_key=' + 'RGAPI-3b5bde16-66b4-4943-b8fa-241d27b29344'
MATCH_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

def getMatchsLink(ppid):
    return MATCH_KEY  + ppid + '/ids' + API_KEY

def getDetailsLink(matchId):
    return DETAILS_KEY + matchId + API_KEY

def getNameLink(ppid):
    return NAME_KEY + ppid + API_KEY


def getPUUID(name, tag):
    return PUUID_KEY + name + '/' + tag + API_KEY