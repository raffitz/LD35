import pygame
import pygame.gfxdraw


# Initializing pygame and opening a window:
fullscreen = False

pygame.init()

pxwidth = 640
pxheight = 360

gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)

pygame.display.set_caption('Ludum Dare 35')

# Setting up the game field:

gamewidth = 640
gameheight = 360

gamefield = pygame.Surface((gamewidth,gameheight),0)
# gamefield.fill()

# Setting up the timer for framerate limiting:
clock = pygame.time.Clock()

# Cycle condition:
running = True

# Main loop:
while running:
	# Event handling:
	for each_event in pygame.event.get():
		if each_event.type == pygame.KEYDOWN:
			if each_event.key ==pygame.K_ESCAPE:
				# If you escape, you escape
				running = False
			elif each_event.key == pygame.K_F11:
				# Toggling fullscreen
				if fullscreen:
					fullscreen = False
					gameDisp = pygame.display.set_mode((oldw,oldh),pygame.RESIZABLE)
				else:
					fullscreen = True
					oldw = pxwidth
					oldh = pxheight
					modes = pygame.display.list_modes()
					gameDisp = pygame.display.set_mode(modes[0],pygame.FULLSCREEN)
				disps = pygame.display.get_surface()
				pxwidth,pxheight = disps.get_size()
		elif each_event.type == pygame.QUIT:
			# If you wanna exit the window, we'll let'ya
			running = False
		elif each_event.type == pygame.VIDEORESIZE:
			# The window is resizeable. If it is, in fact, resized, it needs to be handled
			pxwidth = each_event.w	# New width
			pxheight = each_event.h	# New height
			
			gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)
			disps = pygame.display.get_surface()
			
	
	# Framerate limiting
	clock.tick(30)
	
	# Placing the game field on screen
	scale = min(int(pxwidth*1.0/(1.0*gamewidth)),int(pxheight*1.0/(1.0*gameheight)))
	
	scaledwidth = round(gamewidth*scale)
	scaledheight = round(gameheight*scale)
	
	destination = pygame.Surface((scaledwidth,scaledheight),0)
	
	pygame.transform.scale(gamefield, (scaledwidth, scaledheight), destination)
	
	xoffset = round((pxwidth - scaledwidth)*0.5)
	yoffset = round((pxheight - scaledheight)*0.5)
	
	gameDisp.blit(destination,(xoffset,yoffset),None,0)
	
	# Updating the window:
	pygame.display.update()

# We got out of that vicious cycle, gotta get going:
pygame.quit()
quit()
