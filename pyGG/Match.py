import requests
from bs4 import BeautifulSoup


class Match:
    def __init__(self, game_id, summoner_id, game_time):
        self.game_id = game_id
        self.summoner_id = summoner_id
        self.game_time = game_time

        self.soup = self._load_data()

        self.players = self._get_players()

    def _load_data(self):
        params = {
            "gameId": self.game_id,
            "summonerId": self.summoner_id,
            "gameTime": self.game_time,
        }

        res = requests.get(
            "https://na.op.gg/summoner/matches/ajax/detail/", params=params
        )

        soup = BeautifulSoup(res.content, "html.parser")
        return soup

    def _get_players(self):
        players = []
        summoner_items = self.soup.find_all(attrs={"class": "SummonerName Cell"})
        for item in summoner_items:
            name = item.text.strip()
            players.append(name)

        return players