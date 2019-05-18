import pygame 

class GameElement:
	SCREEN_WIDTH = 1000
	SCREEN_HEIGHT = 800
	OBJECT_WIDTH = 120
	OBJECT_HEIGHT = 150
	RECT_WIDTH = 60
	RECT_HEIGHT = 90
	OBJECT_BORDER_WIDTH = int((OBJECT_WIDTH - RECT_WIDTH)/2)
	WHITE = [255,255,255]
	BLACK = [0,0,0]
	BLUE = [30,144,255]
	card_border_width = 6

	def __init__(self):
		pass

	def drawCircle(self,screen,pos):
		# pos=getPos()
		pygame.draw.circle(screen, self.BLACK, pos, 12)
		pygame.draw.circle(screen, self.WHITE, pos, 10)

	def drawStat(self,screen,pos,val):	
		pygame.draw.circle(screen, self.BLACK, pos, 12)
		pygame.draw.circle(screen, self.WHITE, pos, 10)
		myfont = pygame.font.SysFont('Comic Sans MS', 15)
		text = myfont.render("name", False, self.BLACK)
		#print(self.OBJECT_WIDTH-self.card_border_width)
		screen.blit(text,[10,10])

	def baseSurface(self,name="test"):
		#Base Card Surface
		BaseSurface = pygame.Surface([int(self.OBJECT_WIDTH),int(self.OBJECT_HEIGHT)])
		BaseSurface.fill(self.WHITE)
		#Actual Card Surface
		CardBorderSurface = pygame.Surface([int(self.RECT_WIDTH),int(self.RECT_HEIGHT)])
		CardBorderSurface.fill(self.BLACK)
		BaseSurface.blit(CardBorderSurface,[self.OBJECT_BORDER_WIDTH,self.OBJECT_BORDER_WIDTH])
		#White Card overlay for the Border
		CardOverlaySurface = pygame.Surface([int(self.RECT_WIDTH-self.card_border_width/2),int(self.RECT_HEIGHT-self.card_border_width/2)])
		CardOverlaySurface.fill(self.WHITE)
		BaseSurface.blit(CardOverlaySurface,[self.OBJECT_BORDER_WIDTH+self.card_border_width/3,self.OBJECT_BORDER_WIDTH+self.card_border_width/3])
		#Naming the Card
		myfont = pygame.font.SysFont('Comic Sans MS', 15)
		text = myfont.render(name, False, self.BLACK)
		#print(self.OBJECT_WIDTH-self.card_border_width)
		BaseSurface.blit(text,[self.OBJECT_BORDER_WIDTH, int(self.RECT_HEIGHT/3)])
		return BaseSurface
			
	def drawCard(self,screen,pos,name):
		pygame.draw.rect(screen, self.BLACK, pygame.Rect(pos[0],pos[1], self.RECT_WIDTH, self.RECT_HEIGHT))
		pygame.draw.rect(screen, self.WHITE, pygame.Rect(pos[0]+2,pos[1]+2, self.RECT_WIDTH-4, self.RECT_HEIGHT-4))
		#print(pos)
		self.drawCircle(screen,(int(pos[0]-(self.RECT_WIDTH/2)+(self.RECT_WIDTH/2)),int(pos[1]+(self.RECT_HEIGHT/2)+self.RECT_HEIGHT/2)))
		self.drawCircle(screen,(int(pos[0]-(self.RECT_WIDTH/2)+(self.RECT_HEIGHT/2)-14),int(pos[1]-(self.RECT_HEIGHT/2)+self.RECT_HEIGHT/2)))
		self.drawCircle(screen,(int(pos[0]+(self.RECT_WIDTH/2)+(self.RECT_HEIGHT/2)-14),int(pos[1]+(self.RECT_HEIGHT/2)+self.RECT_HEIGHT/2)))


class Minion(GameElement):
	name = ""
	surface = None
	atkval = 0
	defval = 0
	manacost = 0
	pos = [100,100]

	def __init__(self,screen,name="test"):
		self.surface = self.baseSurface(name=name)
		self.drawStatCircle(self.surface,(20,20),"5")
		self.drawCircle(self.surface,(20,20))
		screen.blit(self.surface,(self.SCREEN_WIDTH/2-self.RECT_WIDTH/2,40))
		# self.surface = pygame.Surface([int(self.RECT_WIDTH),int(self.RECT_HEIGHT)])
		# self.surface.fill(self.BLACK)
		# pygame.draw.rect(self.surface, self.WHITE, pygame.Rect(int(self.card_border_width/2),int(self.card_border_width/2), self.RECT_WIDTH-self.card_border_width, self.RECT_HEIGHT-self.card_border_width))
		# self.drawCircle(self.surface,[10,10],1)
		# #cardbody = pygame.Rect(self.pos[0],self.pos[1],self.RECT_WIDTH,self.RECT_HEIGHT)
		# #self.surface.blit(cardbody,(10,10))
		# screen.blit(self.surface,(self.SCREEN_WIDTH/2-self.RECT_WIDTH/2,40))

	def drawStatCircle(self,surface,pos,val):
		myfont = pygame.font.SysFont('Comic Sans MS', 12)
		val = myfont.render(val, False, self.BLACK)
		pygame.draw.circle(surface,self.BLACK,pos,8,6)
		surface.blit(val,pos)

	def drawStats(self,baseSurface,stats,manacost):
		myfont = pygame.font.SysFont('Comic Sans MS', 8)
		attack = myfont.render(stats[0], False, self.BLACK)
		health = myfont.render(stats[1], False, self.BLACK)
		manacost = myfont.render(manacost, False, self.BLACK)
		#print(self.OBJECT_WIDTH-self.card_border_width)
		self.drawCircle(baseSurface)
				


class Hero(GameElement):
	name = "test"
	surface = "x"
	def __init__(self,screen,name="test"):
		#print(self.RECT_HEIGHT)
		self.surface = pygame.Surface([int(self.RECT_WIDTH),int(self.RECT_HEIGHT)])
		self.surface.fill(self.BLACK)
		self.setName(name)
		screen.blit(self.surface,(self.SCREEN_WIDTH/2-self.RECT_WIDTH/2,40))

	def setPos(self,screen,x,y):
		screen.blit(self.surface,(x,y))

	def setName(self,name):
		myfont = pygame.font.SysFont('Comic Sans MS', 18)
		text = myfont.render(name, False, self.BLUE)
		self.surface.blit(text,[15,60])	

def main():
	pygame.init()
	pygame.font.init()
	
	screen = pygame.display.set_mode((GameElement.SCREEN_WIDTH,GameElement.SCREEN_HEIGHT))
	screen.fill(GameElement.BLUE)
	running = True
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	
		#pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(SCREEN_WIDTH/2-RECT_WIDTH/2, 30, 60, 60))
		card = Minion(screen)
		element = GameElement()
		#hero1.setName("Hero")
		#drawCircle(screen,(40,40),30)
		#element.drawCard(screen,[80,80],"test")
		pygame.display.flip()
		
if __name__ == '__main__':
	main()				
