import pandas as pd
import requests
import re

from pyGG.DataLoader import DataLoader


class Champions(DataLoader):
    def __init__(self, summoner_id, season=17):
        self.__summoner_id = summoner_id
        self.__season = season

        # Data loaded out of usual order (df before json)
        self._df = self._load_df()

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
        self.__init__(value, self.season)

    @property
    def season(self):
        return self.__season

    @season.setter
    def season(self, value):
        if type(value) != int:
            raise ValueError("season must be type integer")
        if value < 0:
            raise ValueError("season must be non-negative")
        self.__init__(self.summoner_id, value)

    def __load_champions(self, season):
        params = {"summonerId": self.summoner_id, "season": season}

        res = requests.get(
            "https://na.op.gg/summoner/champions/ajax/champions.rank/", params=params
        )
        df = pd.read_html(res.text, flavor="lxml")[0]
        df = self.__clean_champions_table(df)
        return df

    def __clean_champions_table(self, df):
        def win_lose_helper(x):
            if x is not None:
                return int(x[1])
            else:
                return 0

        df["Win"] = df["Played"].map(lambda x: re.search(r"^(\d+)W", x))
        df["Win"] = df["Win"].map(win_lose_helper)
        df["Lose"] = df["Played"].map(lambda x: re.search(r"(\d+)L", x))
        df["Lose"] = df["Lose"].map(win_lose_helper)
        df["Win Rate"] = df["Played"].map(lambda x: re.search(r"\s(\d+)%", x)[1])
        df["Played"] = df["Win"] + df["Lose"]
        df["K"] = df["KDA"].map(lambda x: x.split("/")[0].strip())
        df["D"] = df["KDA"].map(lambda x: x.split("/")[1].strip())
        df["A"] = df["KDA"].map(lambda x: x.split("/")[2].split()[0].strip())
        df["KDA Ratio"] = df["KDA"].map(
            lambda x: re.search(r"^[^:]+", x.split()[-1])[0]
        )
        df["CS/min"] = df["CS"].map(lambda x: re.search(r"\d+\.?\d?", x.split()[1])[0])
        df["CS"] = df["CS"].map(lambda x: x.split()[0])
        df.drop(columns=["#", "Champion.1", "KDA"], inplace=True)
        df.fillna(0, inplace=True)
        df.set_index("Champion", inplace=True)

        return df.apply(pd.to_numeric)

    def _load_json(self):
        return self.df.T.to_dict()

    def _load_df(self):
        return self.__load_champions(self.season)

    def __len__(self):
        return len(self.json)

    def __repr__(self):
        return f"Champions - {self.summoner_id} - {self.season}"
