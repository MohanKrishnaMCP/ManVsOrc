import pygame
pygame.init()

win =pygame.display.set_mode((800,600))
pygame.display.set_caption('man vs orc')
screenwidth=800								#screenwidth declared globally

walkright = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkleft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg3.jpg')
char = pygame.image.load('standing.png')

clock=pygame.time.Clock()

score = 0 

class player(object):
	def __init__(self,x,y,width,height):
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.vel=5
		self.jump=False
		self.jumpcount=10
		self.left=False
		self.right=False
		self.walkcount=0
		self.standing = True
		self.hitbox=(self.x+17,self.y+2,35,60)	#(x,y,width,height)

	def draw(self,win):
		if self.walkcount+1 >= 27:
			self.walkcount=0


		if not self.standing:
			if self.left:
				win.blit(walkleft[self.walkcount//3],(self.x,self.y))
				self.walkcount+=1
			elif self.right:
				win.blit(walkright[self.walkcount//3],(self.x,self.y))
				self.walkcount+=1
		else:
			if self.right:
				win.blit(walkright[0],(self.x,self.y))
			else:
				win.blit(walkleft[0],(self.x,self.y))
		self.hitbox=(self.x+17,self.y+2,35,60)
		#pygame.draw.rect(win,(255,0,0),self.hitbox,2)

	def hit(self):
		self.x = 20
		self.y = 420
		self.walkcount = 0
		font1 = pygame.font.SysFont('comicsans', 100)
		text = font1.render('-5', 1, (255, 0, 0))
		win.blit(text, (400,200))
		#delay maechanism for respanwing
		i = 0
		while i <50:
			pygame.time.delay(10)
			i += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 101
					pygame.quit()


class projectile(object):	#bullet
	def __init__(self,x,y,radius,color,facing):
		self.x=x
		self.y=y
		self.radius=radius
		self.color=color
		self.facing=facing
		self.vel = 10*facing

	def draw(self,win):
		pygame.draw.circle(win,self.color,(self.x,self.y), self.radius)

class enemy(object):
	walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
	walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

	def __init__(self,x,y,width,height,end):
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.end=end	
		self.walkcount=0
		self.vel=5
		self.path=[self.x,self.end]
		self.hitbox=(self.x+17,self.y+2,35,60)
		self.health = 100
		self.visible = True

	def draw(self,win): 
		self.move()
		if self.visible:
			if self.walkcount+1 >= 33:
				self.walkcount=0

			if self.vel>0:
				win.blit(self.walkRight[self.walkcount//3],(self.x,self.y))
				self.walkcount+=1
			else:
				win.blit(self.walkLeft[self.walkcount//3],(self.x,self.y))
				self.walkcount+=1

			pygame.draw.rect(win,(255,0,0), (self.hitbox[0],self.hitbox[1] - 20, 50, 10))	#helath bar(red)
			pygame.draw.rect(win,(0,255,0), (self.hitbox[0],self.hitbox[1] - 20, 50 - ((50/100) * (100 - self.health)), 10))#health bar (green - changing)
			self.hitbox=(self.x+17,self.y+2,35,60)
			#pygame.draw.rect(win,(255,0,0),self.hitbox,2)

	def move(self):	
		#make the orc move in opposite direction if the end point is reached 
		if self.vel>0:
			if self.x<self.path[1]:
				self.x+=self.vel
			else:
				self.vel= self.vel*-1
				self.walkcount=0
		else:
			if self.x-self.vel>self.path[0]:
				self.x+=self.vel
			else:
				self.vel= self.vel*-1
				self.walkcount=0

	def hit(self):
		if self.health > 0:
			self.health -=10
		else:
			self.visible = False
		print("hit")

def redrawGameWindow():
	global walkcount
	win.blit(bg,(0,0))
	text=font.render('score: '+ str(score), 1, (0,0,0))
	win.blit(text,(640,10))
	
	man.draw(win)
	orc.draw(win)
	
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()

#-----------main------------------
font = pygame.font.SysFont('comincsans',30, True)
man=player(10,420,64,64)
orc=enemy(100,430,64,64,screenwidth-64)
run=True
shootloop=0
bullets=[]
while run:
	clock.tick(27)

#if the orc collides with the man - execute man.hit() ad score-=5
	if orc.visible:
		if man.hitbox[1] < orc.hitbox[1]+orc.hitbox[3] and man.hitbox[1] +man.hitbox[3] > orc.hitbox[1]:
			if man.hitbox[0] + man.hitbox[2] > orc.hitbox[0] and man.hitbox[0] < orc.hitbox[0]+ orc.hitbox[3]:
				man.hit()
				score -= 5

#shootloop is initialized with 0 - man can shoot only if shootloop is zero. made so that only one bullet comes out when space is pressed creates something like delay
	if shootloop > 0:
		shootloop +=1
	if shootloop > 3:
		shootloop = 0

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run= False

#pop the bullet if it hits the orc,execute orc.hit() and score+=1
	for bullet in bullets:
		if bullet.y-bullet.radius < orc.hitbox[1]+orc.hitbox[3] and bullet.y+bullet.radius > orc.hitbox[1]:
			if bullet.x + bullet.radius > orc.hitbox[0] and bullet.x - bullet.radius < orc.hitbox[0]+ orc.hitbox[3]:
				if orc.visible:
					orc.hit()
					score += 1
					bullets.pop(bullets.index(bullet))
#if the bullet crosses the screen pop the bullet else move the bullwt
		if bullet.x<screenwidth and bullet.x>0:
			bullet.x+=bullet.vel
		else:
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed()			#get the keys that was pressed

#shootloop should be zero for the bullet to be fired
	if keys[pygame.K_SPACE] and shootloop==0:
		if man.left:
			facing=-1
		else:
			facing=1
		if len(bullets)<5:			#max of 5 bullets can exist in the screen
			#append projectile if the bullet is fired- bulet comes from middle of the man
			bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2), 5,(0,0,0), facing))

		shootloop = 1


	if keys[pygame.K_LEFT] and man.x > 0:
		man.x-=man.vel
		man.left=True
		man.right=False
		man.standing=False
	elif keys[pygame.K_RIGHT] and man.x < screenwidth:
		man.x+=man.vel
		man.left=False
		man.right=True
		man.standing = False
	else:
		man.standing=True
		man.walkcount = 0


#-----------Jump-----------
	if not(man.jump):
		if keys[pygame.K_UP]:
			man.jump=True
			man.right=False
			man.left=False
			man.walkcount = 0

	else:
		if man.jumpcount >= -10:
			neg=1
			if man.jumpcount<0:
				neg=-1					#to make the man to come down
			man.y-= int((man.jumpcount**2)*0.5)*neg
			man.jumpcount -=1
		else:
			man.jump=False
			man.jumpcount=10
			
	redrawGameWindow() #redraw game window for every update
pygame.quit()