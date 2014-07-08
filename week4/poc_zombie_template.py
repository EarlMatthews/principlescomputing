"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
#import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for each_zombie in self._zombie_list:
            yield each_zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for each_human in self._human_list:
            yield each_human

    def _get_matrix(self, zero_list):
        """
             get the matrix of distance field.
        """
        max_value = self.get_grid_height() * self.get_grid_width()
        distance_field = [[max_value] * self.get_grid_width() \
            for dummy_idx in range(self.get_grid_height())]
        for cell in zero_list:
            distance_field[cell[0]][cell[1]] = 0
        return distance_field
    
    def _bfs(self, distance_field, start_queue, visted):
        """
            bfs to find the minimal distance.
        """
        while len(start_queue) != 0:
            current_cell = start_queue.dequeue()
            current_distance = distance_field[current_cell[0]][current_cell[1]]
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for each_cell in neighbors:
                row = each_cell[0]
                column = each_cell[1]
                if not visted[row][column] and self.is_empty(row, column):
                    visted[row][column] = True
                    distance_field[row][column] = min(distance_field[row][column], current_distance+1)
                    start_queue.enqueue((row, column))

    def _get_unvisted_matrix(self):
        """
            get not visted matrix.
        """
        visted = [[False] * self.get_grid_width() \
            for dummy_idx in range(self.get_grid_height())]
        return visted

    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        if entity_type == HUMAN:
            zero_list = self._human_list
        elif entity_type == ZOMBIE:
            zero_list = self._zombie_list
        distance_field = self._get_matrix(zero_list)
        for cell in zero_list:
            visted = self._get_unvisted_matrix()
            visted[cell[0]][cell[1]] = True
            start_queue = poc_queue.Queue()
            start_queue.enqueue(cell)
            self._bfs(distance_field, start_queue, visted)
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors = [cell for cell in neighbors if self.is_empty(cell[0], cell[1])]
            neighbors.append(human)
            neighbors.sort(key=lambda cell: zombie_distance[cell[0]][cell[1]], reverse=True)
            candidates = [neighbors[0]]
            max_distance = zombie_distance[neighbors[0][0]][neighbors[0][1]]
            for cell in neighbors[1:]:
                if zombie_distance[cell[0]][cell[1]] != max_distance:
                    break
                candidates.append(cell)
            choice = random.choice(candidates)
            new_human_list.append(choice)
        self._human_list = new_human_list

    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors = [cell for cell in neighbors if self.is_empty(cell[0], cell[1])]
            neighbors.append(zombie)
            neighbors.sort(key=lambda cell:human_distance[cell[0]][cell[1]])
            candidates = [neighbors[0]]
            min_distance = human_distance[neighbors[0][0]][neighbors[0][1]]
            for cell in candidates[1:]:
                if human_distance[cell[0]][cell[1]] != min_distance:
                    break
                candidates.append(cell)
            choice = random.choice(candidates)
            new_zombie_list.append(choice)
        self._zombie_list = new_zombie_list



# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))
