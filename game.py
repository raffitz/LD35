#!/bin/python

import pygame
import pygame.gfxdraw
import pygame.draw
import pygame.image
import pygame.mixer
import pygame.font
import math
import os
import random

# Seed initialization:
random.seed()

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

pmaxspeed = 5.0

paccelv = 0.1

pdecelv = 0.15

paccel = False

pdecel = False

pport = False

pstarboard = False

pangulaccel = 0.03

px = 0.0

py = 0.0

pstate = 3

pradius = 20

pcolor = 10

def renderplayer(targetsurface):
	polyverts = ngonlist(gamewidth//2,gameheight//2,pstate,pradius,pangle)
	pygame.draw.line(targetsurface,colors[saturated[pcolor]],polyverts[0],(polyverts[0][0] + 0.25*pradius*math.cos(pangle),polyverts[0][1] + 0.25*pradius*math.sin(pangle)),2)
	drawpoly(targetsurface,polyverts,colors[saturated[pcolor]],colors['black'],2)

# Enemy stuff:

enemies = []

def gencoords(radius):
	# Generates a pair of coordinates with 95% probability of being within radius
	absolute = 0
	while abs(absolute) < 400:
		absolute = random.gauss(0,radius/3)
	phase = random.uniform(-math.pi,math.pi)
	xcoord = absolute * math.cos(phase) + px
	ycoord = absolute * math.sin(phase) + py
	return (xcoord,ycoord)

def genenemies(n,radius):
	elist = []
	for i in range(n):
		pos = gencoords(radius)
		sides = random.randint(3,7)
		colnum = random.randint(0,11)
		eangle = random.uniform(-math.pi,math.pi)
		elist.append((pos[0],pos[1],sides,colnum,eangle))
	return elist

def renderenemy(targetsurface,enemy):
	ex = int(enemy[0] + gamewidth//2 - px)
	ey = int(enemy[1] + gameheight//2 + py)
	pverts = ngonlist(ex,ey,enemy[2],5,enemy[4])
	render = False
	for pair in pverts:
		if pair[0] >= 0 and pair[0] < gamewidth and pair[1] >= 0 and pair[1] < gameheight:
			render = True
			break
	if not render:
		return False
	drawpoly(targetsurface,pverts,colors[saturated[enemy[3]]],colors['black'],1)
	return True



def renderenemies(targetsurface):
	count = 0
	for e in enemies:
		if renderenemy(targetsurface,e):
			count += 1
	return count

def tickenemies(radius):
	global pradius
	for i in range(len(enemies)):
		e = enemies[i]
		ex = e[0]
		ey = e[1]
		eangle = e[4]
		dists = (ex - px)**2 + (-ey - py)**2
		if dists <= pradius**2:
			newc = gencoords(radius)
			if e[2] == pstate:
				if e[3] == pcolor:
					pradius += 1
					blip.play()
				else:
					nop.play()
			else:
				pradius -=1
				ouch.play()
			newangle = random.uniform(-math.pi,math.pi)
			newcol = random.randint(0,11)
			newsides = random.randint(3,7)
			enemies[i] = (newc[0],newc[1],newsides,newcol,newangle)
			continue
		if dists >= 1.2*radius**2:
			newc = gencoords(radius)
			newangle = random.uniform(-math.pi,math.pi)
			newcol = random.randint(0,11)
			newsides = random.randint(3,7)
			enemies[i] = (newc[0],newc[1],newsides,newcol,newangle)
			continue
		ex -= 0.5*math.cos(eangle)
		ey += 0.5*math.sin(eangle)
		opposite = -ey - py
		adjacent = ex - px
		anglett = math.atan2(opposite,adjacent)
		anglevel = 0.02
		if abs(eangle-anglett)>=2*anglevel:
			if eangle > 0 and anglett > 0:
				if eangle > anglett:
					eangle -= anglevel
				else:
					eangle += anglevel
			elif eangle > 0 and anglett < 0:
				if anglett > eangle - math.pi:
					eangle -= anglevel
				else:
					eangle += anglevel
			elif eangle < 0 and anglett < 0:
				if eangle < anglett:
					eangle += anglevel
				else:
					eangle -= anglevel
			else:
				if anglett < eangle + math.pi:
					eangle += anglevel
				else:
					eangle -= anglevel
		enemies[i] = (ex,ey,e[2],e[3],eangle)

			

		


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
gameover_o = pygame.image.load(os.path.join('img','gameover.png'))
gameover = pygame.Surface((gamewidth,gameheight),pygame.SRCALPHA,gameover_o.get_bitsize(),gameover_o.get_masks())
pygame.transform.scale(gameover_o,(gamewidth,gameheight),gameover)
del gameover_o
movement_o = pygame.image.load(os.path.join('img','movement.png'))
movement = pygame.Surface((gamewidth,gameheight),pygame.SRCALPHA,movement_o.get_bitsize(),movement_o.get_masks())
pygame.transform.scale(movement_o,(gamewidth,gameheight),movement)
del movement_o

# Sound Stuff

pygame.mixer.init()

ouch = pygame.mixer.Sound(os.path.join('snd','ouch.wav'))
blip = pygame.mixer.Sound(os.path.join('snd','blip.wav'))
nop = pygame.mixer.Sound(os.path.join('snd','nop.wav'))

# Inverted stars, to perceive movement:
stars = []
def genstar():
	return (random.randint(-gamewidth//2,gamewidth//2) + px,random.randint(-gameheight//2,gameheight//2) - py,random.randint(0,128))

def genstars(num):
	slist = []
	for i in range(num):
		slist.append(genstar())
	return slist

def renderstar(targetsurface,star):
	pygame.gfxdraw.pixel(targetsurface,int(star[0] + gamewidth//2 - px),int(star[1] + gameheight//2 + py),(star[2],star[2],star[2]))

def renderstars(targetsurface):
	for s in stars:
		renderstar(targetsurface,s)

def teststars():
	for i in range(len(stars)):
		s = stars[i]
		sx = int(s[0] + gamewidth//2 - px)
		sy = int(s[1] + gameheight//2 + py)
		if sx < 0:
			stars[i] = (gamewidth//2 + px,random.randint(-gameheight//2,gameheight//2) - py,random.randint(0,128))
			continue
		if sx >= gamewidth:
			stars[i] = (-gamewidth//2 + px,random.randint(-gameheight//2,gameheight//2) - py,random.randint(0,128))
			continue
		if sy < 0:
			stars[i] = (random.randint(-gamewidth//2,gamewidth//2) + px,gameheight//2 - py,random.randint(0,128))
			continue
		if sy >= gameheight:
			stars[i] = (random.randint(-gamewidth//2,gamewidth//2) + px,-gameheight//2 - py,random.randint(0,128))
			continue


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
				tick = 0
				pangle = - math.pi / 2
				pspeed = 0.0
				pmaxspeed = 5.0
				paccelv = 0.1
				pdecelv = 0.15
				paccel = False
				pdecel = False
				pport = False
				pstarboard = False
				pangulaccel = 0.03
				px = 0.0
				py = 0.0
				pstate = 3
				pradius = 20
				pcolor = 10
				del enemies
				enemies = genenemies(1000,10000)
				del stars
				stars = genstars(256)
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
				elif each_event.key == pygame.K_UP:
					pstate = ((pstate - 2) % 5) + 3
				elif each_event.key == pygame.K_DOWN:
					pstate = ((pstate - 4) % 5) + 3
				elif each_event.key == pygame.K_LEFT:
					pcolor = (pcolor - 1) % 12
				elif each_event.key == pygame.K_RIGHT:
					pcolor = (pcolor + 1) % 12
				elif each_event.key == pygame.K_SPACE:
					state = 2
			elif state == 2:
				if each_event.key == pygame.K_SPACE:
					state = 1
				if each_event.key == pygame.K_r:
					state = 0
			else:
				#Outro
				if each_event.key == pygame.K_SPACE or each_event.key == pygame.K_RETURN:
					state = 0
		elif each_event.type == pygame.QUIT:
			# If you wanna exit the window, we'll let'ya
			running = False
		elif each_event.type == pygame.VIDEORESIZE:
			# The window is resizeable. If it is, in fact, resized, it needs to be handled
			pxwidth = each_event.w	# New width
			pxheight = each_event.h	# New height
			if pxwidth < gamewidth:
				pxwidth = gamewidth
			if pxheight < gameheight:
				pxheight = gameheight
			gameDisp = pygame.display.set_mode((pxwidth,pxheight),pygame.RESIZABLE)
			disps = pygame.display.get_surface()
	
	# Clear screen:
	if state < 2:
		gamefield.fill((255,255,255))
		tick = tick + 1
	
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
		teststars()

		nenemies = renderenemies(gamefield)

		renderstars(gamefield)

		renderplayer(gamefield)
		px = px + pspeed * math.cos(pangle)
		py = py - pspeed * math.sin(pangle)
		if paccel and not pdecel:
			pspeed = pspeed + paccelv
			if pspeed > pmaxspeed:
				pspeed = pmaxspeed
		elif pdecel and not paccel:
			pspeed = pspeed - pdecelv
			if pspeed < 0:
				pspeed = 0
		if pport and not pstarboard:
			pangle -= pangulaccel
		elif pstarboard and not pport:
			pangle += pangulaccel
		while pangle > math.pi:
			pangle = pangle - 2*math.pi
		while pangle < (-1)*math.pi:
			pangle = pangle + 2*math.pi

		tickenemies(10000)

		if pradius < 5 or pradius > gameheight//2:
			state = 3
			gamefield.blit(gameover,(0,0),None,0)
			pygame.font.init()
			pixel = pygame.font.Font(os.path.join('txt','PIXEL___.TTF'),16)
			seconds = tick//30
			minutes = seconds//60
			seconds = seconds%60
			message = ""
			if minutes > 0:
				message = "%s%d minutes, "%(message,minutes)
			message = "%s%d seconds"%(message,seconds)
			textsurf = pixel.render(message,False,colors['white'],colors['black'])
			tw = textsurf.get_width()
			tos = (gamewidth - tw)//2
			gamefield.blit(textsurf,(tos,32),None,0)
			del message
			del textsurf
			del tw
			del tos
			del pixel
			pygame.font.quit()

		if tick < 90:
			gamefield.blit(movement,(0,0),None,0)

	#elif state == 2:
		#Pause
	#else:
		#Outro
	


	# Framerate limiting
	clock.tick(30)
	
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
