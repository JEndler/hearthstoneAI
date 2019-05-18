from hearthstone import deckstrings
from _thread import start_new_thread
import pyperclip
from HSCard import HSCard
import Card
from Gamestate import Gamestate
from Move import Move
import HearthSimulation
import json
import time

class LogWatcher():

	def __init__(self, MyDeckFile = None):
		self.LogPath = "D:\\Hearthstone\\Hearthstone_Data\\output_log.txt"
		self.gamestate = Gamestate()
		self.hero = [None,None,None]  # Hunter, Rogue, Mage, Warlock, Paladin, Warrior, Priest, Druid, Shaman
		self.heroID = [None,None,None] # ID of the Hero Card
		self.lastFromPowerLog = None
		self.listOfHeroNames = ["Malfurion Stormrage", "Rexxar", "Jaina Proudmoore", "Uther Lightbringer",
								"Anduin Wrynn",
								"Valeera Sanguinar", "Thrall", "Gul'dan", "Garrosh Hellscream", "Alleria Windrunner",
								"Khadgar",
								"Medivh", "Lady Liadrin", "Prince Arthas", "Tyrande Whisperwind", "Maiev Shadowsong",
								"Morgl the Oracle",
								"Nesmy Necrofizzle", "Magni Bronzebeard"]
		start_new_thread(self.update,())
		self.watch()                        

	def watch(self):
		print("Watching")
		with open(self.LogPath, 'r', encoding="utf-8") as file:
			line = file.readline()
			print("in file")
			while True:
				nameOfCard = self.getName(line)
				idOfCard = self.getID(line)
				line = file.readline()
				if "entityName=UNKNOWN ENTITY" in line: continue
				elif "BLOCK_START BlockType=POWER" in line:
					if "UNKNOWN ENTITY" not in line:
						if "Target=0" not in line:  # Spell has a Target
							s = line.split("Target=")
							spell = self.getName(s[0])
							target = self.getName(s[1])
							idofSpell = self.getID(s[0])
							idofTarget = self.getID(s[1])
							SpellCard = HSCard(spell, idofSpell)
							if SpellCard.getType() is "SPELL":
								move = Move("playtargetedspell", actioncard=self.CheckCard(SpellCard),
											targetcard= self.CheckCard(self.getCardByID(idofTarget)))
							elif SpellCard.getType() is "MINION":
								move = Move("playtargetedminion", actioncard=self.CheckCard(SpellCard),
											targetcard= self.CheckCard(self.getCardByID(idofTarget)))
							result = spell + " has been played with target : " + target
							if self.lastFromPowerLog != result:
								HearthSimulation.simTurn(self.gamestate, move)
								self.lastFromPowerLog = result
								print(result)
						else:  # Spell has no Target
							s = line.split("Target=")
							spell = self.getName(s[0])
							idofSpell = self.getID(s[0])
							SpellCard = self.getCardByID(idofSpell)
							if SpellCard != None:
								if SpellCard.getType() is "SPELL":
									move = Move("playspell", actioncard=self.CheckCard(SpellCard))
								elif SpellCard.getType() is "MINION":
									move = Move("play", actioncard=self.CheckCard(SpellCard))
								result = spell + " has been played without target."

								if self.lastFromPowerLog != result:
									HearthSimulation.simTurn(self.gamestate, move)
									print(result)
									self.lastFromPowerLog = result
				elif "GameState.DebugPrintEntitiesChosen()" in line:
					print("Choice for Mulligan: " + self.getName(line))
				elif "to FRIENDLY HAND" in line:
					cardDrawn = HSCard(nameOfCard,idOfCard)
					cardDrawn.ID = idOfCard
					self.gamestate.addCardHand(cardDrawn, 1)
					print("to HAND:" + nameOfCard + "*** ID = " + idOfCard)

				elif "to FRIENDLY DECK" in line:
					cardToDeck = self.getCardByID(idOfCard)
					newCard = HSCard(cardToDeck.getName(), idOfCard)
					self.gamestate.destroy(cardToDeck)
					self.gamestate.addCardDeck(newCard,1)	

	def update(self):
		while True:
			time.sleep(3)
			self.printStatus()


	def getID(self, line):
		indexID = line.find(" id=")
		indexEndOfID = line.find("zone=")
		ID = line[indexID + 4:indexEndOfID - 1]
		return ID

	def getName(self, line):
		indexName = line.find("entityName=")
		indexEndOfName = line.find("id=")
		name = line[indexName + 11:indexEndOfName - 1]
		return name

	def getCardByID(self, ID):
		for player in [1, -1]:
			for card in self.gamestate.Board[player]:
				if card.ID == ID: return card
			for card in self.gamestate.Hand[player]:
				if card.ID == ID: return card
			for card in self.gamestate.Deck[player]:
				if card.ID == ID: return card
		print("ERROR : Card with ID:" + str(ID) + " not in play atm.")
		return None                
	
	def delete(self, list, name):
		for card in list:
			if name == card.getName():
				list.remove(card)

	def printStatus(self):
		print("*********STATUS***********")
		print("Cards in Hand:" + str([card.getName() for card in self.gamestate.Hand[1] if card is not None]))
		print("Cards on Board" + str([card.getName() for card in self.gamestate.Board[1] if card is not None]))
		print("Cards on EnemyBoard" + str([card.getName() for card in self.gamestate.Board[-1] if card is not None]))

	def CheckCard(self,card):
		if card is None:
			return 
		if card.getName() == self.hero[1] and card.ID == self.heroID[1]:
			return 1
		elif card.getName() == self.hero[-1] and card.ID == self.heroID[-1]:
			return -1
		elif card.getName() == self.gamestate.HeroPower[1]:
			print("Friendly Heropower was played")
			return None
		elif card.getName() == self.gamestate.HeroPower[-1]:
			print("Enemy Heropower was played")
			return None
		return card

Thiele = LogWatcher()