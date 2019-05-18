# This file is responsible for predicting the enemies plays by using N-Grams
import operator

PATH_TO_DECKS = "D:\\Projects\\Hearthbot_Old\\Decks\\"
#PATH_TO_DECKS = "C:\\Users\\User\\PycharmProjects\\HearthstoneAI\\hearthstoneai\\Decks\\"

PATHS_BY_CLASS = {}
for classname in ["Gul'dan;_WARLOCK","Druid;_DRUID","Mage;_MAGE","Hunter;_HUNTER","Uther Lightbringer;_PALADIN","Rogue;_ROGUE","Garrosh Hellscream;_WARRIOR","Priest;_PRIEST","Shaman;_SHAMAN"]:
	Pathlist = classname.split(";")
	PATHS_BY_CLASS[Pathlist[0]] = Pathlist[1] + "\decks.txt"

# The PATH_TO_DECKS and PATHS_BY_CLASS Variables are supposed to be Static.
# They depict the Path to a Textfile with the Downloaded Decks for the Class
# It's supposed to be used like this:  PathToFile = PATH_TO_DECKS + PATHS_BY_CLASS[ClassName]

class Ngram:
	content = [] # This contains two cards

	def __init__(self, cards):
		self.content = cards

	def getCards(self):
		return self.content

	def setCards(self, cards):
		if cards is not None:
			self.content = cards

	def __str__(self):
		String = "" + str(self.content)
		return String		

	# Self has to be a Bigram here! <-- IMPORTANT
	def compare(self,Trigram): # Compares two NGrams and returns the Intersection if exactly two cards overlap
		overlap = True
		for card in self.getCards():
			if card not in Trigram.getCards(): overlap = False
		if overlap:
			s = set(self.getCards())
			return s.symmetric_difference(Trigram.getCards()).pop() # This returns the Difference between the Bigram and the Trigram if 2 Cards overlap
		return None	


class PredictionHandler:
	CardsPlayedByOpponent = [] # These are all the cards wich have been played by the Opponent.
	DeckListsForClass = [] # This contains a List of Decklists for the Enemies Class.
	Class = ""

	def __init__(self, cardsplayed, className):
		self.CardsPlayedByOpponent = cardsplayed
		self.DeckListsForClass = self.getDecksByClass(className)
		self.Class = className


	# The Parameter mode changes wether the Ngrams are created for the OpponentsDeck or for the Prediction
	def makeNgrams(self, mode): # NEED TO DO IF CLAUSE FOR CLASS DECKLIST AND CARDSBYOPPONENT
		res = [] # This will be a List of Ngrams
		
		if mode == "Prediction":
			for Deck in self.DeckListsForClass:
				for card in Deck:
					for secondCard in Deck:
						if card != secondCard:
								res.append(Ngram([card, secondCard]))

		elif mode == "Opponent":
			for card in self.CardsPlayedByOpponent:
					res.append(Ngram([card]))
		return res

	def predict(self):
		if self.CardsPlayedByOpponent == []:
			if self.Class == "Warlock":
				self.CardsPlayedByOpponent = ["Kobold Librarian"]
			elif self.Class == "Druid":
				self.CardsPlayedByOpponent = ["Wild Growth"]
			elif self.Class == "Hunter":
				self.CardsPlayedByOpponent = ["Animal Companion"]
			elif self.Class == "Uther Lightbringer":
				self.CardsPlayedByOpponent = ["Righteous Protector"]
			elif self.Class == "Rogue":
				self.CardsPlayedByOpponent = ["Backstab"]
			elif self.Class == "Garrosh Hellscream":
				self.CardsPlayedByOpponent = ["Shield Block"]
			elif self.Class == "Priest":
				self.CardsPlayedByOpponent = ["Northshire Cleric"]
			elif self.Class == "Shaman":
				self.CardsPlayedByOpponent = ["Jade Claws"]
			elif self.Class == "Mage":
				self.CardsPlayedByOpponent = ["Fireball"]


		if self.CardsPlayedByOpponent == [] and self.DeckListsForClass == []:
			print("Lists are empty!")
			return
		res = {} # This Dict will contain all Cards and how often they appeared
		BigramsForOpponent = self.makeNgrams("Opponent")
		TrigramsFromDeck = self.makeNgrams("Prediction")
		#print(len(BigramsForOpponent))
		#print(len(TrigramsFromDeck))
		print(self.CardsPlayedByOpponent)
		for bigram in BigramsForOpponent:
			for trigram in TrigramsFromDeck:
				#print("blae")
				compare = bigram.compare(trigram)
				if compare != None:
					if compare in res: res[compare] += 1
					elif compare not in res: res[compare] = 1
		print("blae")
		sorted_res = sorted(res.items(), key=operator.itemgetter(1))
		sortedcards = [x[0] for x in sorted_res]# This returns a List of Tuples with the Key and Value of the Dict, sorted by the Value
		if sortedcards == []:
			sortedcards = ["Chillwind Yeti","Shieldbearer","Worgen Greaser","Stormwatcher","Ravenholdt Assassin","Ravenholdt Assassin","Wisp","Wisp","Murloc Raider","Murloc Raider","Bloodfen Raptor","Bloodfen Raptor","Stormwind Champion","Stormwind Champion","Argent Squire","Argent Squire","Goldshire Footman","Goldshire Footman","River Crocolisk","River Crocolisk","Oasis Snapjaw","Oasis Snapjaw","Angry Chicken","Angry Chicken","Grotesque Dragonhawk""Grotesque Dragonhawk","Am'gam Rager","Am'gam Rager","Duskboar","Duskboar"]
		return sortedcards
			
	def getDecksByClass(self, className):
		print("className")
		print(className)
		res = []
		Path = PATH_TO_DECKS + PATHS_BY_CLASS[className]
		with open(Path, "r") as file:
			for line in file.readlines(): # Each line is a different Deck
				deck = line.split("|")
				deck.pop() # Remove the Last item from the List because it is always "\n"
				res.append(deck)
		return res