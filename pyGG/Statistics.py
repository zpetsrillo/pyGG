import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


class Statistics:
    def __init__(self, form=None):
        if form is None:
            self.__form = {
                "type": "win",
                "league": "",
                "period": "month",
                "mapId": 1,
                "queue": "ranked",
            }
        else:
            self.__form = form

        self.__soup = self.__load_data(self.__form)
        self.__df = self.__load_df()
        self.__json = self.__load_json()

    @property
    def soup(self):
        return self.__soup

    @property
    def json(self):
        return self.__json

    @property
    def df(self):
        return self.__df

    def __load_data(self, form):

        if form == None:
            form = {
                "type": "win",
                "league": "",
                "period": "month",
                "mapId": 1,
                "queue": "ranked",
            }

        res = requests.post("https://na.op.gg/statistics/ajax2/champion/", form)
        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def __clean_data(self):
        df = pd.read_html(str(self.soup))[0]
        df.drop(columns=["Champion"], inplace=True)
        df.rename(columns={"Champion.1": "Champion"}, inplace=True)
        df["Win rate"] = df["Win rate"].map(lambda x: float(x[:-1]))
        df["KDA"] = df["KDA"].map(lambda x: float(x[:-2]))
        df.set_index("#", inplace=True)
        return df

    def __load_json(self):
        return self.df.set_index("Champion").T.to_dict()

    def __load_df(self):
        return self.__clean_data()

    def __str__(self):
        return json.dumps(self.json, indent=4)
