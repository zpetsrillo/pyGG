import pandas as pd
import requests
from bs4 import BeautifulSoup

from pyGG.DataLoader import DataLoader


class Statistics(DataLoader):
    def __init__(self, form=None):
        if form is None:
            form = {
                "type": "win",
                "league": "",
                "period": "month",
                "mapId": 1,
                "queue": "ranked",
            }
        else:
            keys = {"type", "league", "period", "mapId", "queue"}
            if not keys.issubset(set(form.keys())):
                raise ValueError("form missing nessecary values")

        self.__form = form

        # Data loaded out of usual order (df before json)
        self._soup = self._load_data()
        self._df = self._load_df()

        super().__init__()

    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, value):
        self.__init__(value)

    def _load_data(self):
        form = self.__form

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

    def _load_json(self):
        return self.df.set_index("Champion").T.to_dict()

    def _load_df(self):
        return self.__clean_data()

    def __len__(self):
        return len(self.json)
