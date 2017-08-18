"""
    I'm incluing this because I noticed the AlphaBetaPlayer wins more often if I modify 
    isolation.py to return get_legal_moves() in the same order each time (not randomized).
    I added an extra function get_legal_moves_non_randomized() into isolation.py to do this.
    I'm actually not sure why this works, but I ran hundreds of games overnight and it seemed
    to be a very repeatable pattern.  
"""

import random
from game_agent import (IsolationPlayer, SearchTimeout)

class AlphaBetaNonRandomPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left


       # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        # Test if first move of the game -- if so pick the center square
        if len(game.get_blank_spaces()) == game.width * game.height:
            return (3,3)

        moves = game.get_legal_moves_non_randomized()

        while depth <= self.search_depth:   
            try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth, moves)
                depth+=1

            except SearchTimeout:
                return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def maxvalue(self, game, alpha, beta, max_depth, curr_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

        if (max_depth==curr_depth):
            return self.score(game, self)
        else:
            curr_depth+=1
            moves = game.get_legal_moves_non_randomized(self)
            if len(moves)==0:
                # No legals moves left
                return float("-inf")
            maxv = float("-inf")
            for m in moves:
                val = self.minvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val>maxv:
                    maxv = val
                if maxv >= beta:
                    return maxv
                else:
                    alpha = max(alpha, maxv) 
            return maxv

    def minvalue(self, game, alpha, beta, max_depth, curr_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        if (max_depth==curr_depth):
            return self.score(game, self)
        else:
            curr_depth+=1
            moves = game.get_legal_moves_non_randomized()
            if len(moves)==0:
                #no legal moves left for opponent
                return float("+inf")
            minv = float("inf")
            for m in moves:
                val = self.maxvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val < minv:
                    minv = val
                if minv <= alpha:
                    return minv
                else:
                    beta = min(beta, minv)
            return minv


    def alphabeta(self, game, depth, moves, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if len(moves)==0:
            return (-1, -1)
             
        best_move = moves[0]
        maxval=float("-inf")
        for m in moves:
            val = self.minvalue(game.forecast_move(m), alpha, beta, depth, 1)
                
            if val>maxval:
                maxval = val
                best_move = m    

            alpha = max(alpha, maxval)

        return best_move




"""
An attempt to sort the moves into an order that would help alpha-beta pruning.
I stopped using this because it didn't beat the regular AlphaBetaPlayer with
no sorting.
"""
class AlphaBetaSortingPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left


       # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        # Test if first move of the game -- if so pick the center square
        if len(game.get_blank_spaces()) == game.width * game.height:
            return (3,3)

        moves = game.get_legal_moves()
#        print("Initially, moves are ", moves)
        while depth <= self.search_depth:   
            try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
#                print("********************Next round of iterative deepening: depth ", depth, ".  Current best move is ", best_move)
                best_move = self.alphabeta(game, depth, moves)
#                print("At depth ", depth, " best move is ", best_move)
                depth+=1

            except SearchTimeout:
#                print("AlphaBeta Non Sorting           timed out at depth ", depth," returning move ",best_move)
                return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def maxvalue(self, game, alpha, beta, max_depth, curr_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

        if (max_depth==curr_depth):
#            print(" "*curr_depth, "Depth max: Max value at depth ", curr_depth, " returning score ", self.score(game, self))
            return self.score(game, self)
        else:
            curr_depth+=1
            moves = game.get_legal_moves(self)
            if len(moves)==0:
                # No legals moves left
                return float("-inf")
            maxv = float("-inf")
            for m in moves:
                val = self.minvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val>maxv:
                    maxv = val
                if maxv >= beta:
                    return maxv
                else:
                    alpha = max(alpha, maxv) 
#            print(" "*(curr_depth-1), "Maxvalue depth ", curr_depth-1, " returning value ", maxv)
            return maxv

    def minvalue(self, game, alpha, beta, max_depth, curr_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        if (max_depth==curr_depth):
#            print(" "*curr_depth, "Depth max: Max value at depth ", curr_depth, " returning score ", self.score(game, self))
            return self.score(game, self)
        else:
            curr_depth+=1
            moves = game.get_legal_moves()
            if len(moves)==0:
                #no legal moves left for opponent
                return float("+inf")
            minv = float("inf")
            for m in moves:
                val = self.maxvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val < minv:
                    minv = val
                if minv <= alpha:
                    return minv
                else:
                    beta = min(beta, minv)
#            print(" "*(curr_depth-1), "Minvalue depth ", curr_depth-1, " returning value ", minv)
            return minv


    def alphabeta(self, game, depth, moves, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


#        moves = game.get_legal_moves()
        if len(moves)==0:
            return (-1, -1)
             

        best_move = moves[0]
        maxval=float("-inf")
#        for m in moves:
#            val = self.minvalue(game.forecast_move(m), alpha, beta, depth, 1)
                
#            if val>maxval:
#                maxval = val
#                best_move = m    

#            alpha = max(alpha, maxval)

        maxindex = 0
        for i in range(len(moves)):
#            print("Testing move ", i, " of ", len(moves),": ", moves[i])
            val = self.minvalue(game.forecast_move(moves[i]), alpha, beta, depth, 1)
#            print("Move ", moves[i], " has value ", val)
            if val>maxval:
                    best_move = moves[i]
                    moves.remove(best_move)
                    moves.insert(0, best_move)
                    maxval = val
            alpha = max(alpha, maxval)

#        maxindex = 0
#        for i in range(len(moves)):
#            print("Testing move ", i, " of ", len(moves),": ", moves[i])
#            val = self.minvalue(game.forecast_move(moves[i]), alpha, beta, depth, 1)
#            print("Move ", moves[i], " has value ", val)
#            if val>maxval:
#                    best_move = moves[i]
#                    moves.remove(best_move)
#                    moves.insert(0, best_move)
#                    maxval = val
#            alpha = max(alpha, maxval)

#        print("After alphabeta call, moves are: ", moves)

        return best_move
