import requests
from bs4 import BeautifulSoup

from pyGG.MatchHistory import MatchHistory
from pyGG.Match import Match


class Summoner:
    def __init__(self, summoner_name):
        self.summoner_name = summoner_name

        self.soup = self.__load_data(self.summoner_name)
        self.json = self.__as_json()

    def __load_data(self, summoner_name):
        params = {"userName": self.summoner_name}
        res = requests.get(f"https://na.op.gg/summoner/", params=params)
        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def __get_summoner_id(self):
        game_list = self.soup.find(class_="GameListContainer")
        summoner_id = game_list["data-summoner-id"]
        return summoner_id

    def __get_rank(self):
        rank_info = self.soup.find(class_="TierRankInfo")
        rank_type = rank_info.find(class_="RankType").text
        rank_tier = rank_info.find(class_="TierRank").text
        rank_lp = rank_info.find(class_="LeaguePoints").text.split()[0]
        rank_win = rank_info.find(class_="wins").text[:-1]
        rank_lose = rank_info.find(class_="losses").text[:-1]
        rank_winratio = rank_info.find(class_="winratio").text.split()[-1][:-1]
        rank_league = rank_info.find(class_="LeagueName").text.strip()

        return {
            "type": rank_type,
            "tier": rank_tier,
            "lp": int(rank_lp),
            "win": int(rank_win),
            "lose": int(rank_lose),
            "winratio": int(rank_winratio),
            "league": rank_league,
        }

    def __get_sub_rank(self):
        rank_info = self.soup.find(class_="sub-tier__info")
        rank_type = rank_info.find(class_="sub-tier__rank-type").text
        rank_tier = rank_info.find(class_="sub-tier__rank-tier").text.strip()
        rank_lp, rank_win, rank_lose = rank_info.find(
            class_="sub-tier__league-point"
        ).text.split()
        rank_lp = rank_lp[:-3]
        rank_win = rank_win[:-1]
        rank_lose = rank_lose[:-1]
        rank_winratio = rank_info.find(
            "div", class_="sub-tier__gray-text"
        ).text.split()[-1][:-1]

        return {
            "type": rank_type,
            "tier": rank_tier,
            "lp": int(rank_lp),
            "win": int(rank_win),
            "lose": int(rank_lose),
            "winratio": int(rank_winratio),
        }

    def __get_past_rank(self):
        past_rank_list = self.soup.find(class_="PastRankList")
        past_rank_items = past_rank_list.find_all(class_="Item tip")

        past_leagues = [rank for rank in past_rank_list.text.split("\n") if rank != ""]
        past_tier_lp = [" ".join(item["title"].split()[1:]) for item in past_rank_items]

        past_rank = [" ".join(item) for item in zip(past_leagues, past_tier_lp)]

        return past_rank

    def __get_level(self):
        level = self.soup.find(class_="Level").text.strip()

        return int(level)

    def __get_ladder_rank(self):
        ranking = self.soup.find(class_="ranking").text.strip().replace(",", "")

        return int(ranking)

    def __as_json(self):
        return {
            "summoner-id": self.__get_summoner_id(),
            "level": self.__get_level(),
            "ladder-rank": self.__get_ladder_rank(),
            "rank-solo": self.__get_rank(),
            "rank-flex": self.__get_sub_rank(),
            "past-rank": self.__get_past_rank(),
        }

    def get_match_history(self):
        return MatchHistory(self.json["summoner-id"])
