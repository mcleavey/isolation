#  Heuristics that I tested early on.  Some appear in the charts of heuristic_analysis.pdf, so I keep them here for reference.
#  I don't recommend using any.

from heuristics import check_future_steps





#These are early heuristics that were not successful

def dist_diff_score(game, player):
    #Use DIST for the first half of the game, DIFF for the end
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
    if len(game.get_blank_spaces())>30:
        w, h = (game.width-1) / 2., (game.height-1) / 2.
        y, x = game.get_player_location(player)
        return float(abs(h - y) + abs(w - x))
    else: 
        own_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))
        return float(len(own_moves)-len(opp_moves))


def diff_dist_score(game, player):
    #USE DIFF for the first half of the game, DIST for the end
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
#    print("In stages_score: num_spaces is ", num_spaces, " dist is ", dist," and diff is ",diff)
    if len(game.get_blank_spaces())>30:
        own_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))
        return float(len(own_moves)-len(opp_moves))
    else: 
        w, h = (game.width-1) / 2., (game.height-1) / 2.
        y, x = game.get_player_location(player)
        return float(abs(h - y) + abs(w - x))        






def adv_stages_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()

    num_spaces = len(blank_spaces)  

    if num_spaces>44:
        return 1

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))
      

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)



    if num_spaces>16:
        return diff - dist/2.


    if num_spaces<2:
        return 1

    MAX_STEPS = 5

    own_max_steps = 1
    opp_max_steps = 1


    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    if len(blank_spaces)>8:
        return own_max_steps+diff/5.

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




def next_step_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))
    
    num_spaces = len(blank_spaces)
     

    if num_spaces<2:
        return 1

    MAX_STEPS = 5

    own_max_steps = 1
    opp_max_steps = 1
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    if len(blank_spaces)>20:
        return own_max_steps+dist/5.

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


    return own_max_steps-opp_max_steps-dist/5


def mod_stages_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()



    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))
    
    num_spaces = len(blank_spaces)
    
    if num_spaces>40:
        return float(dist)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    if num_spaces>30:
        return diff + dist/2.

    if num_spaces>17:
        return diff

    if num_spaces<2:
        return 1

    MAX_STEPS = 6

    own_max_steps = 1
    opp_max_steps = 1


    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    if len(blank_spaces)>16:
        return own_max_steps+diff/5.

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

def diff_late_game(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()

    num_spaces = len(blank_spaces)  

    if num_spaces>44:
        return 1

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))
      

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)



    if num_spaces>24:
        return diff - dist/2.

    if num_spaces<12:
        return diff



    MAX_STEPS = 5

    own_max_steps = 1
    opp_max_steps = 1


    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

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



def stages_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    diff = len(own_moves)-len(opp_moves)

    w, h = (game.width-1) / 2., (game.height-1) / 2.
    y, x = game.get_player_location(player)
    dist = float(abs(h - y) + abs(w - x))
    
    num_spaces = len(blank_spaces)
    
    player.isTimeout()

    if num_spaces>40:
        return dist + diff/2.

    if num_spaces>30:
        return diff + dist/4.

    if num_spaces>20:
        return diff+dist/8.

    if num_spaces<2:
        return 1

    if num_spaces>16:
        MAX_STEPS = 3
    else:
        MAX_STEPS = 7

    own_max_steps = 1
    opp_max_steps = 1


    for m in own_moves:

        blank_spaces.remove(m)
        num_steps = check_future_steps(m, 1, MAX_STEPS, player, blank_spaces)

        if num_steps==MAX_STEPS:
            own_max_steps = MAX_STEPS
            blank_spaces.append(m)
            break

        blank_spaces.append(m)

        if num_steps>own_max_steps:
            own_max_steps = num_steps

    if len(blank_spaces)>16:
        return own_max_steps+diff/5.

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


