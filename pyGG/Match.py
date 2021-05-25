import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


class Match:
    def __init__(self, game_id, summoner_id, game_time):
        self.game_id = game_id
        self.summoner_id = summoner_id
        self.game_time = game_time

        self.soup = self.__load_data()

        self.json = {"summary": self.__get_summary(), "players": self.__get_players()}

    def __load_data(self):
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

    def __get_players(self):
        win, lose = self.__get_tables()
        win = self.__clean_table(win)
        lose = self.__clean_table(lose)

        players = win.T.to_dict()
        players.update(lose.T.to_dict())

        return players

    def __get_tables(self):
        # TODO: clean tables
        win_df = pd.read_html(str(self.soup.find("table", class_="Result-WIN")))[0]
        lose_df = pd.read_html(str(self.soup.find("table", class_="Result-LOSE")))[0]
        return win_df, lose_df

    def __clean_table(self, df):
        # TODO: add summoner spells, runes, and items
        team_info = df.columns[0].split()
        df["Result"] = team_info[0]
        df["Team Color"] = re.search(r"\(?(\w+)", team_info[1])[1]
        df["Summoner Name"] = df[df.columns[3]]
        df["Champion"] = df[df.columns[0]].map(lambda x: " ".join(x.split()[:-1]))
        df["Level"] = df[df.columns[0]].map(lambda x: int(x.split()[-1]))
        df["OP Rank"] = df["OP Score"].map(lambda x: x.split()[1])
        df["OP Score"] = df["OP Score"].map(lambda x: float(x.split()[0]))
        df["Kill Participation"] = df["KDA"].map(
            lambda x: int(re.search(r"\d+", x.split()[2])[0])
        )
        df["Kill Ratio"] = df["KDA"].map(
            lambda x: re.search(r"^[^:]+", x.split()[0])[0]
        )
        df["K"] = df["KDA"].map(lambda x: int(x.split()[1].split("/")[0]))
        df["D"] = df["KDA"].map(lambda x: int(x.split()[1].split("/")[1]))
        df["A"] = df["KDA"].map(lambda x: int(x.split()[1].split("/")[2]))
        df["Vision Wards Purchased"] = df["Wards"].map(lambda x: int(x.split()[0]))
        df["Wards Placed"] = df["Wards"].map(lambda x: int(x.split()[1]))
        df["Wards Destoryed"] = df["Wards"].map(lambda x: int(x.split()[3]))
        df["CS/min"] = df["CS"].map(
            lambda x: float(re.search(r"\d+\.?\d*", x.split()[1])[0])
        )
        df["CS"] = df["CS"].map(lambda x: int(x.split()[0]))

        columns = [
            "Summoner Name",
            "Champion",
            "Result",
            "Team Color",
            "Level",
            "Tier",
            "OP Rank",
            "OP Score",
            "Kill Participation",
            "Kill Ratio",
            "K",
            "D",
            "A",
            "Damage",
            "Vision Wards Purchased",
            "Wards Placed",
            "Wards Destoryed",
            "CS",
            "CS/min",
        ]

        return df[columns].set_index("Summoner Name")

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

    def __extract_team_info(self, team):
        keys = ["Baron", "Dragon", "Tower"]
        values = [
            int(obj_score.text.strip())
            for obj_score in team.find_all(class_="ObjectScore")
        ]

        return dict(zip(keys, values))

    def __get_summary(self):
        summary = self.soup.find(class_="Summary")
        win_team = self.__extract_team_info(summary.find(class_="Team-200"))
        lose_team = self.__extract_team_info(summary.find(class_="Team-100"))
        win_kills, lose_kills, win_gold, lose_gold = self._extract_summary_info(summary)

        win_team["Kills"] = win_kills
        lose_team["Kills"] = lose_kills
        win_team["Gold"] = win_gold
        lose_team["Gold"] = lose_gold

        return {"win-team": win_team, "lose-team": lose_team}
