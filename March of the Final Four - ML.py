from math import *
from random import *
import MarchOfTheFinalFour as mff
#####################
## March Of The Final Four - Sample Gameplay (not all rules coded)


######################
##Bug fixes required:

##No issues

######################
## Solutions : at the dooorstep, it seems... 
######################

## Math functions for our use in here
    
def multiply(list_a, list_b):
    '''matrix multiplication and addition'''
    list_res = [list_a[n] * list_b[n] for n in range(len(list_a))]
    return fsum(list_res)

def sig(x):
    '''logistic sigmoid function'''
    return exp(x)/(1+ exp(x))

##############################

## Neighbourhood search

def neighbourhood(coords, board_length):
    '''generates the 3 x 3 grid that forms the neighbourhod of the required square'''
    axial_neighbours =  [(coords[0] + 1, coords[1]),(coords[0] - 1, coords[1]),
                        (coords[0], coords[1] + 1), (coords[0], coords[1] - 1)] # neighbours along NEWS directins
    diagonal_neighbours = [(coords[0] + 1, coords[1]+1),(coords[0] - 1, coords[1] - 1),
                           (coords[0]-1, coords[1] + 1), (coords[0]+1, coords[1] - 1)] #diagonal neighbours
    neighbours = axial_neighbours + diagonal_neighbours # supposed neighbours
    ## purging those coordinates with negative values in them:
    for i in range(len(neighbours)):
        if (neighbours[i][0] < 0 or neighbours[i][0] > board_length - 1) or (neighbours[i][1] < 0 or neighbours[i][1] > board_length - 1):
            neighbours[i] = 0
    while 0 in neighbours:
        neighbours.remove(0)
    
    return neighbours

########################
# The NPC's brain

class NPC_Brain:
    '''brain of the NPC ;), actually a single-layer perceptron '''
    def __init__(self,board_size):
        ''' Initialiser'''
        self.inputs =  3 # no. of input nodes for the neural network
        self.board_size = board_size # side length of the board 
        #self.weights = [random() for i in range(self.inputs)] random weights for each game
        self.weights = [random() for i in range(self.inputs)]
        self.inputs_template = [] # a container to hold the inputs to the neural network
        self.scores = []
        
    def process(self, board):
        '''forward-feeding'''
        # we begin by setting the lists to zero so as to make the computer forget the past state of the board and to look for the current state
        self.inputs_template = []
        self.scores = []
        for i in range(self.board_size):
            column = []
            inputs_set = []
            for j in range(self.board_size):
                column.append(board[j][i]) # generating a column
            # now we check for features to score this column with
            # inputs order : [are_pieces_adjacent, proximity/8, enemy_index/8]
            if column.count(mff.computer_piece) == 2:
                # (case - 1: checking for two computer pieces)
                # checking for proximity between computer pieces   
                indices = []
                for piece in range(len(column)):
                    if column[piece] == mff.computer_piece:
                        indices.append(piece)
                    if column[piece] == mff.player_piece:
                        # checking for enemy pieces
                        indices.append(-piece)
                if indices[1] - indices[0] == 0:
                    inputs_set.append(0)
                else:
                    inputs_set.append(1)
                inputs_set.append((indices[1] - indices[0])/8) #proximity between computer pieces / 8
                if indices[len(indices)-1] < 0:
                    while indices[0]>0:
                        indices.pop(0)
                    inputs_set.append(fsum(indices)/(len(indices)*8)) # enemy piece index / 8
                self.inputs_template.append(inputs_set)
            self.scores.append(sig(multiply(inputs_set, self.weights)))
        return self.scores 
            
                
                
                
            
    
    def back_prop(self, learning_rate, target = 0):
        '''Back-propagation, with error function as squared-error function (target - error)**2'''
        for j in range(len(self.inputs_template)):
            for i in range(self.inputs):
                '''overfitting can occur, but still let's try this'''
                self.weights[i] += -learning_rate * 2 * (self.scores[j] - target) * ((self.scores[j]**2)*(1-self.scores[j])) * self.inputs_template[j][i] #backprop formula
                
    
        

class NPC:
    ''' non-playable character / computerized player class '''
    def __init__(self):
        self.mind = NPC_Brain(mff.board.length) # the model
        self.piece_lower = 0; self.piece_upper = 1 # initial row numbers of the computer's pieces
        self.row_expanse = 2
        
    def make_move(self):
        moved = False
        req_target = -1
        counter = 1
        print("Thinking...")
        scores = []
        while not moved:
            scores = self.mind.process(mff.board.table)
            if counter < 50:
                x_coord = scores.index(max(scores))
            else:
                scores.pop(scores.index(max(scores)))
                x_coord = scores.index(max(scores))
            y_coord = randint(0, self.row_expanse)
            try:
                if mff.board.table[int(y_coord) + 1][int(x_coord)] == 0 and (mff.board.table[int(y_coord)][int(x_coord)] not in  [0, mff.player_piece]):
                    mff.board.move_piece((int(x_coord), int(y_coord)), turn = 'computer')
                    self.piece_upper += 1 #increasing the upper limit of the y coordinate by 1
                    moved = True
                    self.row_expanse += 1
                    print("Move made after ",counter,"iterations")
##                    self.mind.back_prop(0.686574, target = req_target)
                    counter = 1
            except mff.InvalidMove:
                # trying to avoid the computer's confusion
                slef.row_expanse -= 1 
                counter += 1
            except IndexError:
                self.row_expanse -= 1
                counter += 1
            if counter >= 100:
                self.mind.train(0.5,target = req_target)
                    
            
                
            
                


npc = NPC() # creating the NPC

## Sample gamplay
## The following gameplay will be a bit smooth in the beginning but turns into a confusion later
all_gone_good = True
while True:
    all_gone_good = True 
    # infinite loop here till errors occur
    player_mv = eval(input("Enter your move:")) # waiting for the player's move
    try:
        mff.board.move_piece(player_mv)
    except mff.InvalidMove:
        print("Invalid move")
        all_gone_good = False
    # next we check if the player's move was valid
    if all_gone_good:
        print(mff.board)
        npc.make_move()
        print(mff.board)
        
    
    
            
        
        
