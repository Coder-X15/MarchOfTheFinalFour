# MarchOfThFinalFour.py

from time import *

# 'March of The Final Four' - a clone of chess

player_piece = 'Φ' # player's piece
computer_piece = 'τ' # computer's piece

class PlayTable:
    def __init__(self, table_side):
        ''' generates the game board, empty and with no pieces '''
        self.length = table_side
        self.table = [[0]*table_side]*table_side

    def __repr__(self):
        '''prints the table'''
        print()
        table_str = ''
        num = 0
        for row in self.table:
            table_str += str(num) + " \t"
            for piece in row:
                table_str += str(piece) + "|"
            table_str += "\n"
            num += 1
        return table_str + "\t0 1 2 3 4 5 6 7"
        
    def reset(self):
        ''' resets the board/ places pieces on it '''
        for row in [0, 1] :
            self.table[row] = [computer_piece]*self.length

        for row in [self.length-2, self.length - 1] :
            self.table[row] = [player_piece]*self.length
        
        for row in range(2, self.length-2):
            self.table[row] = [0]*self.length
    def move_piece(self, coord, turn = 'player'):
        '''moves the piece at coord '''
        if self.table[coord[1]][coord[0]] != 0 and self.table[coord[1] + (1 if turn == 'computer' else -1)][coord[0]] == 0:
            temp = self.table[coord[1]][coord[0]]
            self.table[coord[1]][coord[0]] = 0
            direction = 1 if turn == 'computer' else -1
            self.table[coord[1]+direction][coord[0]] = temp
            print(f"Moved {temp} from {(coord[0],coord[1])}") # msg
        elif self.table[coord[1]][coord[0]] == 0 or self.table[coord[1] + (-1)**(1 if turn == 'player' else 1)][coord[0]] != 0:
            return 'invalid move'
        
        
board = PlayTable(8)
board.reset()
print(board)
