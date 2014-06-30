"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
     This function takes a current board and the next player to move.
    """
    win_state = board.check_win()
    while win_state is None:
        empty = board.get_empty_squares()
        choose_square = random.choice(empty)
        board.move(choose_square[0], choose_square[1], player)
        player = provided.switch_player(player)
        win_state = board.check_win()

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists)
    with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game,
    and which player the machine player is.
    """
    if board.check_win() is None:
        return
    if board.check_win() == provided.DRAW:
        return
    if board.check_win() == player:
        inplace_value = MCMATCH
        uninplace_value = -MCOTHER
    else:
        inplace_value = -MCMATCH
        uninplace_value = MCOTHER
    dimension = board.get_dim()
    for row in range(dimension):
        for column in range(dimension):
            state = board.square(row, column)
            if state == player:
                scores[row][column] += inplace_value
            elif state == provided.EMPTY:
                pass
            else:
                scores[row][column] += uninplace_value

def get_best_move(board, scores):
    """
    This function takes a current board
    and a grid of scores.
    """
    condidate = []
    max_score = None
    dimension = board.get_dim()
    for row in range(dimension):
        for column in range(dimension):
            if board.square(row, column) != provided.EMPTY:
                continue
            current_score = scores[row][column]
            if len(condidate) == 0:
                max_score = current_score
                condidate = [(row, column)]
            elif current_score > max_score:
                max_score = current_score
                condidate = [(row, column)]
            elif current_score == max_score:
                condidate.append((row, column))
    return random.choice(condidate)

def _get_empty_score(dimension):
    """
    Get the scores board(list of lists).
    """
    scores = []
    for dummy_count in range(dimension):
        scores.append([0] * dimension)
    return scores


def mc_move(board, player, trials):
    """
    This function takes a current board,
    which player the machine player is,
    and the number of trials to run.
    """
    scores = _get_empty_score(board.get_dim())
    for dummy_count in range(trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
#http://www.codeskulptor.org/#user35_M53C5z0WRj_2.py
