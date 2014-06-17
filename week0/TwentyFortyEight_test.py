'''
    A simple test for twentyfortyeight
'''
import poc_simpletest
from TwentyFortyEight import TwentyFortyEight
from TwentyFortyEight import DOWN, LEFT, RIGHT, UP

def merge_test(suite):
    '''
        Test method merge
    '''
    from TwentyFortyEight import merge
    suite.run_test(str(merge([2, 0, 2, 4])), str([4, 4, 0, 0]), "merge 1")
    suite.run_test(str(merge([0, 0, 2, 2])), str([4, 0, 0, 0]), "merge 2")
    suite.run_test(str(merge([2, 2, 0, 0])), str([4, 0, 0, 0]), "merge 3")
    suite.run_test(str(merge([2, 2, 2, 2])), str([4, 4, 0, 0]), "merge 4")
    suite.run_test(str(merge([8, 16, 16, 8])), str([8, 32, 8, 0]), "merge 5")

def initial_test(suite):
    """
        Test class initialize
    """
    game = TwentyFortyEight(4, 4)
    result = [[(0, 0), (0, 1), (0, 2), (0, 3)], \
        [(3, 0), (3, 1), (3, 2), (3, 3)], \
        [(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 3), (1, 3), (2, 3), (3, 3)]]
    suite.run_test(str(game.get_direction()), str(result), "initial 1")

def move_test(suite):
    """
        Test move function
    """
    game = TwentyFortyEight(4, 4)
    grid = [[2, 4, 2, 4], [0, 2, 16, 2], [4, 16, 2, 4], [2, 4, 2, 4]]
    result = [[0, 4, 0, 0], [2, 2, 2, 4], [4, 16, 16, 2], [2, 4, 4, 8]]
    game.set_grid(grid)
    game.move(DOWN)
    suite.run_test(str(game), str(result), "Move 1")

    game.reset()
    result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    suite.run_test(str(game), str(result), "move 2")

    grid = [[8, 4, 0, 0], [2, 4, 2, 0], [4, 0, 4, 0], [2, 4, 2, 0]]
    result = [[8, 8, 2, 0], [2, 4, 4, 0], [4, 0, 2, 0], [2, 0, 0, 0]]
    game.set_grid(grid)
    game.move(UP)
    suite.run_test(str(game), str(result), "Move 3")

    grid = [[8, 8, 2, 0], [2, 4, 4, 0], [4, 0, 2, 0], [2, 0, 0, 2]]
    result = [[16, 2, 0, 0], [2, 8, 0, 0], [4, 2, 0, 0], [4, 0, 0, 0]]
    game.set_grid(grid)
    game.move(LEFT)
    suite.run_test(str(game), str(result), "Move 4")

    grid = [[16, 2, 0, 0], [2, 8, 0, 0], [4, 2, 0, 2], [4, 0, 0, 0]]
    result = [[0, 0, 16, 2], [0, 0, 2, 8], [0, 0, 4, 4], [0, 0, 0, 4]]
    game.set_grid(grid)
    game.move(RIGHT)
    suite.run_test(str(game), str(result), "Move 4")

def move_rectangle_test(suite):
    """
     Test rectange game.
    """
    game = TwentyFortyEight(4, 5)
    grid = [[0, 2, 4, 2, 4], [2, 2, 4, 0, 0], [2, 4, 0, 0, 0], [2, 2, 2, 0, 4]]
    result = [[4, 4, 8, 2, 8], [2, 4, 2, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 0]]
    game.set_grid(grid)
    game.move(UP)
    suite.run_test(str(game), str(result), "Move rectange 1")

    grid = [[4, 4, 8, 2, 8], [2, 4, 2, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 0]]
    result = [[8, 8, 2, 8, 0], [2, 4, 2, 0, 0], [2, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    game.set_grid(grid)
    game.move(LEFT)
    suite.run_test(str(game), str(result), "Move rectange 2")

    grid = [[8, 16, 8, 16, 8],
            [16, 8, 16, 8, 16],
            [8, 16, 8, 16, 8],
            [16, 8, 16, 8, 16]]
    game.set_grid(grid)
    game.move(UP) 


def new_tile_test():
    """
        tile test.
    """
    game = TwentyFortyEight(4, 4)
    game.reset()

    game.new_tile()
    print game

    game.new_tile()
    print game

def run_test():
    """
    Some informal testing code
    """
    suite = poc_simpletest.TestSuite()
    merge_test(suite)
    initial_test(suite)
    move_test(suite)
    move_rectangle_test(suite)
    suite.report_results()
    new_tile_test()

if __name__ == '__main__':
    run_test()
