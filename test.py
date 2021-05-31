import unittest

from pyGG import Summoner, MatchHistory, Match, Champions, Leaderboard, Statistics


class TestOpgg(unittest.TestCase):
    def setUp(self):
        self.summoner_name = "dharana"
        self.summoner_id = 38911216

        self.match = {"matchId": 3881510735, "gameTime": 1619404792}

    def test_get_summoner(self):
        opgg = Summoner(self.summoner_name)
        self.assertEqual(opgg.json["summoner-id"], self.summoner_id)

    def test_get_match_history_from_summoner(self):
        opgg = Summoner(self.summoner_name)
        self.assertIsInstance(opgg.get_match_history(), MatchHistory)

    def test_get_champions_from_summoner(self):
        opgg = Summoner(self.summoner_name)
        self.assertIsInstance(opgg.get_champions(), Champions)

    def test_get_match_history(self):
        mh = MatchHistory(self.summoner_id)
        self.assertEqual(len(mh.json), 7)

    def test_show_more_matches_fail(self):
        mh = MatchHistory(self.summoner_id)
        self.assertRaises(Exception, mh.load_more)

    def test_get_all_matches_from_match_history(self):
        mh = MatchHistory(self.summoner_id)
        match_list = mh.get_matches()
        self.assertIsInstance(match_list[0], Match)

    def test_get_match_players(self):
        match = Match(self.match["matchId"], self.summoner_id, self.match["gameTime"])
        self.assertEqual(len(match.json["players"]), 10)

    def test_get_match_summary(self):
        match = Match(self.match["matchId"], self.summoner_id, self.match["gameTime"])
        self.assertDictEqual(
            match.json["summary"],
            {
                "win-team": {
                    "Baron": 1,
                    "Dragon": 4,
                    "Tower": 8,
                    "Kills": 45,
                    "Gold": 72891,
                },
                "lose-team": {
                    "Baron": 0,
                    "Dragon": 2,
                    "Tower": 2,
                    "Kills": 30,
                    "Gold": 60416,
                },
            },
        )

    def test_get_champions(self):
        champions = Champions(self.summoner_id).json
        self.assertEqual(champions["Vayne"]["Penta Kill"], 1)

    def test_get_champions_season(self):
        champions = Champions(self.summoner_id, 15).json
        self.assertEqual(champions["Jinx"]["Gold"], 12070)

    def test_leaderboard(self):
        lb = Leaderboard()
        self.assertEqual(len(lb.json), 100)

    def test_leaderboard_page(self):
        lb = Leaderboard(2)
        self.assertEqual(len(lb.json), 100)

    def test_leaderboard_next_page(self):
        lb = Leaderboard()
        lb.next_page()
        self.assertEqual(len(lb.json), 200)

    def test_leaderboard_load_page(self):
        lb = Leaderboard()
        lb.load_page(5)
        self.assertEqual(len(lb.json), 100)

    def test_statistics(self):
        stats = Statistics()
        self.assertGreaterEqual(len(stats.json), 155)

    def test_statistics_form(self):
        form = {
            "type": "win",
            "league": "diamond",
            "period": "week",
            "mapId": 1,
            "queue": "ranked",
        }
        stats = Statistics(form)
        self.assertGreaterEqual(len(stats.json), 155)

    def test_get_summoner_rank(self):
        opgg = Summoner(self.summoner_name)
        rank_info = opgg.json["rank-solo"]
        self.assertDictEqual(
            rank_info,
            {
                "type": "Ranked Solo",
                "tier": "Platinum 1",
                "lp": 75,
                "win": 158,
                "lose": 150,
                "winratio": 51,
                "league": "Twitch's Marauders",
            },
        )

    def test_get_summoner_sub_rank(self):
        opgg = Summoner(self.summoner_name)
        rank_info = opgg.json["rank-flex"]
        self.assertDictEqual(
            rank_info,
            {
                "type": "Flex 5:5 Rank",
                "tier": "Gold 1",
                "lp": 79,
                "win": 8,
                "lose": 10,
                "winratio": 44,
            },
        )

    def test_get_summoner_past_ranks(self):
        opgg = Summoner(self.summoner_name)
        past_ranks = opgg.json["past-rank"]
        self.assertEqual(len(past_ranks), 6)


if __name__ == "__main__":
    unittest.main()
