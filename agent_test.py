"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players
import time
from collections import namedtuple
from game_agent import (MinimaxPlayer, AlphaBetaPlayer)
from heuristics import (custom_score, alt_custom_score,
                        stages_score)
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)

from importlib import reload

Agent = namedtuple("Agent", ["player", "name"])

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
#        self.player1 = game_agent.AlphaBetaPlayer()
        self.player1 = AlphaBetaPlayer(score_fn=stages_score)
        self.player2 = sample_players.HumanPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    def get_time_left(self):
    	time_per_move = .15  # time in seconds
    	now = time.time()
    	def time_left():     # time in milliseconds
    		return int((time_per_move - (time.time() - now))* 1000)
    	return time_left


    def test_init(self):
    	while True:
    		if len(self.game.get_legal_moves())==0:
    			print("You win! (AlphaBeta loses)")
    			break

	    	new_move = self.player1.get_move(self.game, self.get_time_left())
	    	self.game.apply_move(new_move)

    		if len(self.game.get_legal_moves())==0:
    			print("You lose! (AlphaBeta wins)")
    			break

	    	new_move = self.player2.get_move(self.game, 5.)
	    	self.game.apply_move(new_move)

	    	print(self.game.to_string())




if __name__ == '__main__':
    unittest.main()
