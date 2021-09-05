from math import *
from random import *
import MarchOfTheFinalFour as mff

######################
##Bug fixes required:

##1. The machine player has to somehow adjust its moves in case errors come up as well as when the move it chooses turns invalid

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

def neighbourhood(coords):
    '''generates the 3 x 3 grid that forms the neighbourhod of the required square'''
    axial_neighbours =  [(coords[0] + 1, coords[1]),(coords[0] - 1, coords[1]),
                        (coords[0], coords[1] + 1), (coords[0], coords[1] - 1)] # neighbours along NEWS directins
    diagonal_neighbours = [(coords[0] + 1, coords[1]+1),(coords[0] - 1, coords[1] - 1),
                           (coords[0]-1, coords[1] + 1), (coords[0]+1, coords[1] - 1)] #diagonal neighbours
    neighbours = axial_neighbours + diagonal_neighbours
    return neighbours

########################

# The NPC's brain

class NPC_Brain:
    '''brain of the NPC ;), actually a single-layer perceptron '''
    def __init__(self,board_size):
        ''' Initialiser'''
        self.inputs = board_size # no. of input nodes for the neural network
        self.weights = [random() for i in range(self.inputs)] # random weights for each game
        self.column_scores = [] # column scores (for each column) - the 'liking' of the computer to move a piece in a column as the output
                                # of the neural network's processing 
        self.inputs_template = [] # a container to hold the inputs to the neural network
    def process(self, board, threshold):
        '''forward-feeding'''
        # we begin by setting the lists to zero so as to make the computer forget the past state of the board and to look for the current state
        self.inputs_template = [] 
        self.column_scores = []
        self.row_scores = []
        for column in range(self.inputs):
            scores = [1 if row[column] == mff.player_piece else 0 for row in board] # checking for enemies in each column
            self.inputs_template.append(scores) 
            score = sig(multiply(scores, self.weights)/threshold) # using the logistic sigmoid function to generate a liking for columns :D
            self.column_scores.append(score) # each column score is appended
        return self.column_scores
    def back_prop(self, learning_rate, target = 1):
        '''Back-propagation, with error function as squared-error function (target - error)**2'''
        for row in self.inputs_template:
            for i in range(self.inputs):
                '''overfitting can occur, but still let's try this'''
                self.weights[i] -= learning_rate * 2 * (self.column_scores[i] - target) * (self.column_scores[i]*(1-self.column_scores[i])) * row[i] #backprop formula
        print("Model has been trained") # a msg to make sure all's fine here
                
    
        

class NPC:
    ''' non-playable character / computerized player class '''
    def __init__(self):
        self.mind = NPC_Brain(mff.board.length) # the model
        self.piece_lower = 0; self.piece_upper = 1 # initial row numbers of the computer's pieces 
        
    def make_move(self):
        columns = temp = self.mind.process(mff.board.table, 0.5) # feeding forward
        x_coord = columns.index(max(columns)) # choosing the column the compute likes the most
        y_coord = randint(self.piece_lower, self.piece_upper) % mff.board.length # a random y coordinate is chosen
        moved = False
        while not moved:
            if mff.board.table[(int(y_coord) + 1) % mff.board.length][int(x_coord)] == 0 and (mff.board.table[int(y_coord)][int(x_coord)] not in  [0, mff.player_piece]):
                mff.board.move_piece((int(x_coord), int(y_coord)), turn = 'computer')
                self.mind.back_prop(0.5) # making the computer learn from its decision
                self.piece_upper += 1 #increasing the upper limit of the y coordinate by 1
                moved = True
            else:
                # trying to avoid the computer's confusion
                grid = neighbourhood((x_coord,y_coord)) # taking the 3 x 3 grid around that set of coordinates
                # gonna check through all the squares in the  3 x 3 grid in the following code
                for place in grid:
                    x_coord = place[1]
                    y_coord = place[0]
                    print("Tested:", (x_coord,y_coord), end = ';')
                    if  mff.board.table[place[1]][place[0]] == mff.computer_piece and mff.board.table[(place[1] + 1) % mff.board.length][place[0]] not in  [0, mff.player_piece]:
                        value = mff.board.move_piece((place[0],place[1]), turn = 'computer') # it moves the piece if it ever feels that it's all right to move it forward
                        moved = True if value == None else False # ensuring that the loop can be safely broken  
                        break
                if not moved:
                    x_coord += (-1)**(2 if x_coord in [0,mff.board.length-1] else 1)
                    y_coord += (-1)**(2 if x_coord in [0,mff.board.length-1] else 1)
                    
            
                


npc = NPC() # creating the NPC

## Sample gamplay
## The following gameplay will be a bit smooth in the beginning but turns into a confusion later

while True:
    # infinite loop here till errors occur
    player_mv = eval(input("Enter your move:")) # waiting for the player's move
    value = mff.board.move_piece(player_mv)
    # next we check if the player's move was valid
    if value == None: 
        print(mff.board)
        npc.make_move()
        print(mff.board)
    else:
        print("Invalid move")
        
    
    
            
        
        
