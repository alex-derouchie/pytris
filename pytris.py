import pygame, sys
from pygame.locals import *
import random

pygame.init()

#COLOURS
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
CYAN = pygame.Color(0,255,255)
TETRO_COLORS = {
	"SHAPE_O" : pygame.Color(254, 203, 0)
	"SHAPE_T" : pygame.Color(149, 45, 152)
	"SHAPE_I" : pygame.Color(0, 159, 218)
	"SHAPE_L" : pygame.Color(255, 121, 0)
	"SHAPE_J" : pygame.Color(0, 101, 189)
	"SHAPE_S" : pygame.Color(105, 190, 40)
	"SHAPE_Z" : pygame.Color(237, 41, 57)
}


#Shape Definitions

SHAPE_O = [['....',
			'.XX.',
			'.XX.',
			'....']]
			
SHAPE_I = [['....',
			'XXXX',
			'....',
			'....'],
		   ['.X..',
			'.X..',
			'.X..',
			'.X..',]]
			
SHAPE_Z = [['....',
			'XX..',
			'.XX.',
			'....'],
		   ['.X..',
		    'XX..',
			'X...',
			'....']]
			
SHAPE_S = [['....',
			'.XX.',
			'XX..',
			'....'],
		   ['....',
		    '.X..',
		    '.XX.',
			'..X.']]
			
SHAPE_T = [['....',
			'.X..',
			'XXX.',
			'....'],
		   ['....',
			'.X..',
			'.XX.',
			'.X..'],
		   ['....',
			'XXX.',
			'.X..',
			'....'],
		   ['.X..',
			'XX..',
			'.X..',
			'....',]]
			
SHAPE_L = [['....',
			'...X',
			'.XXX',
			'....'],
		   ['....',
			'..X.',
			'..X.',
			'..XX'],
		   ['....',
			'....',
			'.XXX',
			'.X..'],
		   ['....',
			'.XX.',
			'..X.',
			'..X.',]]
			
SHAPE_J = [['....',
			'.X..',
			'.XXX',
			'....'],
		   ['....',
			'..XX',
			'..X.',
			'..X.'],
		   ['....',
			'....',
			'.XXX',
			'...X'],
		   ['....',
			'..X.',
			'..X.',
			'.XX.',]]

#Constants
WINDOW_SIZE = (320,560)
FPS = 2

shapes = [SHAPE_O, SHAPE_I, SHAPE_Z, SHAPE_S, SHAPE_T, SHAPE_L, SHAPE_J]
BLOCK_SIZE = (20,20)
EDGE_BORDER = 3
CUBE_BORDER = 2
PLAYAREA_ORGIN = (60,60)
PLAYAREA_RIGHT_EDGE = 260
PLAYAREA_LEFT_EDGE = 60
BLOCK_OFFSET = 20

#Tetromino class representing a single tetromino
class Tetromino(object):
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = TETRO_COLORS[shape]
		self.rotation = 0

#Model Functions

#builds a grid of RGB values corresponding to the tetrominos filling each corresponding block
def build_grid(filled_blocks = {}):
	grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if (j,i) in filled_blocks:
				filled_color = filled_blocks[(j,i)]
				grid[i][j] = filled_color
	return grid


#Controller Functions



#View Functions


def main(window):

	clock = pygame.time.Clock() #Clock initialization
	
	current_state = {}
	
	#Game Loop
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		pygame.display.update()
		clock.tick(FPS)
			
			
	
##SETUP##
#10x20 board + bottom content + margins
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pytris")	
main(window)






