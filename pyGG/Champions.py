import pandas as pd
import requests
import re


class Champions:
    def __init__(self, summoner_id, season=17):
        self.summoner_id = summoner_id
        self.df = self.__load_champions(season)
        self.json = self.df.T.to_dict()

    def __load_champions(self, season):
        params = {"summonerId": self.summoner_id, "season": season}

        res = requests.get(
            "https://na.op.gg/summoner/champions/ajax/champions.rank/", params=params
        )
        df = pd.read_html(res.text)[0]
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
