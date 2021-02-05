import requests
import aiohttp
import asyncio
import json

class Riot:
    def __init__(self, network):
        self.network = network
        self.asyncio = asyncio
        self.loop = None
        self.matchDetails = {}
        self.riotIds = {}
        self.playerNames = {}
        self.loadJson()
        return

    def loadJson(self):
        try:
            with open('Resource/matchDetails.json', 'r') as fp:
                self.matchDetails = json.load(fp)
            with open('Resource/riotIds.json', 'r') as fp:
                self.riotIds = json.load(fp)
            with open('Resource/playerNames.json', 'r') as fp:
                self.playerNames = json.load(fp)
        except IOError:
            return


    def save(self):
        with open('Resource/matchDetails.json', 'w+') as fp:
            json.dump(self.matchDetails, fp)
        with open('Resource/riotIds.json', 'w+') as fp:
            json.dump(self.riotIds, fp)
        with open('Resource/playerNames.json', 'w+') as fp:
            json.dump(self.playerNames, fp)


    def getPlayerPUUID(self, name, tag):

        masterId = self.network.setting.riotServer + name + tag

        if masterId in self.riotIds:
            return self.riotIds[masterId]

        puuidLink = self.network.getPUUID(name, tag)
        # print(puuidLink)
        try:
            puuidRequest = requests.get(puuidLink)
        except requests.exceptions.RequestException as e:
            print(puuidLink)
            print(e)
            print('无法连接PUUID服务器')
            return None
        idDetails = puuidRequest.json()
        if not puuidRequest.ok:
            print(puuidLink)
            print(puuidRequest.headers)
            print(puuidRequest.status_code)
            print('userId -> PUUID服务器错误')
            print(idDetails)
            return None
        else:
            if idDetails.get('puuid') is not None:
                self.riotIds[masterId] = idDetails.get('puuid')
                self.save()
            return idDetails.get('puuid')

        

    def getMatchs(self, ppid):
        matchLink = self.network.getMatchsLink(ppid)
        try:
            matchRequest = requests.get(matchLink)
        except requests.exceptions.RequestException as e:
            print(matchLink)
            print(e)
            print('无法连接比赛ID服务器')
            return None
        matchIds = matchRequest.json()
        if not matchRequest.ok:
            print(matchLink)
            print(matchRequest.headers)
            print(matchRequest.status_code)
            print('比赛ID服务器错误')
            print(matchIds)
            return None
        return matchIds

    async def aioMatchDetail(self, matchId):
        if matchId in self.matchDetails.keys:
            return self.matchDetails[matchId]
        async with aiohttp.ClientSession() as session:
            detailsLink = self.network.getDetailsLink(matchId)
            async with session.get(detailsLink) as resp:
                detail = await resp.json()

        header = resp.headers
        if 'X-Method-Rate-Limit-Count' in header:
            print('X-Method-Rate-Limit-Count: ',
                  header['X-Method-Rate-Limit-Count'])
            print('X-App-Rate-Limit', header['X-App-Rate-Limit'])

        if 'Retry-After' in header:
                print('aio服务器正忙,请等待', header['Retry-After'], '秒')
                return header['Retry-After']

        if resp.ok:
            self.matchDetails[matchId] = detail
            self.save()
            return detail
        else:
            print('AIO比赛内容服务器错误: ', resp.status)
            print(detailsLink)
            print(detail)
            return None

    def getDetail(self, matchId):
        if matchId in self.matchDetails:
            return self.matchDetails[matchId]
        detailsLink = self.network.getDetailsLink(matchId)
        try:
            detailsRequest = requests.get(detailsLink)
        except requests.exceptions.RequestException as e:
            print(detailsLink)
            print(e)
            print('无法连接比赛内容服务器')
            return None
        detail = detailsRequest.json()
        header = detailsRequest.headers
        if 'X-Method-Rate-Limit-Count' in header:
            print('X-Method-Rate-Limit-Count: ',
                  header['X-Method-Rate-Limit-Count'])
            print('X-App-Rate-Limit', header['X-App-Rate-Limit'])
        if not detailsRequest.ok:
            print(detailsLink)
            print(header)
            print(detailsRequest.status_code)
            print(detail)
            print('比赛内容服务器错误')
            if 'Retry-After' in header:
                print('服务器正忙,请等待', header['Retry-After'], '秒')
                return header['Retry-After']
            return None
        else:
            self.matchDetails[matchId] = detail
            self.save()
        if detail is None:
            print('比赛内容服务返回空')
        return detail

    # 在main中使用和inspector中使用
    def getPlayerName(self, puuid):
        if puuid in self.playerNames:
            return self.playerNames[puuid]
        nameLink = self.network.getNameLink(puuid)
        try:
            nameRequest = requests.get(nameLink)
        except requests.exceptions.RequestException as e:
            print(nameLink)
            print(e)
            print('无法连接puuid->userId服务器')
            return '名字Unknow', 'unknow'
        name = nameRequest.json()
        #headers = nameRequest.headers
        #print(headers)
        if not nameRequest.ok:
            print(nameLink)
            print(nameRequest.headers)
            print(nameRequest.status_code)
            print(name)
            print('puuid->userid服务器错误:')
            return '名字Unknow', 'unknow'
        else:
            self.playerNames[puuid] = name['gameName'], name['tagLine']
            self.save()
        return name['gameName'], name['tagLine']