import HearthSimulation
import MCTree
import LogWatcherv2
import copy
import Gamestate
import time
import MCTree
import LogWatcherv2
import copy
import HearthSimulation
import Move
import HSCard
import numpy
import Actions
import pickle
start_time = time.time()
#Log = LogWatcherv2.LogWatcherv2()
## Log.decodeDeckstring("",True)
#gamestate = Log.gamestate
gamestate = Gamestate.Gamestate()
gamestate.Class = ["Uther Lightbringer","Uther Lightbringer","Uther Lightbringer"]
Wisp = HSCard.HSCard("Wisp",1)
Dusk = HSCard.HSCard("Duskboar",3)
#Dusk.canAttack = True
Wisp.canAttack = True
 
gamestate.Hand = [[],[HSCard.HSCard("Snowflipper Penguin",1),HSCard.HSCard("Snowflipper Penguin",2),HSCard.HSCard("Wisp",3),HSCard.HSCard("Wisp",4),HSCard.HSCard("Dire Mole",5),
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
 
gamestate.Board = [[],[],[]]
gamestate.ManaCrystals = [1,1,1]
 
print(gamestate.Board)
print(gamestate.Hand)
gamestate.fillup()
print(gamestate.Board)
print(gamestate.Hand)
print(gamestate.Deck)
print(gamestate.ManaCrystals)
 
 
Wins = [0,0]
for num_Games in range(30):
    Temp_Gamestate = copy.deepcopy(gamestate)
    while HearthSimulation.checkIfRunning(Temp_Gamestate):
        if Temp_Gamestate.ActivePlayer == 1:
            NewMove =  MCTree.FindMoveOne(Temp_Gamestate, 2)
        else:
            NewMove = MCTree.RandomMove(Temp_Gamestate)
        HearthSimulation.simTurn(Temp_Gamestate,NewMove)
        #print("____________________")
        #print(Temp_Gamestate.Health)
        #print(Temp_Gamestate.ManaCrystals)
    Winner = HearthSimulation.checkEndGame(Temp_Gamestate)
    Winner = (Winner + 1)/2
    Wins[int(Winner)] += 1
    print(Wins)
 
print(Wins)