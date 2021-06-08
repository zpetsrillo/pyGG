import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

from pyGG.Match import Match
from pyGG.DataLoader import DataLoader


class MatchHistory(DataLoader):
    def __init__(self, summoner_id, gamemode="soloranked"):
        self.__summoner_id = summoner_id
        self.__gamemode = gamemode
        self.__last_info = 0

        super().__init__()

    @property
    def summoner_id(self):
        return self.__summoner_id

    @summoner_id.setter
    def summoner_id(self, value):
        if type(value) != int:
            raise ValueError("summoner_id must be type integer")
        if value < 0:
            raise ValueError("summoner_id must be non-negative")
        self.__init__(value, self.gamemode)

    @property
    def gamemode(self):
        return self.__gamemode

    @gamemode.setter
    def gamemode(self, value):
        gamemodes = [
            "soloranked",
            "flexranked",
            "normal",
            "aram",
            "bot",
            "clash",
            "event",
            "total",
        ]

        if value not in gamemodes:
            raise ValueError("Unsupported gamemode")

        self.__init__(self.summoner_id, value)

    def _load_data(self):
        params = {
            "startInfo": self.__last_info,
            "summonerId": self.summoner_id,
            "type": self.gamemode,
        }

        res = requests.get(
            "https://na.op.gg/summoner/matches/ajax/averageAndList/", params=params
        )
        if res.status_code == 418:
            raise Exception("No results to load")

        as_json = json.loads(res.text)
        self.__last_info = as_json["lastInfo"]

        soup = BeautifulSoup(as_json["html"], "lxml")
        return soup

    def __load_matches(self):
        if self.soup.findAll(text="There are no results recorded."):
            raise Exception("There are no results recorded.")

        match_history = []
        matches = self.soup.find_all(class_="GameItem")
        for match in matches:
            game_id = match["data-game-id"]
            summoner_id = match["data-summoner-id"]
            game_time = match["data-game-time"]
            game_result = match["data-game-result"]

            match_history.append(
                {
                    "gameId": game_id,
                    "summonerId": summoner_id,
                    "gameTime": game_time,
                    "result": game_result,
                }
            )

        return match_history

    def _load_json(self):
        return self.__load_matches()

    def _load_df(self):
        columns = ["gameId", "summonerId", "gameTime", "result"]
        df = pd.DataFrame(self.json, columns=columns)
        df["gameTime"] = pd.to_datetime(df["gameTime"], unit="s")
        return df

    def load_more(self):
        """
        Load more items into match_history
        """
        self._load_data()
        self._json += self.__load_matches()
        self._df = self._load_df()

    def get_matches(self):
        """
        Returns a list of Match objects for all items currently in match_history
        """
        match_list = []
        for match in self.json:
            match_list.append(
                Match(match["gameId"], match["summonerId"], match["gameTime"])
            )

        return match_list

    def __len__(self):
        return len(self.json)

    def __repr__(self):
        return (
            f"MatchHistory - {self.summoner_id} - {self.gamemode} - {self.__last_info}"
        )
