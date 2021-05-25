import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


class Leaderboard:
    def __init__(self, page=1):
        self.page = page
        self.soup = self.__load_leaderboard()
        self.json = self.__clean_leaderboard()
        self.df = self.__to_df()

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

    def __to_df(self):
        return pd.DataFrame(self.json).set_index("rank")

    def load_page(self, page):
        """
        Load leadboard for given page (100 summoners per page)
        """
        self.page = page
        self.soup = self.__load_leaderboard()
        self.json = self.__clean_leaderboard()
        self.df = self.__to_df()

    def next_page(self):
        """
        Increment page number and load page (100 summoners per page)
        """
        self.load_page(self.page + 1)
