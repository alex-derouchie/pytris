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
	"SHAPE_O" : pygame.Color(254, 203, 0),
	"SHAPE_T" : pygame.Color(149, 45, 152),
	"SHAPE_I" : pygame.Color(0, 159, 218),
	"SHAPE_L" : pygame.Color(255, 121, 0),
	"SHAPE_J" : pygame.Color(0, 101, 189),
	"SHAPE_S" : pygame.Color(105, 190, 40),
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
PLAYAREA_WIDTH = 200
PLAYAREA_HEIGHT = 400
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

def get_next_tetro():
	return Tetromino(5,0,random.choice(shapes))
	
def move_tetro(Tetromino, tick, filled_blocks = {}):
	#Detect keys pressed, move tetro using check f'ns accordingly
	pass
	
def is_move_valid(Tetromino, left, filled_blocks = {}):
	tetro_position = get_tetro_position(Tetromino)
	for pos in tetro_position:
		if left and (pos[0]-1, pos[1]) in filled_blocks:
			return False
		elif (not left) and (pos[0]+1, pos[1]) in filled_blocks:
			return False
	return True
	
def is_fall_valid(Tetromino, filled_blocks = {}):
	tetro_position = get_tetro_position(Tetromino)
	for pos in tetro_position:
		if (pos[0], pos[1]+1) in filled_blocks:
			return False
	return True
	
def get_tetro_position(Tetromino):
	blocks = []
	rotated_tetro = Tetromino.shape[Tetromino.rotation % len(Tetromino.shape)]
	for i, line in enumerate(rotated_tetro):
		row = list(line)
		for j, column in enumerate(row):
			if column == 'X':
				blocks.append((shape.x + j, shape.y + i))
	return blocks


#View Functions

def draw_window(window, grid):
	window.fill((0,0,0))
	
	pygame.font.init()
	font = pygame.font.SysFont('impact', 40)
	label = font.render('Pytris', 1, CYAN)
	window.blit(label, (WINDOW_SIZE[0]/2 - (label.get_width()/2), 10))
	
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(window, grid[i][j], (PLAYAREA_ORGIN[0] + j*BLOCK_OFFSET, PLAYAREA_ORGIN[1] + i*BLOCK_OFFSET, BLOCK_OFFSET, BLOCK_OFFSET), 0)
	pygame.draw.rect(window, CYAN, (PLAYAREA_ORGIN[0], PLAYAREA_ORGIN[1], PLAYAREA_WIDTH, PLAYAREA_HEIGHT), 4)


#Main function & game loop
def main(window):

	grid = build_grid({}) #Grid initialization
	
	#Testing functionality
	#grid[19][0] = TETRO_COLORS['SHAPE_L']
	#grid[19][1] = TETRO_COLORS['SHAPE_L']
	#grid[19][2] = TETRO_COLORS['SHAPE_L']
	#grid[18][2] = TETRO_COLORS['SHAPE_L']
	#grid[19][3] = TETRO_COLORS['SHAPE_I']
	#grid[19][4] = TETRO_COLORS['SHAPE_I']
	#grid[19][5] = TETRO_COLORS['SHAPE_I']
	#grid[19][6] = TETRO_COLORS['SHAPE_I']
	
	clock = pygame.time.Clock() #Clock initialization
	current_state = {} #Keeps track of coords of occupied blocks
	
	draw_window(window, grid)
	
	
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






