import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json


class Leaderboard:
    def __init__(self, page=1):
        self.__page = page
        self.__soup = self.__load_leaderboard()
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
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        if type(value) != int:
            raise ValueError("Page must be type integer")
        if value < 0:
            raise ValueError("Page must be non-negative")
        self.__page = value

    def __load_leaderboard(self):
        params = {"page": self.page}

        res = requests.get("https://na.op.gg/ranking/ladder/", params=params)
        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def __clean_leaderboard_rows(self, rows):
        output = []
        for row in rows:
            summoner_id = re.search(r"summoner-(\d+)", row["id"])[1]
            rank = row.find("td", class_="ranking-table__cell--rank").text.strip()
            summoner = row.find(
                "td", class_="ranking-table__cell--summoner"
            ).text.strip()
            tier = row.find("td", class_="ranking-table__cell--tier").text.strip()
            lp = row.find("td", class_="ranking-table__cell--lp").text.split()[0]
            level = row.find("td", class_="ranking-table__cell--level").text.strip()

            win_ratio = row.find("td", class_="ranking-table__cell--winratio")
            win = win_ratio.find(class_="winratio-graph__text--left").text.strip()
            lose = win_ratio.find(class_="winratio-graph__text--right").text.strip()
            wr = win_ratio.find(class_="winratio__text").text.strip()[:-1]

            output.append(
                {
                    "summoner_id": int(summoner_id),
                    "rank": int(rank),
                    "summoner": summoner,
                    "tier": tier,
                    "lp": int(lp.replace(",", "")),
                    "level": int(level),
                    "win": int(win),
                    "lose": int(lose),
                    "wr": int(wr),
                }
            )

        return output

    def __clean_leaderboard_rows_highest(self, rows):
        output = []
        for row in rows:
            summoner_id = re.search(r"summoner-(\d+)", row["id"])[1]

            rank = row.find(class_="ranking-highest__rank").text.strip()
            summoner = row.find(class_="ranking-highest__name").text.strip()
            tier, lp, _ = row.find(class_="ranking-highest__tierrank").text.split()
            level = re.search(
                r"(Lv\.)?(\d+)", row.find(class_="ranking-highest__level").text.strip()
            )[2]

            win_ratio = row.find("div", class_="ranking-highest-winratio")
            win = win_ratio.find(class_="winratio-graph__text--left").text.strip()
            lose = win_ratio.find(class_="winratio-graph__text--right").text.strip()
            wr = win_ratio.find(class_="winratio__text").text.strip()[:-1]

            output.append(
                {
                    "summoner_id": int(summoner_id),
                    "rank": int(rank),
                    "summoner": summoner,
                    "tier": tier,
                    "lp": int(lp.replace(",", "")),
                    "level": int(level),
                    "win": int(win),
                    "lose": int(lose),
                    "wr": int(wr),
                }
            )

        return output

    def __clean_leaderboard(self):
        output = []

        if self.page == 1:
            ranking_highest = self.soup.find_all("li", class_="ranking-highest__item")
            output += self.__clean_leaderboard_rows_highest(ranking_highest)

        rows = self.soup.find_all("tr", class_="ranking-table__row")
        output += self.__clean_leaderboard_rows(rows)

        return output

    def __load_json(self):
        return self.__clean_leaderboard()

    def __load_df(self):
        return pd.DataFrame(self.json).set_index("rank")

    def load_page(self, page):
        """
        Load leadboard for given page (100 summoners per page)
        """
        self.__init__(page)

    def next_page(self):
        """
        Increment page number and load page (100 summoners per page)
        """
        self.load_page(self.page + 1)

    def __len__(self):
        return len(self.json)

    def __str__(self):
        return json.dumps(self.json, indent=4)
