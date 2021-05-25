import pandas as pd
import requests
from bs4 import BeautifulSoup


class Statistics:
    def __init__(self, form=None):
        self.soup = self.__load_data(form)
        self.df = self.__clean_data()
        self.json = self.df.set_index("Champion").T.to_dict()

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
