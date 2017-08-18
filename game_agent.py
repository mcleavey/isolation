import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """ 
    This used to be    diff_dist_full_subt(game, player) 
    It appears as that throughout heuristic_analysis.pdf, but 
    I promoted it to custom_score for submission.  

    It increases win rates on average by 4% over AB_Improved

    Calculate the heuristic value of a game state from the point of view
    of the given player.

    Heuristic
    ---------
    Consider the number of available legal moves to the player, minus the number
    of available legal moves to the opponent.  Subtract a penalty for choosing a 
    square far from the center (based on the number of steps away from the center,
    so that moves in the corners are most heavily penalized)

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #Diff determines the relative advantage of the player's number of options
    # over the opponent's number

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    #Dist measures the number of steps away from the center space. Corners are
    #most heavily penalized.

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = abs(h - y) + abs(w - x)

    return diff-.6*dist



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.


    Heuristic
    ----------
    This uses stages (based on the number of blank spaces available) to change
    strategy throughout the game.  

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")



    blank_spaces = game.get_blank_spaces()


# Early in the game, use the strategy of AB_Center, since that seems to be an effective
#  agent

    if len(blank_spaces)>34:
        w, h = (game.width-1) / 2., (game.height-1) / 2.
        y, x = game.get_player_location(player)
        return (h-y)**2 + (w-x)**2


# Midgame, switch to the strategy of AB_Improved
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves) - len(opp_moves)

    if len(blank_spaces)>16:
        return diff


# At the end, use check_future_steps to look for the moves that let the player survive the 
#  largest number of future turns (steps)

    MAX_STEPS = 6
    own_max_steps = 1

    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            return num_steps + diff/4.

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    return own_max_steps+diff/4.



def custom_score_3(game, player):
    """
    In the runs, this is listed as "AB_Custom", but I demoted it to custom_score_3
    since it did not perform as well as Diff_dist_subt


    Calculate the heuristic value of a game state from the point of view
    of the given player.

    Heuristic
    ---------
    Define stages of the game (based on the number of blank spaces remaining on the board)
    Use different tactics based on whether it is early stage or late stage

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")



    # Diff is the relative advantage of the player's number of options
    # minus the opponent's number of options
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    #Dist is the number of steps away from the center 

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))

    #Determine what stage of the game you're in
    blank_spaces = game.get_blank_spaces()    
    num_spaces = len(blank_spaces)


    #Early on use dist (imitating how AB_Center seems to win often)
    if num_spaces>40:
        return dist + diff/8.

    #In mid game, use diff (imitating AB_Improved)
    if num_spaces>24:
        return diff + dist/8.

    if num_spaces<2:
        return 1

    #In late game, look for the longest available run
    #First use a lower MAX_STEPS to keep the heuristic fast
    if num_spaces>16:
        MAX_STEPS = 4
    else:
        #Later just try to find the absolute best step
        MAX_STEPS = 6

    own_max_steps = 1
    opp_max_steps = 1


    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        #Choose a future move and remove that from blank_spaces - this avoids the
        # slowness of having to create a copy of the board (through the options in isolation.py)
        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    #If you're earlier on, just return the length of one's own best run,
    # to be faster.  Adding in diff/5 to break the tie in case more
    # than one option has a long run remaining

    if len(blank_spaces)>16:
        return own_max_steps+diff/5.

    #Towards the end of the game, also check how long the opponent's run
    # could be (this gives more weight to choosing an option that blocks the
    #  opponent, but is slower and might be a disadvantage in iterative deepining
    #  in that you can't search as many levels deep)
    for mo in opp_moves:
        blank_spaces.remove(mo)
        num_steps = check_future_steps(mo, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            opp_max_steps = MAX_STEPS
            blank_spaces.append(mo)
            break

        blank_spaces.append(mo)

        if num_steps>opp_max_steps:
            opp_max_steps = num_steps


    return own_max_steps-opp_max_steps+diff/5.








# Now a series of options that are all slight variations of custom_score (where 
# Diff and Dist are combined with various weights)

def diff_dist_calculator(game, player, weight):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #Diff is one's own available legal moves minus the opponent's available legal moves
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    #Dist is the number of steps away from the center square of the board
    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = abs(h - y) + abs(w - x)

    return diff+weight*dist

def diff_dist_sum(game, player):
    return diff_dist_calculator(game, player, .3)
    

def diff_dist_subt(game, player):
    return diff_dist_calculator(game, player, -.3)


def diff_dist_eq_subt(game, player):
    return diff_dist_calculator(game, player, -1)


def diff_dist_half_subt(game, player):
    return diff_dist_calculator(game, player, -.5)
    

def diff_dist_dbl_subt(game, player):
    return diff_dist_calculator(game, player, -2)



def diff_dist_dbfive_subt(game, player):
    return diff_dist_calculator(game, player, -2.5)

def diff_dist_trp_subt(game, player):
    return diff_dist_calculator(game, player, -3)

def diff_dist_half_sum(game, player):
    return diff_dist_calculator(game, player, .5)

def diff_dist_pteight_sum(game, player):
    return diff_dist_calculator(game, player, .8)


def diff_sqdist_sum(game, player):
    # Use normal distance (here it's actually distance squared, since there's no
    # advantage to then taking a square root) instead of
    # counting the steps away.

    # Use a similar combination of Diff + Dist as in the previous several functions

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = (h - y)**2 + (w - x)**2

    return diff+.2*dist





def check_future_steps(move, curr_steps, MAX_STEPS, player, blank_spaces=[]):
    """
    Do a look ahead to determine how many steps the player could take (ie the number
    of future turns you could make before forfeiting.)

    This is similar to the overall minimax search, but it attempts to be faster in two ways:
    first, it only considers the player's moves, it doesn't look at what the opponent might do
    second, it keeps track of the available blank spaces without creating a copy of the board each
    time (the way the minimax functions do when they use forecast_move in isolation.py)

    Parameters
    ----------
    move : position on the board
        The current move being imagined

    curr_steps : integer
        Number of future turns one has already looked ahead

    MAX_STEPS : integer
        Max number of future turns to consider (ie, only check if the player could survive
        at least 5 future turns, when actually the player could survive 8).  This is to save time.

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    blank_spaces : array of board spaces
        Spaces still available on the board (the spaces in the current imaginary run have
        already been taken out)


    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    player.isTimeout()

    if len(blank_spaces)==0:
        return curr_steps-1

    #Copied from isolation.py, the way to determine the future possible legal moves
    r, c = move
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if (r + dr, c + dc) in blank_spaces]

    # If we've hit the MAX_STEPS we want to consider, return with the result
    if curr_steps == MAX_STEPS:
        if len(valid_moves)>0:
            return MAX_STEPS
        else:
            return MAX_STEPS-1

    # If we've run out of moves, return
    if len(valid_moves)==0:
        return curr_steps-1

    own_max_steps = curr_steps-1

    # Consider the available remaining moves. For each one, figure out how long a run you could create
    for m in valid_moves:
        # Remove the chosen move from the list of blank spaces (we do this to avoid the deep copy of the board)
        blank_spaces.remove(m)
        num_steps = check_future_steps(m, curr_steps+1, MAX_STEPS, player, blank_spaces)
        # Return the space to the list and go on to consider a different move
        blank_spaces.append(m)

        # If you've successfully found a run with MAX STEPS, return that 
        if num_steps == MAX_STEPS:
            return num_steps
        
        #If you've found a more successful run, replace your previous best
        if num_steps > own_max_steps:
            own_max_steps = num_steps

    return own_max_steps





class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=30, score_fn=custom_score, timeout=35.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """


    def isTimeout(self):
        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def maxvalue(self, game, max_depth, curr_depth):
        """
        Search for the branch with the highest score value.  Return that value.

        Parameters
        ---------------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        max_depth: int
            The maximum number of plies to check (this remains the same for
            Minimax, and will increase on each run in the AlphaBetaPlayer 
            which uses iterative deepening)

        curr_depth: int
            The current depth being checked (incremented on each call until it reaches
            max_depth)

        Returns
        -----------------
        val : int
            The score for the best move available (the maximum given all the legal moves available)
        """

        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

        # Reached the depth we wanted to consider. Return the score for that
        #   move (based on the heuristics in improved_score, or custom_score)
        if (max_depth==curr_depth):
            return self.score(game, self)
        else:

            # Increase depth counter for when we next call minvalue
            curr_depth+=1
            moves = game.get_legal_moves(self)
            if len(moves)==0:
                # No legals moves left, player would lose if we chose this branch
                return float("-inf")

            best_move = moves[0]
            maxv=float("-inf")

            # Consider each move. If it returns a higher predicted value than
            #   what was previously stored in best_move, replace best_move and maxv
            for m in moves:
                val = self.minvalue(game.forecast_move(m), max_depth, curr_depth)
                if (val>maxv):
                    maxv = val
                    best_move = m    
            return maxv

    

    def minvalue(self, game, max_depth, curr_depth):
        """
        Search for the branch with the highest score value.  Return that value.

        Parameters
        ---------------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        max_depth: int
            The maximum number of plies to check (this remains the same for
            Minimax, and will increase on each run in the AlphaBetaPlayer 
            which uses iterative deepening)

        curr_depth: int
            The current depth being checked (incremented on each call until it reaches
            max_depth)

        Returns
        -----------------
        val : int
            The score for the best move available (the maximum given all the legal moves available)
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Reached the depth we wanted to consider. Return the score for that
        #   move (based on the heuristics in improved_score, or custom_score)
        if (max_depth==curr_depth):
            return self.score(game, self)
        else:
            # Increase depth counter for when we next call maxvalue
            curr_depth+=1

            moves = game.get_legal_moves()
            if len(moves)==0:
                #no legal moves left for opponent, opponent would lose on this branch
                return float("+inf")

            best_move = moves[0]
            minv=float("inf")

            # Consider each move. If it returns a lower predicted value than
            #   what was previously stored in best_move, replace best_move and minv            
            for m in moves:
                val = self.maxvalue(game.forecast_move(m), max_depth, curr_depth)
                if (val<minv):
                    minv = val
                    best_move = m     
            return minv



    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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


        moves = game.get_legal_moves()

        if len(moves)==0:
            best_move = (-1, -1)   # no moves left, forfeit game

        else:              
            best_move = moves[0]
            maxval=float("-inf")

            # We're not doing iterative deepening, so we put the try/except around 
            #  testing each move. If we run out of time, we return the best move that
            #  we've found so far.

            for m in moves:
                try:
                    val = self.minvalue(game.forecast_move(m), depth, 1)
            
                except SearchTimeout:
                    return best_move
                
                if val>maxval:
                    maxval = val
                    best_move = m    


        return best_move



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def isTimeout(self):
        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()

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


        while depth <= self.search_depth:   
            try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth)
                depth+=1

            except SearchTimeout:
#                print("Timeout- spaces remaining: ", len(game.get_blank_spaces()))
                return best_move


#        print("Spaces remaining: ", len(game.get_blank_spaces()))
        # Return the best move from the last completed search iteration
        return best_move



    def maxvalue(self, game, alpha, beta, max_depth, curr_depth):
        """
        Search for the branch with the highest score value.  Return that value.

        Parameters
        ---------------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        alpha : float
            The low end of alpha-beta pruning -- while you are in minvalue() function,
            if minv is lower than this, you know this branch won't get considered in the
            maxvalue node above it, so you can stop testing
            
        beta : float
            The high end of alpha-beta pruning -- while you are in maxvalue() function, 
            if maxv is higher than this, you know this branch won't get considered in the 
            minvalue node above it, so you can stop testing 

        max_depth: int
            The maximum number of plies to check (this remains the same for
            Minimax, and will increase on each run in the AlphaBetaPlayer 
            which uses iterative deepening)

        curr_depth: int
            The current depth being checked (incremented on each call until it reaches
            max_depth)

        Returns
        -----------------
        val : float
            The score for the best move available (the maximum given all the legal moves available)
        """

        if self.time_left() < self.TIMER_THRESHOLD:
           raise SearchTimeout()


        # Reached the depth we wanted to consider. Return the score for that
        #   move (based on the heuristics in improved_score, or custom_score)
        if (max_depth==curr_depth):
            return self.score(game, self)

        else:
            # Increase depth counter for when we next call minvalue
            curr_depth+=1
            moves = game.get_legal_moves(self)
            if len(moves)==0:
                # No legals moves left
                return float("-inf")
            
            maxv = float("-inf")

            # Consider each move. If it returns a higher predicted value than
            #   what was previously stored in best_move, replace maxv

            for m in moves:
                val = self.minvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val>maxv:
                    maxv = val

                # Check if maxv is more than beta - this means it is more than a neighboring node, and the
                # minvalue above will never choose this branch. You can stop searching this branch and 
                # return upwards.
                if maxv >= beta:
                    return maxv

                # Need to continue searching this branch. If maxv is higher than the previously saved alpha,
                #  set alpha to be equal to this new max
                else:
                    alpha = max(alpha, maxv) 

            return maxv


    def minvalue(self, game, alpha, beta, max_depth, curr_depth):
        """
        Search for the branch with the highest score value.  Return that value.

        Parameters
        ---------------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        alpha : float
            The low end of alpha-beta pruning -- while you are in minvalue() function,
            if minv is lower than this, you know this branch won't get considered in the
            maxvalue node above it, so you can stop testing
            
        beta : float
            The high end of alpha-beta pruning -- while you are in maxvalue() function, 
            if maxv is higher than this, you know this branch won't get considered in the 
            minvalue node above it, so you can stop testing 

        max_depth: int
            The maximum number of plies to check (this remains the same for
            Minimax, and will increase on each run in the AlphaBetaPlayer 
            which uses iterative deepening)

        curr_depth: int
            The current depth being checked (incremented on each call until it reaches
            max_depth)

        Returns
        -----------------
        val : float
            The score for the best move available (the maximum given all the legal moves available)
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Reached the depth we wanted to consider. Return the score for that
        #   move (based on the heuristics in improved_score, or custom_score)
        if (max_depth==curr_depth):
            return self.score(game, self)
        else:
            # Increase depth counter for when we next call maxvalue
            curr_depth+=1

            moves = game.get_legal_moves()
            if len(moves)==0:
                #no legal moves left for opponent, opponent would lose on this branch
                return float("+inf")

            minv = float("inf")

            # Consider each move. If a given move returns a lower predicted value than
            #   what was previously found, replace minv
            for m in moves:
                val = self.maxvalue(game.forecast_move(m), alpha, beta, max_depth, curr_depth)
                if val < minv:
                    minv = val

                # Check if minv is less than alpha - this means it is less than a neighboring node, and the
                # maxvalue above will never choose this branch. You can stop searching this branch and 
                # return upwards.
                if minv <= alpha:
                    return minv

                # Need to continue searching this branch. If minv is lower than the previously saved beta,
                #  set beta to be equal to this new min
                else:
                    beta = min(beta, minv)
            return minv


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
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


        moves = game.get_legal_moves()
        if len(moves)==0:    # no legal moves available, forfeit the game
            return (-1, -1)
             
        best_move = moves[0]
        maxval=float("-inf")

        # Consider each available move, and select the move with the highest
        #   score (returned from searching the tree "depth" nodes down)
        #   Each time this alphabeta() function is called, depth will be one
        #   higher, and the search will be that much deeper

        for m in moves:
            val = self.minvalue(game.forecast_move(m), alpha, beta, depth, 1)
                
            if val>maxval:
                maxval = val
                best_move = m    

            # Increase alpha to the max value already found - this way minvalue() 
            #  can stop searching if it knows it will return a value lower than
            #  a max that was already found
            alpha = max(alpha, maxval)

        return best_move


