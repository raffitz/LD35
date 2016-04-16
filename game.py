#!/bin/python

import pygame
import pygame.gfxdraw
import pygame.draw
import pygame.image
import math
import os

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

# Player:

pangle = - math.pi / 2

pspeed = 0.0

paccel = False

pdecel = False

pport = False

pstarboard = False

px = 0.0

py = 0.0

pstate = 3

pcolor = 'chartreuse'

def renderplayer(targetsurface):
	polyverts = ngonlist(gamewidth//2,gameheight//2,pstate,20,pangle)
	pygame.draw.line(targetsurface,colors[pcolor],polyverts[0],(polyverts[0][0] + 5*math.cos(pangle),polyverts[0][1] + 5*math.sin(pangle)),2)
	drawpoly(targetsurface,polyverts,colors[pcolor],colors['black'],2)

# Initializing pygame and opening a window:

fullscreen = False

pygame.init()

pxwidth = 640
pxheight = 360

gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)

# Setting up the game field:

gamewidth = 640
gameheight = 360

gamefield = pygame.Surface((gamewidth,gameheight),0)
gamefield.fill((255,255,255))

# Title stuff

pygame.display.set_caption('polyAgonY')
titlepic_o = pygame.image.load(os.path.join('img','title.png'))
titlepic = pygame.Surface((gamewidth,gameheight),pygame.SRCALPHA,titlepic_o.get_bitsize(),titlepic_o.get_masks())
pygame.transform.scale(titlepic_o,(gamewidth,gameheight),titlepic)
del titlepic_o
anykey_o = pygame.image.load(os.path.join('img','instructions.png'))
anykey = pygame.Surface((gamewidth,gameheight),pygame.SRCALPHA,anykey_o.get_bitsize(),anykey_o.get_masks())
pygame.transform.scale(anykey_o,(gamewidth,gameheight),anykey)
del anykey_o

# Setting up the timer for framerate limiting:
clock = pygame.time.Clock()

# Cycle condition:
running = True

# Game tick counter:
tick = 0

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
			if state == 1:
				# Game
				if not (paccel or pdecel):
					if each_event.key == pygame.K_w:
						paccel = True
					elif each_event.key == pygame.K_s:
						pdecel = True
				if not (pport or pstarboard):
					if each_event.key == pygame.K_a:
						pport = True
					elif each_event.key == pygame.K_d:
						pstarboard = True
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
			elif state == 1:
				# Game
				if each_event.key == pygame.K_w:
					paccel = False
				elif each_event.key == pygame.K_s:
					pdecel = False
				elif each_event.key == pygame.K_a:
					pport = False
				elif each_event.key == pygame.K_d:
					pstarboard = False
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
		# Rotation rate - 30 = 1 RPS, 60 = 0.5 RPS, and so on
		rrate = 240
		purengon(gamefield,gameheight//2,gameheight//2,3 + ((tick//180) % 15),gameheight//3,((tick % rrate)*math.pi*2)/rrate,colors[saturated[(tick//30)% 12]],(0,0,0),1)
		gamefield.blit(titlepic,(0,0),None,0)
		if (tick // 30) % 2 == 1:
			gamefield.blit(anykey,(0,0),None,0)

	elif state == 1:
		#Game
		renderplayer(gamefield)
		px = px + pspeed * math.cos(pangle)
		py = py - pspeed * math.sin(pangle)
		if paccel and not pdecel:
			pspeed = pspeed + 0.01
			if pspeed > 1:
				pspeed = 1
		elif pdecel and not paccel:
			pspeed = pspeed - 0.01
			if pspeed < 0:
				pspeed = 0
		if pport and not pstarboard:
			pangle -= 0.1
		elif pstarboard and not pport:
			pangle += 0.1
		while pangle > math.pi:
			pangle = pangle - 2*math.pi
		while pangle < (-1)*math.pi:
			pangle = pangle + 2*math.pi
		# Debug print:
		if tick % 60 == 0:
			print('(%s,%s) %srad %s\n'%(px,py,pangle,pspeed))

	#elif state == 2:
		#Pause
	#else:
		#Outro
	


	# Framerate limiting
	clock.tick(30)

	tick = tick + 1
	
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
