import pygame
from pygame.locals import *

pygame.init()
#10x20 board + bottom content + margins
window = pygame.display.set_mode((320, 560))

#COLOURS
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
CYAN = pygame.Color(0,255,255)

#Game Loop
while True:
	pygame.display.update()
	pygame.draw.line(window, CYAN, (58,58), (58, 462), 3)
	pygame.draw.line(window, CYAN, (58,58), (262, 58), 3)
	pygame.draw.line(window, CYAN, (262,58), (262, 462), 3)
	pygame.draw.line(window, CYAN, (58,462), (262, 462), 3)
	pygame.draw.rect(window, RED, ((60, 60),(20, 20)), 2 )
	pygame.draw.rect(window, GREEN, ((80, 60),(20, 20)), 2 )
	pygame.draw.rect(window, RED, ((100, 60),(20, 20)), 2 )
	pygame.draw.rect(window, GREEN, ((120, 60),(20, 20)), 2 )
	pygame.draw.rect(window, RED, ((140, 60),(20, 20)), 2 )
	pygame.draw.rect(window, GREEN, ((160, 60),(20, 20)), 2 )
	pygame.draw.rect(window, RED, ((180, 60),(20, 20)), 2 )
	pygame.draw.rect(window, GREEN, ((200, 60),(20, 20)), 2 )
	pygame.draw.rect(window, RED, ((220, 60),(20, 20)), 2 )
	pygame.draw.rect(window, GREEN, ((240, 60),(20, 20)), 2 )
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
