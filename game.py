#!/bin/python

import pygame
import pygame.gfxdraw
import pygame.draw
import math

# Color declaration:

colors = {	'black':	(0,0,0),
		'white':	(255,255,255),
		'red':		(255,0,0),
		'green':	(0,255,0),
		'blue':		(0,0,255),
		'yellow':	(255,255,0),
		'cyan':		(0,255,255),
		'magenta':	(255,0,255),
		'azure':	(0,127,255),
		'violet':	(127,0,255),
		'rose':		(255,0,127),
		'orange':	(255,127,0),
		'chartreuse':	(127,255,0),
		'spring':	(0,255,127)}

primaries = ['red','green','blue']
secondaries = ['yellow','cyan','magenta']
tertiaries = ['azure','violet','rose','orange','chartreuse','spring']

saturated = primaries + secondaries + tertiaries

bw = ['black','white']

allcols = bw + saturated

# Draw a polygon:
def drawpoly(targetsurface,polyverts,incolor,bordercolor,border):
	pygame.draw.polygon(targetsurface,incolor,polyverts,0)
	if border != 0:
		pygame.draw.polygon(targetsurface,bordercolor,polyverts,border)

# Generate ngon poly list:
def ngonlist(centerx,centery,n,radius,angle):
	if n < 3:
		return []
	polyverts = []
	for i in range(n):
		finangle = i * ((2 * math.pi) / n) + angle
		horizcomp = radius * math.cos(finangle)
		vertcomp = radius * math.sin(finangle)
		polyverts.append( (centerx + horizcomp,centery + vertcomp) )
	return polyverts

# Draw an ngon:
def purengon(targetsurface,centerx,centery,n,radius,angle,incolor,bordercolor,border):
	if n < 3:
		return
	polyverts = ngonlist(centerx,centery,n,radius,angle)
	drawpoly(targetsurface,polyverts,incolor,bordercolor,border)


#pygame.draw.line(targetsurface,incolor,polyverts[0],(polyverts[0][0] + 0.25*radius*math.cos(angle),polyverts[0][1] + 0.25*radius*math.sin(angle)),2)

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
gamefield.fill((255,255,255))

# Setting up the timer for framerate limiting:
clock = pygame.time.Clock()

# Cycle condition:
running = True

# Game tick counter:
tick = 0
loops = 0

# Game state:
state = 0
#	States:
#	0	Intro
#	1	Game
#	2	Pause
#	3	Outro

# Main loop:
while running:
	# Event handling:
	for each_event in pygame.event.get():
		if each_event.type == pygame.KEYDOWN:
			if each_event.key ==pygame.K_ESCAPE:
				# If you escape, you escape
				running = False
				continue
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
				continue
			#if state == 0:
				# Intro
			#elif state == 1:
				# Game
			#elif state == 2:
				# Pause
			#else:
				# Outro
		elif each_event.type == pygame.KEYUP:
			if each_event.key ==pygame.K_ESCAPE:
				continue
			elif each_event.key == pygame.K_F11:
				continue
			if state == 0:
				# Intro
				state = 1
			#elif state == 1:
				#Game
			#elif state == 2:
				#Pause
			#else:
				#Outro
		elif each_event.type == pygame.QUIT:
			# If you wanna exit the window, we'll let'ya
			running = False
		elif each_event.type == pygame.VIDEORESIZE:
			# The window is resizeable. If it is, in fact, resized, it needs to be handled
			pxwidth = each_event.w	# New width
			pxheight = each_event.h	# New height
			
			gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)
			disps = pygame.display.get_surface()
	
	# Clear screen:
	gamefield.fill((255,255,255))
	
	# States:
	if state == 0:
		# Intro
		# Test polygon draw:
		purengon(gamefield,180,180,3 + ((loops//12) % 15),50,(tick*math.pi*2)/30,colors[saturated[loops % 12]],(0,0,0),1)
	#elif state == 1:
		#Game
	#elif state == 2:
		#Pause
	#else:
		#Outro
	


	# Framerate limiting
	clock.tick(30)

	tick = tick + 1
	if tick > 30:
		tick = tick - 30
		loops += 1
	
	# Placing the game field on screen
	scale = min(int(pxwidth*1.0/(1.0*gamewidth)),int(pxheight*1.0/(1.0*gameheight)))
	
	scaledwidth = int(round(gamewidth*scale))
	scaledheight = int(round(gameheight*scale))
	
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
