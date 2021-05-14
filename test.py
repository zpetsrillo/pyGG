import unittest

from pyGG import Summoner, MatchHistory, Match, Champions, Leaderboard, Statistics


class TestOpgg(unittest.TestCase):
    def setUp(self):
        self.summoner_name = "dharana"
        self.summoner_id = 38911216

        self.match = {"matchId": 3881510735, "gameTime": 1619404792}

    def test_get_summoner(self):
        opgg = Summoner(self.summoner_name)
        self.assertIsInstance(opgg.get_match_history(), MatchHistory)

    def test_show_more_matches_success(self):
        mh = MatchHistory(self.summoner_id)
        mh.load_more()
        self.assertEqual(len(mh.json), 40)

    # def test_show_more_matches_fail(self):

    def test_get_match_history(self):
        mh = MatchHistory(self.summoner_id)
        self.assertEqual(len(mh.json), 20)

    # def test_get_full_match_history(self):

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

    # slow to execute
    # def test_get_all_matches(self):
    #     summoner = pyGG.Summoner(self.summoner_id)
    #     match_list = summoner.get_matches()
    #     self.assertIsInstance(match_list[0], pyGG.Match)

    def test_get_champions(self):
        champions = Champions(self.summoner_id).json
        self.assertEqual(champions["Vayne"]["Penta Kill"], 1)

    def test_leaderboard(self):
        lb = Leaderboard()
        self.assertEqual(len(lb.json), 100)

    def test_statistics(self):
        stats = Statistics()
        self.assertGreaterEqual(len(stats.json), 155)


if __name__ == "__main__":
    unittest.main()
