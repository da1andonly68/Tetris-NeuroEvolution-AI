import pygame
from pygame.locals import *  # noqa
import sys
import random
import numpy as np
import PIL
import pickle

ROW_COUNT = 24
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

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
    board += [[1 for x in range(COLUMN_COUNT)]]
    return board


class Tetris:
    
    def __init__(self):
       
        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.score = 0
        self.setup()
        
    def calculateInput(self):
        dist_X_to_The_Wall = self.wallx+80
        dist_Y_to_The_Wall_UP = self.birdY-(0 - self.gap - self.offset+500)
        dist_Y_to_The_Wall_DOWN = self.birdY-(360 + self.gap - self.offset)
        dist_Y_TOP = self.birdY
        dist_Y_BOTTOM = 720-self.birdY
        res = [dist_X_to_The_Wall,dist_Y_to_The_Wall_UP,dist_Y_to_The_Wall_DOWN,dist_Y_TOP,dist_Y_BOTTOM]
        return res
    
    def new_stone(self):
        self.stone = random.choice(tetris_shapes)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if self.stone[0][0] != 0:
            self.shape = self.stone[0][0]
        else:
            self.shape = self.stone[1][1]
        self.rotation = 1

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True
    
    def setup(self):
        self.board = new_board()
        self.new_stone()

    def drop(self):
        self.stone_y += 1#was 1
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
            while True:
                for i, row in enumerate(self.board[:-1]):
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
                pixels.append(self.board[row][column])
        return pixels

    def output_shape_location(self):
        return [self.stone_x, self.stone_y]

    #The outputs are as follows: Current Shape, Shape Location, Shape Rotation, Grid Data 
    def output_info(self):
        outputs = []
        outputs.append(self.shape)
        outputs.append(self.rotation)
        outputs.extend(self.output_shape_location())
        outputs.extend(self.output_board())
        return outputs

    def calculate_fitness(self):
        fitness = 0
        for row in range(len(self.board) -1):#leaves out the pre-populated bottom row
            total = 0
            for column in range(len(self.board[0])):
                if self.board[row][column] != 0:
                    total += 1
            if(total >= 5):
                fitness += (total / COLUMN_COUNT )
        fitness += self.score * 2
        return fitness

    def play_ai(self, input):
        if input == 1:
            self.move(-1)
        elif input == 2:
            self.move(1)
        elif input == 3:
            self.rotate_stone()
        elif input == 4:
            self.rotate_stone_counter_clockwise()

import neat

number_generations = 1000
def eval_genomes(genomes,config):
    for genome_id, genome in genomes:
        genome.fitness = 99999
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        game = Tetris()
        while (not game.game_over and not game.score > 10):
            game.drop()
            nnInput = game.output_info()
            output = net.activate(nnInput)
            max_index = 0
            max = 0
            for d in range(len(output)):  
                if output[d] > max:
                    max = output[d]
                    max_index = d
            game.play_ai(max_index)
        if game.calculate_fitness() >= 10:
            with open("./data/legend.pickle", "wb") as pickle_out:
                pickle.dump(net, pickle_out) 
        genome.fitness = game.calculate_fitness()
    
if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'./data/TetrisNEAT')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(False))
    winner = p.run(eval_genomes,number_generations)
