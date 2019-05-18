import numpy as np
import Card as cards
#import HearthSimulation as HearthSim


class HSCard():
	FirstName = "" #for cards like shifter zerus
	Name = ""
	Type = ""  # TYPE MINION, SPELL, ENCHANTMENT, HERO POWER, WEAPON or HERO
	Health = -1
	Attack = -1
	Stats = np.array([Health, Attack])
	Durability = -1
	Cost = -1  # NORMAL COST WITHOUT REDUCTIONS
	OriginalCost = -1
	CardClass = "NEUTRAL"
	Collectible = True
	Mechanics = []  # ["CHARGE", "BATTLECRY"]
	MaxHealth = -1
	MaxHealth = -1
	ID = 0
	CardId = 0

	# LIST OF ALL MECHANICS --->
	# ADJACENT_BUFF, AI_MUST_PLAY, AURA -> (Aura Buffs e.g.["Stormwind Champion"]), BATTLECRY, CHARGE,
	# CHOOSE_ONE, COMBO, COUNTER -> (Essentially just Counterspell), DEATHRATTLE,
	# DISCOVER, DIVINE_SHIELD, ENRAGED, FORGETFUL -> (50% to Attack the wrong target), FREEZE, IMMUNE, INSPIRE,
	# JADE_GOLEM,
	# MORPH -> (Cards such as ["Polymorph"] or ["Devolve"]), OVERLOAD, POISONOUS,
	# RITUAL -> (C'Thun Buffs such as ["C'Thun's Chosen"]), SECRET, SILENCE, STEALTH, SPELLPOWER, TAG_ONE_TURN_EFFECT,
	# TAUNT, TOPDECK -> Cards that reveal themselves when drawn e.g. ["Flame Leviathan"], UNTOUCHABLE,
	# WINDFURY, ImmuneToSpellpower -> (Cards that don't increase their Damage normally such as ["Arcane Missiles"]),
	# InvisibleDeathrattle -> (Used for some Boss Fights)
	# ENTOURAGE -> (Cards wich create random Cards from a given Pool such as ["Ysera"], ["Animal Companion"])

	Set = ""  # BASIC, CLASIC, ONE NIGHT IN KARAZHAN
	MultiClassGroup = ""  # JADE_LOTUS, GRIMY_GOONS or KABAL
	Faction = ""  # ALLIANCE or HORDE
	Race = ""  # MURLOC, BEAST, DRAGON, MECHANICAL, DEMON, ELEMENTAL, TOTEM or PIRATE
	Text = ""
	Source = ""  # CREATED BY e.g. PRIMORDIAL GLYPH
	Alive = True
	canAttack = False
	Player = 0
	SpellDamage = -1

	def __init__(self, name, id):
		self.ID = id
		self.CardId = id
		card = cards.cards.searchname(name)
		self.Name = name
		self.FirstName = name
		self.Pos = 0
		if card is not -1:
			if card["type"] == "MINION":
				self.Stats = np.array([card["attack"], card["health"]])
				self.Health = card["health"]
				self.Attack = card["attack"]
				self.Type = "MINION"
				if "race" in card: self.Race = card["race"]
				if "faction" in card: self.Faction = card["faction"]
				if "MultiClassGroup" in card: self.MultiClassGroup = card["MultiClassGroup"]

			elif card["type"] == "SPELL":
				self.Type = "SPELL"
			elif card["type"] == "WEAPON":
				self.Type = "WEAPON"
				self.Attack = card["attack"]
				self.Durability = card["durability"]
			elif card["type"] == "HERO":
				self.Health = 0
				self.Attack = 0
				self.Type == "Hero"
			elif card["type"] == "HERO POWER":
				self.Type == "Hero"
			elif card["type"] == "ENCHANTMENT":
				pass
			if "CardClass" in card: self.CardClass = card["CardClass"]
			if "mechanics" in card: self.Mechanics = card["mechanics"]
			if "set" in card: self.Set = card["set"]
			if "text" in card: self.Text = card["text"]
			if "cost" in card: self.Cost = card["cost"]


	def __repr__(self):
		return self.Name
	#GET-METHODS
	def getName(self):
		return self.Name
	def getType(self):
		return self.Type
	def getHealth(self):
		return self.Health
	def getAttack(self):
		return self.Attack
	def getStats(self):
		return self.Stats
	def getDurability(self):
		return self.Durability
	def getCost(self):
		return self.Cost
	def getCardClass(self):
		return self.CardClass
	def getCollectible(self):
		return self.Collectible
	def getMechanics(self):
		return self.Mechanics
	def getSet(self):
		return self.Set
	def getMultiClassGroup(self):
		return self.MultiClassGroup
	def getFaction(self):
		return self.Faction
	def getRace(self):
		return self.Race
	def Adapt(self):
		pass
		#todo
	def getText(self):
		return self.Text
	def getSource(self):
		return self.Source
	#SET-METHODS
	def setSource(self, source):
		self.Source = source
	def setHealth(self, health):
		self.Health = health
	def adjHealth(self, Ammount):
		self.Health += Ammount
	def adjAttack(self, Ammount):
		self.Attack -= Ammount
	#def Health(self, ammount):
		#todo
		pass
	#def Attack(self,ammount):
		#todo
	#	pass
	def Reset(self):
		#todo
		pass
	def setAttack(self, attack):
		self.Attack = attack
	def setCost(self, cost):
		self.Cost = cost
	def getPosition(self):
		pass
	def getMaxHealth(self):
		#todo
		pass

	#def checkdie(self):

	def triggerDeathrattle(self):
		pass
	#def getCardsForClass(self, class):
		#TODO
print(HSCard("Murloc Tidecaller",9).Attack)

#cardlist

list = cards.cards.getJsonFromFile()
cardlist = []
for card in list:
	cardlist.append(card)
