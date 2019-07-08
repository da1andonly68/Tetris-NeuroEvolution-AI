import sys
import random
import numpy as np
import PIL
import pickle
import neat

#NEAT Setup
number_generations = 20
fitness_for_saving = 13

#Game Setup 
#Rows and Columns of the grid
ROW_COUNT = 24
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

tetris_shapes = [
    [[0, 1, 0],
     [1, 1, 1]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return np.rot90(shape)

def rotate_counter_clockwise(shape):
    np.rot90(shape)
    np.rot90(shape)
    return np.rot90(shape)

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                pass
    return False
    
def remove_row(board, row):
    del board[row]
    return [[0 for i in range(COLUMN_COUNT)]] + board

#moves game peice from being controlled by player to part of the heap
def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
    offset_x, offset_y = matrix_2_offset
    for cy, row in enumerate(matrix_2):
        for cx, val in enumerate(row):
            try:
                matrix_1[cy + offset_y - 1][cx + offset_x] += val
            except IndexError:
                pass
    return matrix_1


def new_board():
    board = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
    #a row is added at the very bottom for collision checking
    board += [[1 for x in range(COLUMN_COUNT)]]
    return board

#No graphics are generated
class Tetris:
    
    def __init__(self):
       
        self.board = None
        self.game_over = False
        self.score = 0
        self.setup()
        
    
    def new_stone(self):
        self.stone = random.choice(tetris_shapes)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        #Sets the number for the input for the AI that represents which shape is active
        if self.stone[0][0] != 0:
            self.shape = self.stone[0][0]
        else:
            self.shape = self.stone[1][1]
        self.shape /= 7

        self.rotation = 1

        #Ends game if top of board is collided into
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True
    
    def setup(self):
        self.board = new_board()
        self.new_stone()

    def drop(self):
        self.stone_y += 1
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
            while True:
                for i, row in enumerate(self.board[:-1]):
                    #if row full(Zeros represent empty space)
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        self.score += 1
                        break
                else:
                    break
            self.new_stone()

    def rotate_stone(self):
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone
                #Tracks the rotation of the shape for the AI input
                if self.rotation == 4:
                    self.rotation = 1
                else:
                    self.rotation += 1

    def rotate_stone_counter_clockwise(self):
        new_stone = rotate_counter_clockwise(self.stone)
        if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
            self.stone = new_stone
            if self.rotation == 1:
                self.rotation = 4
            else:
                self.rotation -= 1

    def move(self, delta_x):
        new_x = self.stone_x + delta_x
        if new_x < 0:
            new_x = 0
        if new_x > COLUMN_COUNT - len(self.stone[0]):
            new_x = COLUMN_COUNT - len(self.stone[0])
        if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
            self.stone_x = new_x

    def output_board(self):
        pixels = []
        for row in range(len(self.board) -1):#leaves out the pre-populated bottom row
            for column in range(len(self.board[0])):
                if self.board[row][column] != 0:
                    value = 1
                else:
                    value = 0
                pixels.append(value)
        return pixels

    def output_shape_location(self):
        #Scales the number from a small fraction to 1
        return [self.stone_x / 8, self.stone_y / 22]

    #The outputs are as follows: Current Shape, Shape Location, Shape Rotation, Grid Data 
    #Inputs to the AI
    def output_info(self):
        outputs = []
        outputs.append(self.shape)
        outputs.append(self.rotation)
        outputs.extend(self.output_shape_location())
        outputs.extend(self.output_board())
        return outputs

    def calculate_fitness(self):
        #Give partial credit for rows with 2 or more peices at end of game
        fitness = 0
        for row in range(len(self.board) -1):#leaves out the pre-populated bottom row
            total = 0
            for column in range(len(self.board[0])):
                if self.board[row][column] != 0:
                    total += 1
            if(total >= 5):
                fitness += (total / COLUMN_COUNT )
        #Bonus points for actually clearing rows
        fitness += self.score * 2
        return fitness

    #The AI can output 0 - 4. If zero, it does nothing
    def play_ai(self, input):
        if input == 1:
            self.move(-1)
        elif input == 2:
            self.move(1)
        elif input == 3:
            self.rotate_stone()
        elif input == 4:
            self.rotate_stone_counter_clockwise()


def eval_genomes(genomes,config):
    #Run the game for player of the population
    #And create a neural network for each player
    for genome_id, genome in genomes:
        genome.fitness = 0
        #Generate a neural network
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        #Start a new game
        game = Tetris()
        while (not game.game_over and not game.score > 15):
            game.drop()
            nnInput = game.output_info()
            output = net.activate(nnInput)
            max_index = 0
            max = 0
            for d in range(len(output)):  
                if output[d] > max:
                    max = output[d]
                    max_index = d
            #Feed the highest output index to the game
            game.play_ai(max_index)
        #if this player did well, go ahead and save them for running
        if game.calculate_fitness() >= fitness_for_saving:
            with open("./data/legend.pickle", "wb") as pickle_out:
                pickle.dump(net, pickle_out) 
        genome.fitness = game.calculate_fitness()
    
if __name__ == "__main__":
    #Setup NEAT
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'./data/TetrisNEAT')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(False))
    stats = neat.StatisticsReporter()
    winner = p.run(eval_genomes,number_generations)
