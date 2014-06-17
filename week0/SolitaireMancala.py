'''
    SolitaireMancala class
    Author:@Honestman
'''
#! /usr/bin/python
#-*- coding=utf-8 -*-

class SolitaireMancala(object):
    '''
    A simple games
    '''
    def __init__(self):
        '''
        Create a SolitaireMancala object whose configuration 
        consists of a board with an empty store and no houses
        '''
        self.conf = [0]

    def set_board(self, configuration):
        '''
        Set the board to be a copy of the supplied configuration 
        '''
        self.conf = list(configuration)

    def __str__(self):
        '''
        Return a string corresponding to the current 
        configuration of the Mancala board.
        '''
        return str(self.conf[::-1])

    def get_num_seeds(self, house_num):
        '''
        Return the number of seeds in the house with index house_num.
        '''
        return self.conf[house_num]

    def is_legal_move(self, house_num):
        '''
        Return True if moving the seeds from house house_num is legal. 
        Otherwise, return False.
        '''
        if house_num == 0:
            return False
        return self.conf[house_num] == house_num

    def apply_move(self, house_num):
        '''
        Apply a legal move for house house_num to the board.
        '''
        if not self.is_legal_move(house_num):
            return
        self.conf[house_num] = 0
        for index in range(house_num):
            self.conf[index] += 1

    def choose_move(self):
        '''
        Return the index for the legal move whose 
        house is closest to the store. If no legal move is available, return 0.
        '''
        for index in range(1, len(self.conf)):
            if index == self.conf[index]:
                return index
        return 0

    def is_game_won(self):
        '''
        Return True if all houses contain no seeds. Return False otherwise.
        '''
        for index in range(1, len(self.conf)):
            if self.conf[index] != 0:
                return False
        return True

    def plan_moves(self):
        '''
        Given a Mancala game, return a list of legal moves
        computed to win the game if possible.
        '''
        steps = []
        mala = SolitaireMancala()   
        mala.set_board(self.conf)
        while not mala.is_game_won():
            possible_step = mala.choose_move()
            if possible_step == 0:
                return steps
            steps.append(possible_step)
            mala.apply_move(possible_step)
        return steps

if __name__ == '__main__':
    import poc_mancala_testsuite
    poc_mancala_testsuite.run_test(SolitaireMancala)


