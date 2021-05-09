import requests
from bs4 import BeautifulSoup
import json


class Summoner:
    def __init__(self, summoner_id, gamemode="soloranked"):
        self.summoner_id = summoner_id
        self.gamemode = gamemode
        self.last_info = 0

        self.soup = self._load_data()
        self.match_history = self._load_matches()

    def _load_data(self):
        params = {
            "startInfo": self.last_info,
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

    def _load_matches(self):
        # TODO: handle no more matches to load
        match_history = []
        matches = self.soup.find_all(class_="GameItem")
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

    def load_more(self):
        self._load_data()
        self.match_history += self._load_matches()
