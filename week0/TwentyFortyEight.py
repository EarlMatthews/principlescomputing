'''
    This class is a simple implement of 2048 game.
'''
#! /usr/bin/python
#-*- coding=utf-8 -*-
#import poc_2048_gui        

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    is_merged = False
    result = []
    last_num = 0
    index = 0
    for index in range(len(line)):
        if line[index] != 0:
            last_num = line[index]
            break

    if last_num == 0:
        return line

    for next_index in range(index+1, len(line)):
        if line[next_index] == 0:
            continue
        if is_merged:
            last_num = line[next_index]
            is_merged = False
        elif last_num == line[next_index]:
            result.append(last_num*2)
            is_merged = True
        else:
            result.append(last_num)
            last_num = line[next_index]

    if is_merged == False:
        result.append(last_num)

    result.extend([0]*(len(line)-len(result)))

    return result

class TwentyFortyEight(object):
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height = grid_height
        self.width = grid_width
        self.grid = None
        self.direction = {}
        self._initial_direction()
        self.reset()

    def _initial_direction(self):
        """
            Initialize the start direction list
        """
        # initial up and down
        tmp_list_up = []
        tmp_list_down = []
        for column in range(self.width):
            tmp_list_up.append((0, column))
            tmp_list_down.append((self.height-1, column))
        self.direction[UP] = tmp_list_up
        self.direction[DOWN] = tmp_list_down

        #initial left and right
        tmp_list_left = []
        tmp_list_right = []
        for row in range(self.height):
            tmp_list_left.append((row, 0))
            tmp_list_right.append((row, self.width-1))
        self.direction[LEFT] = tmp_list_left
        self.direction[RIGHT] = tmp_list_right

    def get_direction(self):
        """
            get initial direction of the tiles.
            This method is create for test purpose.
        """
        result = []
        result.append(self.direction[UP]) 
        result.append(self.direction[DOWN])     
        result.append(self.direction[LEFT])  
        result.append(self.direction[RIGHT]) 
        return result

    def set_grid(self, grid):
        """
            set grid.
            This method is created for test purpose.
        """
        self.grid = grid
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        self.grid = []
        for dummy_row in range(self.height):
            self.grid.append([0]*self.width)
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        grid = self.grid
        self.reset()
        initial_tiles = self.direction[direction]
        offset = OFFSETS[direction]
        for tile in initial_tiles:
            operate_list = []
            line = []
            while (0 <= tile[0] < self.height) and (0 <= tile[1] < self.width):
                operate_list.append(tile)
                line.append(grid[tile[0]][tile[1]])
                tile = (tile[0] + offset[0], tile[1] + offset[1])
            line = merge(line)
            for lino in range(len(line)):
                row, column = operate_list[lino]
                self.set_tile(row, column, line[lino])
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        import random
        possible_select = []
        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column] == 0:
                    possible_select.append((row, column))
        if len(possible_select) == 0:
            return
        choice = random.choice(possible_select)
        two_four = random.randint(1, 10)
        if two_four == 10:
            #self.grid[choice[0]][choice[1]] = 4
            self.set_tile(choice[0], choice[1], 4)
        else:
            #self.grid[choice[0]][choice[1]] = 2
            self.set_tile(choice[0], choice[1], 2)
            
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grid[row][col]
 
# if __name__ == '__main__':
#     merge([2, 0, 2, 4])
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
