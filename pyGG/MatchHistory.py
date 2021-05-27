import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

from pyGG.Match import Match
from pyGG.Champions import Champions


class MatchHistory:
    def __init__(self, summoner_id, gamemode="soloranked"):
        self.summoner_id = summoner_id
        self.__gamemode = gamemode
        self.__last_info = 0

        self.__soup = self.__load_data()
        self.__json = self.__load_json()
        self.__df = self.__load_df()

    @property
    def soup(self):
        return self.__soup

    @property
    def json(self):
        return self.__json

    @property
    def df(self):
        return self.__df

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

        self.__gamemode = value

    def __load_data(self):
        params = {
            "startInfo": self.__last_info,
            "summonerId": self.summoner_id,
            "type": self.gamemode,
        }

        res = requests.get(
            "https://na.op.gg/summoner/matches/ajax/averageAndList/", params=params
        )
        as_json = json.loads(res.text)
        self.last_info = as_json["lastInfo"]

        soup = BeautifulSoup(as_json["html"], "lxml")
        return soup

    def __load_matches(self):
        # TODO: handle no more matches to load
        match_history = []
        matches = self.__soup.find_all(class_="GameItem")
        for match in matches:
            game_id = match["data-game-id"]
            summoner_id = match["data-summoner-id"]
            game_time = match["data-game-time"]
            game_result = match["data-game-result"]

            # TODO: Add all readily available match data to output

            match_history.append(
                {
                    "gameId": game_id,
                    "summonerId": summoner_id,
                    "gameTime": game_time,
                    "result": game_result,
                }
            )

        return match_history

    def __load_json(self):
        return self.__load_matches()

    def __load_df(self):
        columns = ["gameId", "summonerId", "gameTime", "result"]
        df = pd.DataFrame(self.__json, columns=columns)
        df["gameTime"] = pd.to_datetime(df["gameTime"], unit="s")
        return df

    def load_more(self):
        """
        Load more items into match_history
        """
        self.__load_data()
        self.__json += self.__load_matches()

    def get_matches(self):
        """
        Returns a list of Match objects for all items currently in match_history
        """
        match_list = []
        for match in self.__json:
            match_list.append(
                Match(match["gameId"], match["summonerId"], match["gameTime"])
            )

        return match_list

    def get_champions(self, season=17):
        """
        Returns Champions object for summoner, optional season paramater
        """
        return Champions(self.summoner_id, season)

    def __str__(self):
        return json.dumps(self.__json, indent=4)

    def __repr__(self):
        return json.dumps(self.__json, indent=4)
