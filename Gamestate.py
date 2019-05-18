from HSCard import HSCard
import random
import copy
import PredictionHandler
class Gamestate():
    SeenEnemyCards = []        #Seen Enemy Cards as String
    SeenCards = []          #Seen Friendly Cards as Strings
    Gamemode = []
    TurnNumber = 0
    ActivePlayer = 1        #1 or -1
    Gamemode = [[], [],[]]
    TurnNumber = 0
    Class = ["","",""]      #Class as string
    Deck = [[], [],[]]       # containing HSCards
    Hand = [[], [],[]]      #Board containing HSCards
    Board = [[], [],[]]     #Board containing HSCards
    EnemyCardLen = 0        #how many cards in enemies Hand
    EnemyDeckLen = 30       #how many cards the Enemy has in his Hand
    Health = [-1,-1, -1]    #Life as Int in List
    MaxHealth = [-1,-1,-1]  #Max Health achived per Healing in a List
    Armor = [0,0,0]         #Armor as Int in a List
    Weapon = [None,None,None] #Weapons as HSCards in a List
    Secret = [[], [], []]       #Secrets as HSCards in a List
    ManaCrystals = [0,0,0]  #ManaCrystals as Int in a List
    EmptyManaCrystals = [0, 0, 0] #EmptyManaCrystals as Int in a List
    Fatigue = [0,0,0]           #Fatigue as Ints in a List
    Enchantments = [[], [], []] #Enchantments as HSCards in a List
    Quest = ["", ""]          
    SpellsPlayed = [[], [], []] #Spells played as Int in a List
    MinionsPlayed = [[], [],[]] #Minions played as Int in a List
    MinionsDied = [[], [], []]  # MinionsDied as Int in a List
    CardsPlayedThisTurn = [[], [], []] #Cards played this Turn as HSCard in a List
    JadeCount = [0, 0,0]        #JadeCount as Int in a List
    CthunStats = [0,0,0]         #Attack as Int in a List
    HeroPower = ["","",""]
    HeroPowerUsed = False
    Gameover = False
    Graveyard = [[],[],[]]
    Winner = 0
    HeroAttack = [-1,-1,-1]
    HeroArmor = [-1,-1,-1]
    Numberofsecretsplayed = [0,0,0]
    Numberofotherclasscardsplayed = [0,0,0]
    Numberoftotemsplayed = [0,0,0]
    Numberofspellsplayed = [0,0,0]
    #todo reset the following after every Round
    Numberofspellsthisturnmorefivecost = [0,0,0]
    Numberofoverloadedmanacrystals = [0,0,0]

    #todo till here
  #  def __init__(self):
        #watcher = lw.LogWatcher()
        #lw.watch()
        #Player1_Class = lw.getFriendlyClass()
      #  pass
   #Todo test version of init

    def __init__(self):
        self.Health = [30, 30, 30]
    def getMana(self, Player):
        return self.ManaCrystals[Player]
    #def addManaSpace(self, player):
        #todo
    def getClass(self,player):
        return self.Class[player]
   #def adjCThunHealth(self,amount,player):
        #todo
    #def adjCThunAttack(self,amount,player):
        #todo
    def getOpponentClass(self,player):
        return self.Class[player]
    def getCardBoardPos(self, card):
        return self.Board[card.player].index(card)
    def getCardHandPos(self,card):
        return self.Hand[card.player].index(card)
    def draw(self, player):
        if len(self.Deck[player]) > 0:
            card = random.choice(self.Deck[player])
            if len(self.Hand[player]) < 7:
                self.Hand[player].append(card)
        else:
            self.Fatigue[player] += 1
            self.Health[player] -= self.Fatigue[player]
    def adjArmor(self,amount,player):
        self.Armor[player]+= amount
    def addManaCrystal(self, player):
        if self.ManaCrystals[player] < 10:
            self.ManaCrystals+=1
    def adjHealth(self,amount, player):
        if self.Armor[player] > 0:
            if self.Armor[player] > amount:
                self.Armor[player]-= amount
            else:
                self.Health[player] += (amount-self.Armor[player])
                self.Armor[player] = 0
        else:
            self.Health[player] += amount
        #todo remove armor first dont heal more than 30
        #todo
   # def summonJade(self,player):
        #todo
 #   def adjWeapon(self,player,amAttack,amHealth):
        #todo
   # def setCardAttack(self,card,player):
        #todo
    #def setCardHealth(self,card,player):
        #todo
    def healHealth(self, hero, amount):
        self.Health += amount
    def healCardHealth(self,card,amount):
        card.adjHealth(amount)
        if card.Health < 0:
            card.destroy()
    def adjCardHealth(self,card, ammount):
        card.adjHealth(ammount)
    def adjCardAttack(self,card, ammount):
        card.adjHealth(ammount)
    def summon(self, card,player):
        card.reset()
        if self.Board[player]<7:
            self.Board.append(card)

    def reset(self):
        self.SeenEnemyCards = []  # Seen Enemy Cards as String
        self.SeenCards = []  # Seen Friendly Cards as Strings
        self.Gamemode = []
        self.TurnNumber = []
        self.ActivePlayer = 1  # 1 or -1
        self.Gamemode = [[], [], []]
        self.TurnNumber = 0
        self.Class = [[], [], []]  # Class as string
        self.Deck = [[], [], []]  # containing HSCards
        self.Hand = [[], [], []]  # Board containing HSCards
        self.Board = [[], [], []]  # Board containing HSCards
        self.EnemyCardLen = 0  # how many cards in enemies Hand
        self.EnemyDeckLen = 30  # how many cards the Enemy has in his Hand
        self.Health = [30, 30, 30]  # Life as Int in List
        self.MaxHealth = [30, 30, 30]  # Max Health achived per Healing in a List
        self.Armor = [0, 0, 0]  # Armor as Int in a List
        self.Weapon = [None, None, None]  # Weapons as HSCards in a List
        self.Secret = [[], [], []]  # Secrets as HSCards in a List
        self.ManaCrystals = [0, 0, 0]  # ManaCrystals as Int in a List
        self.EmptyManaCrystals = [0, 0, 0]  # EmptyManaCrystals as Int in a List
        self.Fatigue = [0, 0, 0]  # Fatigue as Ints in a List
        self.Enchantments = [[], [], []]  # Enchantments as HSCards in a List
        self.Quest = ["", ""]  # Fuck these
        self.SpellsPlayed = [[], [], []]  # Spells played as Int in a List
        self.MinionsPlayed = [[], [], []]  # Minions played as Int in a List
        self.MinionsDied = [[], [], []]  # MinionsDied as Int in a List
        self.CardsPlayedThisTurn = [[], [], []]  # Cards played this Turn as HSCard in a List
        self.JadeCount = [0, 0, 0]  # JadeCount as Int in a List
        self.CthunStats = [0, 0, 0]  # Attack as Int in a List
        self.Value = -1
        self.HeroPower = ["", "", ""]
        self.HeroPowerUsed = False
        self.Gameover = False
        self.Graveyard = [[], [], []]
        self.Winner = 0
        self.HeroAttack = [-1, -1, -1]
        self.HeroArmor = [-1, -1, -1]
        self.Numberofsecretsplayed = [0, 0, 0]
        self.Numberofotherclasscardsplayed = [0, 0, 0]
        self.Numberoftotemsplayed = [0, 0, 0]
        self.Numberofspellsplayed = [0, 0, 0]
        # todo reset the following after every Round
        self.Numberofspellsthisturnmorefivecost = [0, 0, 0]
        self.Numberofoverloadedmanacrystals = [0, 0, 0]

    def destroyByID(self, id):
        for card in self.Board[1]:
            if card.ID == id:
                self.Board[1].remove(card)
        for card in self.Hand[1]:
            if card.ID == id:
                self.Hand[1].remove(card)
        for card in self.Deck[1]:
            if card.ID == id:
                self.Deck[1].remove(card)

    def fillup(self):
        X = self.SeenEnemyCards
        print(len(X))
        print(str(self.Class[-1]))
        Thiele = PredictionHandler.PredictionHandler(cardsplayed=X, className=str(self.Class[-1]))
        print("cds")

        predictList = Thiele.predict()
        print("q")
        #predictList = ["Blessing of Might","Blessing of Might","Gnomish Inventor","Gnomish Inventor","Goldshire Footman","Goldshire Footman","Hammer of Wrath","Hammer of Wrath","Hand of Protection","Hand of Protection","Holy Light","Holy Light","Ironforge Rifleman","Ironforge Rifleman","Light's Justice","Light's Justice","Lord of the Arena","Lord of the Arena","Nightblade","Nightblade","Raid Leader","Raid Leader","Stonetusk Boar","Stonetusk Boar","Stormpike Commando","Stormpike Commando","Stormwind Champion","Stormwind Champion","Stormwind Knight","Stormwind Knight"]
        idnr = 100
        print("abc")
        cardlist = predictList[:self.EnemyCardLen]
        for i in range(self.EnemyCardLen):
            self.Hand[-1].append(HSCard(random.choice(predictList[:30]),idnr))
            idnr+=1
        for i in range(30-len(self.SeenEnemyCards)-self.EnemyCardLen):
            #print(self.Deck)
            self.Deck[-1].append(HSCard(random.choice(predictList[:30]),idnr))
            idnr += 1
        with open("MyDeck.txt") as f:
            for line in f:
                Seen = copy.deepcopy(self.SeenCards)
                if line in Seen:
                    Seen.remove(line)
                else:
                    self.Deck[1].append(HSCard(line[:-1],44))
        random.shuffle(self.Deck[1])
        random.shuffle(self.Deck[2])

    def deepcopystate(self):
        CopiedBoard = [[],[],[]]
        CopiedHand = [[],[],[]]
        CopiedDeck = [[],[],[]]
        CopiedMana = [0,0,0]
        CopiedHealth = [0,0,0]
        CopiedEmptyMana = [0,0,0]
        CopiedFatigue = [0,0,0]
        CopiedArmor = [0,0,0]
        CopiedseenEnemy = [[],[],[]]
        for player in [-1,1]:
            for card in self.Board[player]:
                CopiedCard = HSCard(card.getName(),card.ID)
                CopiedBoard[player].append(CopiedCard)
            for card in self.Hand[player]:
                CopiedCard = HSCard(card.getName(),card.ID)
                CopiedHand[player].append(CopiedCard)
            for card in self.Deck[player]:
                CopiedCard = HSCard(card.getName(),card.ID)
                CopiedDeck[player].append(CopiedCard)
            for card in self.SeenEnemyCards:
                CopiedCard = card
                CopiedseenEnemy.append(CopiedCard)

            for player in [0,1,2]:
                CopiedHealth[player] = self.Health[player]
                CopiedEmptyMana[player] = self.EmptyManaCrystals[player]
                CopiedMana[player] = self.ManaCrystals[player]
                CopiedFatigue[player] = self.Fatigue[player]
                CopiedArmor[player] = self.HeroArmor[player]
        CopiedGamestate = Gamestate()
        CopiedGamestate.Board = CopiedBoard
        CopiedGamestate.Deck = CopiedDeck
        CopiedGamestate.Hand = CopiedHand
        CopiedGamestate.ManaCrystals = CopiedMana
        CopiedGamestate.Health = CopiedHealth
        CopiedGamestate.EmptyManaCrystals = CopiedEmptyMana
        CopiedGamestate.ActivePlayer = self.ActivePlayer
        CopiedGamestate.Fatigue = CopiedFatigue
        CopiedGamestate.HeroArmor = CopiedArmor
        CopiedGamestate.SeenEnemyCards = CopiedseenEnemy
        CopiedGamestate.EnemyDeckLen = self.EnemyDeckLen
        CopiedGamestate.EnemyCardLen = self.EnemyCardLen


        return CopiedGamestate

    def summonfromHand(self, card):
        card.reset()
        if self.Board[card.player]<7:
            self.Board[card.player].append(card)
            self.Hand[card.player].remove(card)
    def summonfromdeck(self, card):
        card.reset()
        if self.Board[card.player]<7:
            self.Board[card.player].append(card)
            self.Deck[card.player].remove(card)
    def discard(self, card):
        self.Hand[card.player].remove(card)
    def discordRandom(self,player):
        card = random.choice(self.Hand[player])
        self.Hand[player].remove(card)
  #  def getMinnionsHand(self):
        #todo retrun list of minionis on hand
    def destroy(self, card):
        if card in self.Board[card.player]:
            self.Board[card.player].remove(card)
        if card in self.Hand[card.player]:
            self.Hand[card.player].remove(card)
        if card in self.Deck[card.player]:
            self.Deck[card.player].remove(card)
    def addCardDeck(self, card, player):
        if len(self.Deck[player]) == 0:
            self.Deck[player] = [card]
        else:
            index = random.randint(0,len(self.Deck[player])-1)
            self.Deck[player] = self.Deck[player][:index] + [card] + self.Deck[player][index:]
            card.player = player
    def addCardHand(self,card,player):
        if len(self.Hand[player]) < 10:
            self.Hand[player].append(card)
            card.player = player
    def addCardBoard(self,card,player):
        if len(self.Board[player]) < 7:
            self.Board[player].append(card)
            card.player = player

    def clone(self):
        return copy.deepcopy(self)

                #    def getAktivePlayer(self):  
#        return self.AktivePlayer