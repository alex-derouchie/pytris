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
GRAY = pygame.Color(150,150,150)

#OIZSTLJ
TETRO_COLORS = [(254,203,0), (0,159,218), (237,41,57), (105,190,40), (149,45,152), (255,121,0), (0,101,189)]


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
			'..X.',
			'XXX.',
			'....'],
		   ['....',
			'.X..',
			'.X..',
			'.XX.'],
		   ['....',
			'....',
			'XXX.',
			'X...'],
		   ['....',
			'XX..',
			'.X..',
			'.X..',]]
			
SHAPE_J = [['....',
			'X...',
			'XXX.',
			'....'],
		   ['....',
			'.XX.',
			'.X..',
			'.X..'],
		   ['....',
			'....',
			'XXX.',
			'..X.'],
		   ['....',
			'.X..',
			'.X..',
			'XX..',]]

#Constants
WINDOW_SIZE = (320,560)
FPS = 30

shapes = [SHAPE_O, SHAPE_I, SHAPE_Z, SHAPE_S, SHAPE_T, SHAPE_L, SHAPE_J]
BLOCK_SIZE = (20,20)
EDGE_BORDER = 3
CUBE_BORDER = 2
PLAYAREA_ORGIN = (60,60)
NEXT_TETRO_ORIGIN = (65, 480)
PLAYAREA_WIDTH = 200
PLAYAREA_HEIGHT = 400
BLOCK_OFFSET = 20
SCORE = 0

#Tetromino class representing a single tetromino
class Tetromino(object):
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = TETRO_COLORS[shapes.index(shape)]
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
	return Tetromino(3,-2,random.choice(shapes))
	
def move_tetro(tetromino, direction, filled_blocks = {}):
	moved = False
	old_pos = get_tetro_position(tetromino)
	if direction == 'LEFT' and is_move_valid(tetromino, True, filled_blocks):
		for pos in old_pos:
			if pos in filled_blocks:
				filled_blocks.pop(pos)
		tetromino.x -= 1
		return True
	elif direction == 'RIGHT' and is_move_valid(tetromino, False, filled_blocks):
		for pos in old_pos:
			if pos in filled_blocks:
				filled_blocks.pop(pos)
		tetromino.x += 1
		return True
	elif direction == 'DOWN' and is_fall_valid(tetromino, filled_blocks):
		for pos in old_pos:
			if pos in filled_blocks:
				filled_blocks.pop(pos)
		tetromino.y += 1
		return True
	return False
	
def is_move_valid(tetromino, left, filled_blocks = {}):
	tetro_position = get_tetro_position(tetromino)
	min_x = 10
	max_x = -1
	for pos in tetro_position:
		if pos[0] < min_x: min_x = pos[0]
		if pos[0] > max_x: max_x = pos[0]

	if left:
		if min_x == 0:
			return False
		for pos in tetro_position:
			if pos[0] == min_x and ((pos[0]-1, pos[1]) in filled_blocks):
				return False
	else:
		if max_x == 9:
			return False
		for pos in tetro_position:
			if pos[0] == max_x and ((pos[0]+1, pos[1]) in filled_blocks):
				return False
	return True
	
def is_fall_valid(tetromino, filled_blocks = {}):
	tetro_position = get_tetro_position(tetromino)
	max_y = -10
	
	#TODO: This only checks if there are collisions with the lowest parts of the tetro, not every part of it.
	for pos in tetro_position:
		if pos[1] > max_y: max_y = pos[1] #Determining lowest point
		
	if max_y == 19: #Tetro at bottom of playarea
			return False
			
	for pos in tetro_position:
		if ((pos[0], pos[1]+1) not in tetro_position) and ((pos[0], pos[1]+1) in filled_blocks):
			return False
	return True
	
def is_rotation_valid(tetromino, filled_blocks = {}):
	tetro_position = get_tetro_position(tetromino)
	blocks = []
	rotated_tetro = tetromino.shape[(tetromino.rotation + 1) % len(tetromino.shape)]
	for i, line in enumerate(rotated_tetro):
		row = list(line)
		for j, column in enumerate(row):
			if column == 'X':
				blocks.append((tetromino.x + j, tetromino.y + i))
	for pos in blocks:
		if pos[0] < 0 or pos[0] > 9:
			return False
		if pos[1] > 19:
			return False
		if pos in filled_blocks and pos not in tetro_position:
			return False
	return True
	
def get_tetro_position(tetromino):
	blocks = []
	rotated_tetro = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
	for i, line in enumerate(rotated_tetro):
		row = list(line)
		for j, column in enumerate(row):
			if column == 'X':
				blocks.append((tetromino.x + j, tetromino.y + i))
	return blocks
	
def check_filled_rows(tetromino, filled_blocks = {}):
	full_rows = []
	tetro_position = get_tetro_position(tetromino)
	for pos in tetro_position:
		row_full = True
		for i in range(10):
			if (i, pos[1]) not in filled_blocks:
				row_full = False
		if row_full and pos[1] not in full_rows:
			full_rows.append(pos[1])
	return full_rows
	
def shift_upper_rows(row, filled_blocks = {}):
	for r in range(row-1, -1, -1):
		for c in range(10):
			if (c, r) in filled_blocks:
				popped_val = filled_blocks.pop((c,r))
				filled_blocks[(c,r+1)] = popped_val
			
def clear_filled_rows(tetromino, filled_blocks = {}):
	global SCORE
	filled_rows = check_filled_rows(tetromino, filled_blocks)
	SCORE += len(filled_rows)*1000
	for row in filled_rows:
		for col in range(10):
			filled_blocks.pop((col, row))
		shift_upper_rows(row, filled_blocks)
		
def game_over(tetromino):
	tetro_pos = get_tetro_position(tetromino)
	for pos in tetro_pos:
		if pos[1] < 0:
			return True
	return False
	
			

#View Functions

def draw_window(window, grid, next_tetro, game_done):
	window.fill((0,0,0))
	
	pygame.font.init()
	if game_done:
		over_font = pygame.font.SysFont('impact', 50)
		over_label = over_font.render('GAME OVER', 1, RED)
		window.blit(over_label, (int(WINDOW_SIZE[0]/2 - (over_label.get_width()/2)), 100))
		score_font = pygame.font.SysFont('impact', 36)
		score_label = score_font.render(f'SCORE: {SCORE}', 1, WHITE)
		window.blit(score_label, (int(WINDOW_SIZE[0]/2 - (score_label.get_width()/2)), 300))
		instruction_font = pygame.font.SysFont('impact', 26)
		instruction_label = instruction_font.render('Press Enter for new game', 1, GRAY)
		window.blit(instruction_label, (int(WINDOW_SIZE[0]/2 - (instruction_label.get_width()/2)), 350))
		return
	else:
		title_font = pygame.font.SysFont('impact', 40)
		title_label = title_font.render('Pytris', 1, CYAN)
		window.blit(title_label, (int(WINDOW_SIZE[0]/2 - (title_label.get_width()/2)), 10))
		score_font = pygame.font.SysFont('impact', 20)
		score_label = score_font.render('SCORE', 1, WHITE)
		score_value_label = score_font.render(f'{SCORE}', 1, WHITE)
		window.blit(score_label,(int(WINDOW_SIZE[0]* (2/3) - (score_label.get_width()/2)), 470))
		window.blit(score_value_label,(int(WINDOW_SIZE[0]* (2/3) - (score_value_label.get_width()/2)), 500))
		next_tetro_font = pygame.font.SysFont('impact', 20)
		next_tetro_label = next_tetro_font.render('NEXT', 1, WHITE)
		window.blit(next_tetro_label,(int(WINDOW_SIZE[0]* (1/4)), 470)) 
	
		draw_next_tetro(window, next_tetro)

		for i in range(len(grid)):
			for j in range(len(grid[i])):
				pygame.draw.rect(window, grid[i][j], (PLAYAREA_ORGIN[0] + j*BLOCK_OFFSET, PLAYAREA_ORGIN[1] + i*BLOCK_OFFSET, BLOCK_OFFSET, BLOCK_OFFSET), 0)
		pygame.draw.rect(window, CYAN, (PLAYAREA_ORGIN[0], PLAYAREA_ORGIN[1], PLAYAREA_WIDTH, PLAYAREA_HEIGHT), 4)
	
def draw_next_tetro(window, next_tetro):
	rotated_tetro = next_tetro.shape[0]
	for i, line in enumerate(rotated_tetro):
		row = list(line)
		for j, column in enumerate(row):
			if column == 'X':
				pygame.draw.rect(window, next_tetro.color, (NEXT_TETRO_ORIGIN[0] + j*BLOCK_OFFSET, NEXT_TETRO_ORIGIN[1] + i*BLOCK_OFFSET, BLOCK_OFFSET, BLOCK_OFFSET), 0)


#Main function & game loop
def main(window):	
	current_tetro = get_next_tetro()
	clock = pygame.time.Clock() #Clock initialization
	current_time = pygame.time.get_ticks()
	pygame.key.set_repeat(1, 150)
	current_state = {} #Keeps track of coords of occupied blocks
	grid = build_grid(current_state) #Grid initialization
	next_tetro = get_next_tetro()
	keydown = False
	GAME_OVER = False
	global SCORE
	
	draw_window(window, grid, next_tetro, GAME_OVER)
	
	#Game Loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if not GAME_OVER:
					if event.key == pygame.K_LEFT:
						move_tetro(current_tetro, 'LEFT', current_state)
					if event.key == pygame.K_RIGHT:
						move_tetro(current_tetro, 'RIGHT', current_state)
					if event.key == pygame.K_DOWN:
						keydown = True
						if move_tetro(current_tetro, 'DOWN', current_state) == False:
							if game_over(current_tetro):
								GAME_OVER = True
								draw_window(window, grid, next_tetro, GAME_OVER)	
							clear_filled_rows(current_tetro, current_state)
							current_tetro = next_tetro
							next_tetro = get_next_tetro()
							SCORE += 100
						else:
							SCORE += 10
					if event.key == pygame.K_UP and is_rotation_valid(current_tetro, current_state):
						old_pos = get_tetro_position(current_tetro)
						for pos in old_pos:
							if pos in current_state:
								current_state.pop(pos)
						current_tetro.rotation += 1
				else:
					if event.key == pygame.K_RETURN:
						GAME_OVER = False
						SCORE = 0
						current_state = {}
						current_tetro = get_next_tetro()
						next_tetro = get_next_tetro()
						
					if event.key == pygame.K_ESCAPE:
						break
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					keydown = False
			
					
		current_tetro_pos = get_tetro_position(current_tetro)
		for pos in current_tetro_pos:
			current_state[pos] = current_tetro.color
		
		if (keydown == False) and (pygame.time.get_ticks() - current_time > 1000):
			current_time = pygame.time.get_ticks()
			if move_tetro(current_tetro, 'DOWN', current_state) == False:
				if game_over(current_tetro):
					GAME_OVER = True
					draw_window(window, grid, next_tetro, GAME_OVER)	
				clear_filled_rows(current_tetro, current_state)
				current_tetro = next_tetro
				next_tetro = get_next_tetro()
		
		grid = build_grid(current_state)
		draw_window(window, grid, next_tetro, GAME_OVER)	
		pygame.display.update()
		clock.tick(FPS)

		
			
	
##SETUP##
#10x20 board + bottom content + margins
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pytris")	
main(window)






