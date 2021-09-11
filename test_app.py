from unittest import TestCase
from flask import json
from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:  # Question: what is the difference between app.test and self.test
            response = client.post("/api/new-game")
            # breakpoint()""
            # data = json.loads(response.get_data(as_text=True))
            data = response.get_json()
            # write a test for this route
            self.assertIn('gameId', data)
            # self.assertEquals(type(data['board'][0]) == "list", "incorrect",
            #                         type(data['board']) == "list", "incorrect")

            self.assertTrue(all(isinstance(x, list)) for x in data['board'])

    def test_api_score_word(self):
        """Test scoring a word"""

        with self.client as client:
            new_game_response = client.post("/api/new-game")
            game_data = new_game_response.get_json()

            game_id = game_data["gameId"]
            game = games[game_id]
            game.board = [
                ['C', 'A', 'T', 'A', 'S'],
                ['E', 'V', 'S', 'E', 'G'],
                ['S', 'S', 'E', 'K', 'H'],
                ['E', 'I', 'O', 'S', 'S'],
                ['A', 'B', 'L', 'O', 'A'],
            ]

            score_word_response_ok = client.post(
                "/api/score-word",
                json={'gameId': game_id, 'word': "CAT"})
            score_word_data_ok = score_word_response_ok.get_json()

            score_word_response_not_a_word = client.post(
                "/api/score-word", json={'gameId': game_id, 'word': "ADASDA"})
            score_word_data_not_a_word = score_word_response_not_a_word.get_json()

            score_word_response_not_on_board = client.post(
                "/api/score-word", json={'gameId': game_id, 'word': "ZEBRA"})
            score_word_data_not_on_board = score_word_response_not_on_board.get_json()

            self.assertEquals(score_word_data_ok["result"], "ok")
            self.assertEquals(score_word_data_not_a_word["result"], "not-word")
            self.assertEquals(
                score_word_data_not_on_board["result"], "not-on-board")
