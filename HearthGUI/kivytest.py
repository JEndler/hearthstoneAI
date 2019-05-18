import pygame
import random
import Gamestate
import HSCard
import HearthSimulation
import MCTree
import math
 
 
 
gamestate = Gamestate.Gamestate()
gamestate.Class = ["Uther Lightbringer","Uther Lightbringer","Uther Lightbringer"]
Wisp = HSCard.HSCard("Wisp",1)
Dusk = HSCard.HSCard("Duskboar",3)
#Dusk.canAttack = True
Wisp.canAttack = True
 
#https://console.cloud.google.com/cloudshell/editor?project=hearthsimserver&organizationID
 
gamestate.Deck = [[],[HSCard.HSCard("Snowflipper Penguin",1),HSCard.HSCard("Snowflipper Penguin",2),HSCard.HSCard("Wisp",3),HSCard.HSCard("Wisp",4),HSCard.HSCard("Dire Mole",5),
                      HSCard.HSCard("Murloc Raider",6),HSCard.HSCard("Bloodfen Raptor",7),HSCard.HSCard("Bloodfen Raptor",8),HSCard.HSCard("Murloc Raider",9),HSCard.HSCard("Duskboar",10),
                      HSCard.HSCard("Duskboar",11),HSCard.HSCard("River Crocolisk",12),HSCard.HSCard("River Crocolisk",13),HSCard.HSCard("Am'gam Rager",14),HSCard.HSCard("Am'gam Rager",15),
                      HSCard.HSCard("Chillwind Yeti",16),HSCard.HSCard("Chillwind Yeti",17),HSCard.HSCard("Oasis Snapjaw",18),HSCard.HSCard("Oasis Snapjaw",19),HSCard.HSCard("Worgen Greaser",20),
                      HSCard.HSCard("Worgen Greaser",21),HSCard.HSCard("Boulderfist Ogre",22),HSCard.HSCard("Boulderfist Ogre",23),HSCard.HSCard("Core Hound",24),HSCard.HSCard("Core Hound",25),
                      HSCard.HSCard("War Golem",26),HSCard.HSCard("War Golem",27),HSCard.HSCard("Eldritch Horror",28),HSCard.HSCard("Eldritch Horror",29),HSCard.HSCard("Faceless Behemoth",30)],
                  [HSCard.HSCard("Snowflipper Penguin",19),HSCard.HSCard("Snowflipper Penguin",29),HSCard.HSCard("Wisp",39),HSCard.HSCard("Wisp",49),HSCard.HSCard("Dire Mole",59),HSCard.HSCard("Murloc Raider",69),
                   HSCard.HSCard("Bloodfen Raptor",79),HSCard.HSCard("Bloodfen Raptor",98),HSCard.HSCard("Murloc Raider",99),HSCard.HSCard("Duskboar",910),HSCard.HSCard("Duskboar",191),
                   HSCard.HSCard("River Crocolisk",192),HSCard.HSCard("River Crocolisk",193),HSCard.HSCard("Am'gam Rager",914),HSCard.HSCard("Am'gam Rager",159),HSCard.HSCard("Chillwind Yeti",169),
                   HSCard.HSCard("Chillwind Yeti",917),HSCard.HSCard("Oasis Snapjaw",198),HSCard.HSCard("Oasis Snapjaw",199),HSCard.HSCard("Worgen Greaser",920),HSCard.HSCard("Worgen Greaser",291),
                   HSCard.HSCard("Boulderfist Ogre",229),HSCard.HSCard("Boulderfist Ogre",923),HSCard.HSCard("Core Hound",249),HSCard.HSCard("Core Hound",925),HSCard.HSCard("War Golem",269),
                   HSCard.HSCard("War Golem",271),HSCard.HSCard("Eldritch Horror",281),HSCard.HSCard("Eldritch Horror",219),HSCard.HSCard("Faceless Behemoth",301)]]
 
gamestate.Board = [[],[HSCard.HSCard("Snowflipper Penguin",1),HSCard.HSCard("Wisp",3),HSCard.HSCard("Dire Mole",5),
                      HSCard.HSCard("Murloc Raider",6)],
                  [HSCard.HSCard("Wisp",39),HSCard.HSCard("Dire Mole",59),HSCard.HSCard("Murloc Raider",69),
                   HSCard.HSCard("Bloodfen Raptor",79)]]
 
gamestate.Hand = [[],[HSCard.HSCard("Boulderfist Ogre",22),HSCard.HSCard("Core Hound",24),
                      HSCard.HSCard("War Golem",26)],
                  [HSCard.HSCard("Wisp",39),HSCard.HSCard("Wisp",49),HSCard.HSCard("Dire Mole",59),HSCard.HSCard("Murloc RaIDer",69),
                   HSCard.HSCard("Bloodfen Raptor",79)]]
gamestate.ManaCrystals = [10,10,10]
 
 
 
 
 
 
 
 
 
 
 
pygame.init()
 
screen = pygame.display.set_mode([1500,1000])
info = pygame.display.Info()
print(info)
pygame.display.set_caption("Jugend Forscht Simulation")
 
running = True
 
W = screen.get_width()
H = screen.get_height()
FPS = 30
 
StatFont = pygame.font.SysFont("Times New Roman", 20)
NameFont = pygame.font.SysFont("Times New Roman", 15,bold=True)
GameFont = pygame.font.SysFont("Times New Roman", 35, bold=True)
 
 
 
 
 
 
# Initialize keymap.
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
ENTER = 4
controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER]
keymap = dict()
keys = controls
for k in keys: keymap[k] = False
 
 
def Gamestate_to_Board(gamestate):
 
    Hand = gamestate.Hand
    Board = gamestate.Board
    HeroHealth = gamestate.Health
 
    for _ in range(1,3):
 
        for index, card in enumerate(Hand[_], start=0):
 
            newcard = pygame.Surface([120, 150])
            newcard.fill((200,200,200))
 
            pygame.draw.rect(newcard,(0,255,255),(5,5,50,40),4)
            pygame.draw.rect(newcard, (200, 0, 0), (65, 105, 50, 40), 4)
            pygame.draw.rect(newcard, (200, 255, 0), (5, 105, 50, 40), 4)
 
            Mana = StatFont.render(str(Hand[_][index].Cost),False,(0,0,0))
            Health = StatFont.render(str(Hand[_][index].Health),False , (0,0,0))
            Attack = StatFont.render(str(Hand[_][index].Attack),False,(0,0,0))
            Name = NameFont.render(str(Hand[_][index].Name),False,(0,0,0))
 
            newcard.blit(Mana, (20, 15))
            newcard.blit(Health, (80, 115))
            newcard.blit(Attack, (20, 115))
            newcard.blit(Name,(5,65))
 
            if _ == 1:
                screen.blit(newcard,(20+index*(10+120),50))
            else:
                screen.blit(newcard, (20 + index * (10 + 120), 700))
 
 
    for _ in range(1,3):
 
        newcard = pygame.Surface([120, 250])
        newcard.fill((200, 200, 200))
 
        pygame.draw.rect(newcard, (255, 0, 0), (30, 100, 60, 50), 4)
 
        newcard.blit(StatFont.render(str(HeroHealth[_]),False,(0,0,0)), (50, 115))
 
        if _ == 1:
            screen.blit(newcard, (1350, 50))
        else:
            screen.blit(newcard, (1350, 600))
 
 
    for _ in range(1,3):
 
        for index, card in enumerate(Board[_], start=0):
 
            newcard = pygame.Surface([120, 150])
            newcard.fill((200,200,200))
 
            pygame.draw.rect(newcard,(0,255,255),(5,5,50,40),4)
            pygame.draw.rect(newcard, (200, 0, 0), (65, 105, 50, 40), 4)
            pygame.draw.rect(newcard, (200, 255, 0), (5, 105, 50, 40), 4)
 
            Mana = StatFont.render(str(Board[_][index].Cost),False,(0,0,0))
            Health = StatFont.render(str(Board[_][index].Health),False , (0,0,0))
            Attack = StatFont.render(str(Board[_][index].Attack),False,(0,0,0))
            Name = NameFont.render(str(Board[_][index].Name), False, (0, 0, 0))
 
            newcard.blit(Mana, (20, 15))
            newcard.blit(Health, (80, 115))
            newcard.blit(Attack, (20, 115))
            newcard.blit(Name, (5, 65))
 
            if _ == 1:
                screen.blit(newcard,(20+index*(10+120),230))
            else:
                screen.blit(newcard, (20 + index * (10 + 120), 520))
 
Crosshair = 0
keyup = False
LegalMoves = HearthSimulation.listoflegalmoves(gamestate)
 
 
def draw_arrow(screen, colour, start, end):
    pygame.draw.line(screen, colour, start, end, 5)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(screen, (255, 0, 0), (
        (end[0] + 20 * math.sin(math.radians(rotation)), end[1] + 20 * math.cos(math.radians(rotation))), (
            end[0] + 20 * math.sin(math.radians(rotation - 120)), end[1] + 20 * math.cos(math.radians(rotation - 120))),
        (end[0] + 20 * math.sin(math.radians(rotation + 120)),
         end[1] + 20 * math.cos(math.radians(rotation + 120)))))
 
StartPoint = [0,0]
EndPoint = [0,0]
 
while running:
    screen.fill((0, 0, 200))
 
    if gamestate.ActivePlayer == -1:
        screen.blit(GameFont.render("It is your Turn", False, (0, 255, 0)), (0, 900))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keymap[event.key] = True
            elif event.type == pygame.KEYUP:
                keymap[event.key] = False
                keyup = False
 
        for dir in [0, 1, 2, 3, 4]:
            if keymap[controls[dir]]:
                if dir == LEFT:
                    if keyup == False:
                        if Crosshair > 0:
                            Crosshair-=1
                        keyup = True
                if dir == RIGHT:
                    if keyup == False:
                        if Crosshair < len(LegalMoves)-1:
                            Crosshair+=1
                        keyup = True
                if dir == UP:
                    if keyup == False:
                        HearthSimulation.simTurn(gamestate, LegalMoves[Crosshair])
                        LegalMoves = HearthSimulation.listoflegalmoves(gamestate)
                        Crosshair = 0
                        keyup = True
 
        Move = LegalMoves[Crosshair]
        StartPoint = [0,0]
        EndPoint = [0,0]
 
        if Move.type == "end":
            pass
        elif Move.type == "play":
            for index, card in enumerate(gamestate.Hand[-1], start=0):
                if Move.actioncard != None and Move.actioncard not in [0, 1, -1]:
                    if card.ID == Move.actioncard.ID:
                        StartPoint = (20 + index * (10 + 120), 700)
            EndPoint = (30 + len(gamestate.Board[-1]) * (10 + 120), 580)
        elif Move.type == "attack":
            for index, card in enumerate(gamestate.Board[-1], start=0):
                if Move.actioncard != None and Move.actioncard not in [0, 1, -1]:
                    if card.ID == Move.actioncard.ID:
                        StartPoint = (20 + index * (10 + 120), 520)
            for index, card in enumerate(gamestate.Board[1], start=0):
                if Move.target != None and Move.target not in [0,1,-1]:
                    if card.ID == Move.target.ID:
                        EndPoint = (20 + index * (10 + 120), 380)
            if Move.target == 1:
                EndPoint = (1350, 250)
 
 
 
 
 
 
 
 
 
    elif gamestate.ActivePlayer == 1:
        screen.blit(GameFont.render("It is the AI's Turn", False, (255, 0, 0)), (0,900))
        HearthSimulation.simTurn(gamestate,MCTree.RandomMove(gamestate))
        LegalMoves = HearthSimulation.listoflegalmoves(gamestate)
 
 
 
 
    screen.blit(GameFont.render(str(LegalMoves[Crosshair]), False, (255, 0, 0)), (400,900))
    Gamestate_to_Board(gamestate)
 
    if gamestate.ActivePlayer == -1:
        draw_arrow(screen, (255, 0, 0), StartPoint, EndPoint)
 
    pygame.display.update()
 
 
 
def Gamestate_to_Board(gamestate):
 
    Hand = gamestate.Hand
    Board = gamestate.Board
    Hero = gamestate.Hero
 
 
 
 
 
 
pygame.quit()