import requests
from bs4 import BeautifulSoup

from pyGG.Summoner import Summoner
from pyGG.Match import Match


class pyGG:
    def __init__(self, summoner_name=None, summoner_id=None):
        self.summoner_name = summoner_name

        if summoner_id is not None:
            self.summoner_id = summoner_id

        if summoner_name is not None:
            self.soup = self._load_data(self.summoner_name)
            self.summoner_id = self._get_summoner_id()

    def _load_data(self, summoner_name):
        params = {"userName": self.summoner_name}
        res = requests.get(f"https://na.op.gg/summoner/", params=params)
        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def _get_summoner_id(self):
        game_list = self.soup.find(class_="GameListContainer")
        summoner_id = game_list["data-summoner-id"]
        return summoner_id

    def get_summoner(self):
        return Summoner(self.summoner_id)
