import unittest

from pyGG import pyGG


class TestOpgg(unittest.TestCase):
    def setUp(self):
        self.summoner_name = "dharana"
        self.summoner_id = 38911216

        self.match = {"matchId": 3881510735, "gameTime": 1619404792}

    def test_get_profile(self):
        opgg = pyGG.pyGG(self.summoner_name)
        self.assertIsInstance(opgg.summoner, pyGG.Summoner)

    def test_show_more_matches_success(self):
        summoner = pyGG.Summoner(self.summoner_id)
        summoner.load_more()
        self.assertEqual(len(summoner.match_history), 40)

    # def test_show_more_matches_fail(self):

    def test_get_match_history(self):
        summoner = pyGG.Summoner(self.summoner_id)
        self.assertEqual(len(summoner.match_history), 20)

    # def test_get_all_matches(self):

    def test_get_match_players(self):
        match = pyGG.Match(
            self.match["matchId"], self.summoner_id, self.match["gameTime"]
        )
        self.assertEqual(len(match.players), 10)


if __name__ == "__main__":
    unittest.main()