import requests
from bs4 import BeautifulSoup
import pandas as pd


class Match:
    def __init__(self, game_id, summoner_id, game_time):
        self.game_id = game_id
        self.summoner_id = summoner_id
        self.game_time = game_time

        self.soup = self._load_data()

        self.players = self._get_players()
        self.summary = self._get_summary()

    def _load_data(self):
        params = {
            "gameId": self.game_id,
            "summonerId": self.summoner_id,
            "gameTime": self.game_time,
            "moreLoad": 1,
        }

        res = requests.get(
            "https://na.op.gg/summoner/matches/ajax/detail/", params=params
        )

        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def _get_players(self):
        players = []
        summoner_items = self.soup.find_all(class_="SummonerName Cell")
        for item in summoner_items:
            name = item.text.strip()
            players.append(name)

        return players

    def _get_tables(self):
        # TODO: clean tables
        win_df = pd.read_html(str(self.soup.find("table", class_="Result-WIN")))[0]
        lose_df = pd.read_html(str(self.soup.find("table", class_="Result-LOSE")))[0]
        return win_df, lose_df

    def _extract_summary_info(self, summary):
        win_team = summary.find_all(class_="graph win--team")
        lose_team = summary.find_all(class_="graph lose--team")

        win_kills, win_gold = [int(val["style"][5:]) for val in win_team]
        lose_kills, lose_gold = [int(val["style"][5:]) for val in lose_team]

        return (
            win_kills,
            lose_kills,
            win_gold,
            lose_gold,
        )

    def _extract_team_info(self, team):
        keys = ["Baron", "Dragon", "Tower"]
        values = [
            int(obj_score.text.strip())
            for obj_score in team.find_all(class_="ObjectScore")
        ]

        return dict(zip(keys, values))

    def _get_summary(self):
        summary = self.soup.find(class_="Summary")
        win_team = self._extract_team_info(summary.find(class_="Team-200"))
        lose_team = self._extract_team_info(summary.find(class_="Team-100"))
        win_kills, lose_kills, win_gold, lose_gold = self._extract_summary_info(summary)

        win_team["Kills"] = win_kills
        lose_team["Kills"] = lose_kills
        win_team["Gold"] = win_gold
        lose_team["Gold"] = lose_gold

        return {"win-team": win_team, "lose-team": lose_team}
