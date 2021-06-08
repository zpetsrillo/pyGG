import json
import pandas as pd
from bs4 import BeautifulSoup


class DataLoader:
    def __init__(self):
        self._soup = self._load_data()
        self._json = self._load_json()
        self._df = self._load_df()

    @property
    def soup(self):
        return self._soup

    @property
    def json(self):
        return self._json

    @property
    def df(self):
        return self._df

    def _load_data(self):
        return BeautifulSoup()

    def _load_json(self):
        return dict()

    def _load_df(self):
        return pd.DataFrame()

    def __str__(self):
        return json.dumps(self.json, indent=4)
