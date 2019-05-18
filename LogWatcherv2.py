from _thread import start_new_thread
from hearthstone import deckstrings
import pyperclip
from HSCard import HSCard
import Card
from Gamestate import Gamestate
from Move import Move
import HearthSimulation
import json
import time


class LogWatcherv2:
    def __init__(self, deckstring=None, copiedToClipboard=False):
        self.firstRotation = True
        self.coinLook = False
        self.LogPath = "E:\\Hearthstone\\Hearthstone_Data\\output_log.txt"
        #self.LogPath = "D:\\Hearthstone\\Hearthstone_Data\\output_log.txt"
        self.Log_Power = self.LogPath  # + "\\Power.log"
        self.Log_Zone = self.LogPath  # + "\\Zone.log"
        self.gamestate = Gamestate()
        self.gamestate.ManaCrystals = [0, 0, 0]
        self.activePlayer = -1
        self.muliganInt = 0
        self.listOfHeroNames = ["Malfurion Stormrage", "Rexxar", "Jaina Proudmoore", "Uther Lightbringer",
                                "Anduin Wrynn",
                                "Valeera Sanguinar", "Thrall", "Gul'dan", "Garrosh Hellscream", "Alleria Windrunner",
                                "Khadgar",
                                "Medivh", "Lady Liadrin", "Prince Arthas", "Tyrande Whisperwind", "Maiev Shadowsong",
                                "Morgl the Oracle",
                                "Nesmy Necrofizzle", "Magni Bronzebeard"]

        self.deck = []
        self.hero = [None, None, None]  # Hunter, Rogue, Mage, Warlock, Paladin, Warrior, Priest, Druid, Shaman
        self.heroID = [None, None, None]  # ID of the Hero Card
        self.format = "Standart"
        self.counterDict = {}
        self.cardsPlayedThisTurn = []
        self.minionsDiedThisTurn = []
        self.minionsThatAttackedThisTurn = []
        self.numOfAttacksThisTurn = []
        self.spellsPlayedThisTurn = []
        self.lastFromPowerLog = None
        self.ID = 1000
        if deckstring is not None and not copiedToClipboard:
            self.deck, self.hero, self.format = self.decodeDeckstring(deckstring)
        if copiedToClipboard:
            self.deck, self.hero, self.format = self.decodeDeckstring(deckstring, copiedToClipboard=True)
        for card in self.deck: print(card.name)
        # start_new_thread(self.update,())
        self.watch()

    def watch(self):
        print("Watch")
        counter = 1
        with open(self.Log_Zone, 'r', encoding="utf-8") as file:
            line = file.readline()
            while line:
                line = file.readline()
                nameOfCard = self.getName(line)
                idOfCard = self.getID(line)
                if "entityName=UNKNOWN ENTITY" in line: continue
                if "to FRIENDLY HAND" in line:
                    print(line)
                    cardDrawn = HSCard(nameOfCard, idOfCard)
                    cardDrawn.ID = idOfCard
                    self.gamestate.addCardHand(cardDrawn, 1)
                    print("******************************")
                    print("to HAND:" + nameOfCard + "*** ID = " + idOfCard)
                    print("******************************")
                elif "to FRIENDLY DECK" in line:
                    cardToDeck = self.getCardByID(idOfCard)
                    newCard = HSCard(cardToDeck.getName(), idOfCard)
                    print(self.gamestate.Hand[1])
                    for i in range(3):
                        if cardToDeck in self.gamestate.Hand[1]:
                            print("Card got Removed: " + cardToDeck.getName())
                            self.gamestate.Hand[1].remove(cardToDeck)
                        print("CardRemoveLOOP***********")
                    print(self.gamestate.Hand[1])
                    for i in range(3): self.gamestate.destroyByID(idOfCard)
                    # self.gamestate.addCardDeck(newCard,1)
                    print("******************************")
                    print("to DECK:" + nameOfCard + "*** ID = " + idOfCard)
                    print("******************************")
                    self.printStatus()
                elif "from FRIENDLY HAND -> FRIENDLY DECK" in line and "UNKNOWN ENTITY" not in line:
                    cardtoDeck = self.getCardByID(idOfCard)
                    if cardtoDeck is None: continue
                    print("Card to Deck Transition: " + cardtoDeck.getName())
                    if cardtoDeck in self.gamestate.Hand[1]:
                        self.gamestate.Hand[1].remove(cardtoDeck)
                elif "pos from" in line and "UNKNOWN ENTITY" not in line and "-> 0" not in line:
                    indexID = line.find(" id=")
                    ID = self.getID(line[indexID + 2:])
                    card = self.getCardByID(ID)
                    if card != None:
                        index = line.find("pos from")
                        pos = line[index + 14:index + 16]
                        # print(nameOfCard + " is now in Position:" + str(int(pos)))  # Cast as Int do know if the Pos has two digits or one
                        card.Pos = pos
                        print("Pos Change from Card: " + str(card) + " ID: " + str(ID) + " to pos: " + str(pos))
                        # print("Line: " + line)
                        # print(card.Name)
                        # print(pos)
                elif "to FRIENDLY PLAY (Hero)" in line:
                    self.hero[1] = nameOfCard
                    self.gamestate.Class[1] = nameOfCard
                    self.heroID[1] = idOfCard
                    continue  # This continue is needed so that the other elif's don't trigger

                elif "to OPPOSING PLAY (Hero)" in line:
                    self.gamestate.Class[-1] = nameOfCard
                    self.hero[-1] = nameOfCard
                    self.heroID[-1] = idOfCard
                    continue  # This continue is needed so that the other elif's don't trigger

                elif "to FRIENDLY PLAY (Hero Power)" in line:
                    self.gamestate.HeroPower[1] = nameOfCard
                    continue  # This continue is needed so that the other elif's don't trigger
                elif "to OPPOSING PLAY (Hero Power)" in line:
                    self.gamestate.HeroPower[-1] = nameOfCard
                    continue  # This continue is needed so that the other elif's don't trigger

                # elif "to FRIENDLY PLAY" in line:
                #     print("a")
                #     if "(Weapon)" in line:
                #         move = Move("playweapon", actioncard=self.CheckCard(self.getCardByID(idOfCard)))
                #         HearthSimulation.simTurn(self.gamestate, move)
                #         # print("Played Weapon: " + str(nameOfCard) + "*** ID = " + idOfCard)
                #     else:
                #         if not self.getCardByID(idOfCard) is None:
                #             move = Move("play", actioncard=self.CheckCard(self.getCardByID(idOfCard)))
                #             HearthSimulation.simTurn(self.gamestate, move)

                elif "to OPPOSING PLAY" in line:
                    cardPlayed = HSCard(nameOfCard, idOfCard)
                    cardPlayed.ID = idOfCard
                    if "(Weapon)" in line:
                        move = Move("playweapon", actioncard=self.CheckCard(cardPlayed))
                        print("_______________")
                        print(125)
                        print(move)
                        print(self.gamestate.ActivePlayer)
                        print("______________----------------_______________________")
                        HearthSimulation.simTurn(self.gamestate, move)
                        print("Enemy played Weapon: " + str(self.getName(line)))
                    else:
                        if cardPlayed.getName() is "Silver Hand Recruit": continue
                        move = Move("play", self.CheckCard(card=cardPlayed))
                        print("_______________")
                        print(134)
                        print(move)
                        print(self.gamestate.ActivePlayer)
                        print("______________----------------_______________________")
                        HearthSimulation.simTurn(self.gamestate, move)
                        print("to ENEMY BOARD:" + nameOfCard + "*** ID = " + idOfCard)

                elif "START waiting for zone OPPOSING DECK" in line and self.gamestate.ActivePlayer == 1:
                    if self.muliganInt > 1:
                        self.turnTransition(True)
                    else:
                        self.muliganInt += 1

                elif "START waiting for zone FRIENDLY DECK" in line and self.gamestate.ActivePlayer == -1:
                    if self.muliganInt > 1:
                        self.turnTransition(False)
                    else:
                        self.muliganInt += 1

                elif "BLOCK_START BlockType=ATTACK" in line:
                    s = line.split("Target=")
                    attacker = self.getName(s[0])
                    defender = self.getName(s[1])
                    idOfAttacker = self.getID(s[0])
                    idOfDefender = self.getID(s[1])
                    move = Move("attack", actioncard=self.CheckCard(self.getCardByID(idOfAttacker)),
                                targetcard=self.CheckCard(self.getCardByID(idOfDefender)))
                    result = attacker + "*ID=" + idOfAttacker + "*" + " has attacked : " + defender + "*ID=" + idOfDefender + "*"
                    if self.lastFromPowerLog != result:
                        print(result)
                        if (not move.actioncard == None) and (not move.target == None):
                            print("_______________")
                            print(166)
                            print(move)
                            print(self.gamestate.ActivePlayer)
                            print("______________----------------_______________________")
                            HearthSimulation.simTurn(self.gamestate, move)
                        self.lastFromPowerLog = result

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
                                            targetcard=self.CheckCard(self.getCardByID(idofTarget)))
                            elif SpellCard.getType() is "MINION":
                                move = Move("playtargetedminion", actioncard=self.CheckCard(SpellCard),
                                            targetcard=self.CheckCard(self.getCardByID(idofTarget)))
                            result = spell + " has been played with target : " + target
                            if self.lastFromPowerLog != result:
                                print("_______________")
                                print(190)
                                print(move)
                                print(self.gamestate.ActivePlayer)
                                print("______________----------------_______________________")
                                HearthSimulation.simTurn(self.gamestate, move)
                                self.lastFromPowerLog = result
                        else:  # Spell has no Target
                            # print(self.gamestate.Hand)
                            # print("2")
                            s = line.split("Target=")
                            spell = self.getName(s[0])
                            idofSpell = self.getID(s[0])
                            SpellCard = self.getCardByID(idofSpell)
                            # print(self.gamestate.Hand)
                            if SpellCard != None:
                                if SpellCard.getType() is "SPELL":
                                    move = Move("playspell", actioncard=self.CheckCard(SpellCard))
                                elif SpellCard.getType() is "MINION":
                                    move = Move("play", actioncard=self.CheckCard(SpellCard))
                                result = spell + " has been played without target."

                                if self.lastFromPowerLog != result:
                                    # print(result)
                                    if self.gamestate.ActivePlayer is -1: continue
                                    print("_______________")
                                    print(215)
                                    print(move)
                                    print(self.gamestate.ActivePlayer)
                                    print("______________----------------_______________________")
                                    HearthSimulation.simTurn(self.gamestate, move)
                                    self.lastFromPowerLog = result
                                    # print(self.gamestate.Hand)

                elif "BLOCK_START BlockType=PLAY" in line:
                    if "<b>Hero Power</b>" in HSCard(self.getName(line), 0).getText():
                        if self.getName(line) == "Reinforce": continue
                        result = "Heropower has been played: " + self.getName(line)
                        if self.hero in ["Mage", "Priest"]:  # Targeted Heropower
                            s = line.split("Target=")
                            target = self.getName(s[1])
                            idofTarget = self.getID(s[1])
                            move = Move("heropower", targetcard=self.CheckCard(getCardByID(idofTarget)))
                            print("_______________")
                            print(232)
                            print(move)
                            print(self.gamestate.ActivePlayer)
                            print("______________----------------_______________________")
                            # HearthSimulation.simTurn(self.gamestate, move)
                        else:
                            move = Move("heropower")
                            print("_______________")
                            print(240)
                            print(move)
                            print(self.gamestate.ActivePlayer)
                            print("______________----------------_______________________")
                        if self.lastFromPowerLog != result:
                            HearthSimulation.simTurn(self.gamestate, move)
                            print(result)
                            self.lastFromPowerLog = result
                            line = file.readline()

                elif "Entity=GameEntity" in line and "value=FINAL_WRAPUP" in line:
                    print("End Of Game")
                    self.reset()

                elif "FULL_ENTITY - Updating" in line and "UNKNOWN ENTITY" not in line:
                    card = HSCard(self.getName(line), 0)

                    if card.getType() is not "HERO": continue  # For Cards like Heropowers or The Coin
                    # See which player this Entity belongs to
                    index = line.find("player=")
                    playerNum = line[
                                index + 7:index + 8]  # This is 1 if the Hero is friendly and 0 if the Hero is an Enemy
                    if playerNum == "1":
                        self.hero[1] = self.getName(line)
                        print("Friendly Hero: " + self.hero[1])
                    elif playerNum == "2":
                        self.hero[-1] = self.getName(line)
                        print("Enemy Hero: " + self.hero[-1])
                    else:
                        print("ERROR Hero could not be resolved. Index = '" + str(playerNum) + "'")

                if self.firstRotation:
                    start = input("Who started?: ")
                    self.firstRotation = False
                    print(start)
                    if str(start) == "-1":
                        self.gamestate.EnemyCardLen = 3
                        self.gamestate.EnemyDeckLen = 27
                        # self.gamestate.ManaCrystals[-1] += 1
                        # self.gamestate.EmptyManaCrystals[-1] += 1
                        self.gamestate.ActivePLayer = -1
                    if str(start) == "1":
                        self.gamestate.EnemyCardLen = 5
                        self.gamestate.EnemyDeckLen = 26
                        self.gamestate.ManaCrystals[1] += 1
                        self.gamestate.EmptyManaCrystals[1] += 1
                        self.gamestate.ActivePLayer = 1
                        # print(self.gamestate.Hand)
                        # for card in self.gamestate.Hand[1]:
                        #    print(card.ID)

    def turnTransition(self, bool):

        print(self.gamestate.ManaCrystals)
        print(self.gamestate.EmptyManaCrystals)
        print(self.gamestate.ActivePlayer)
        print("_______________")
        print("______________----------------_______________________")
        move = Move("end")
        print(298)
        print(move)
        print(self.gamestate.ActivePlayer)
        HearthSimulation.simTurn(self.gamestate, move)
        print(self.gamestate.ManaCrystals)
        print(self.gamestate.EmptyManaCrystals)
        print(self.gamestate.ActivePlayer)
        if bool:
            if not self.gamestate.ActivePlayer == 1:
                self.endOfTurn()
                self.printStatus()
        else:
            if self.gamestate.ActivePlayer == 1:
                self.endOfTurn()
                self.printStatus()

    def getPlayer(self, line):
        pass
        # todo

    def getID(self, line):
        indexID = line.find(" id=")
        indexEndOfID = line.find("zone=")
        ID = line[indexID + 4:indexEndOfID - 1]
        return ID

    def CheckCard(self, card):
        if card is None: return card
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

    def endOfTurn(self):
        self.counterDict = {}
        self.cardsPlayedThisTurn = []
        self.minionsDiedThisTurn = []
        self.minionsThatAttackedThisTurn = []
        self.numOfAttacksThisTurn = []
        self.spellsPlayedThisTurn = []
        print("End Of Turn")

    def getName(self, line):
        indexName = line.find("entityName=")
        indexEndOfName = line.find("id=")
        name = line[indexName + 11:indexEndOfName - 1]
        return name

    def getTarget(self, line):
        pass

    def printStatus(self):
        print("*********STATUS***********")
        print("Cards in Hand:" + str([card.getName() for card in self.gamestate.Hand[1] if card is not None]))
        print("Pos of Cards in Hand:" + str([card.Pos for card in self.gamestate.Hand[1] if card is not None]))
        print("Cards on Board" + str([card.getName() for card in self.gamestate.Board[1] if card is not None]))
        print("Pos of Cards on Board" + str([card.Pos for card in self.gamestate.Board[1] if card is not None]))
        print("Cards on EnemyBoard" + str([card.getName() for card in self.gamestate.Board[-1] if card is not None]))

    def update(self):
        while True:
            time.sleep(5)
            self.printStatus()

    def decodeDeckstring(self, deckstring, copiedToClipboard=False):
        deck = []
        hero = ""
        if copiedToClipboard: deckstring = pyperclip.paste()
        for line in deckstring.split("\n"):
            if "#" not in line:
                while (len(line) % 4 != 0): line += "="  # Base 64 padding
                deckstring = line
                break
        format = "Standart"
        cards, heroes, format = deckstrings.parse_deckstring(deckstring)
        for card in cards:
            for i in range(card[1]):
                print("hello")
                print(card[0])
                print(Card.cards.searchCardbyID(card[0]))
                name = Card.cards.searchCardbyID(card[0])["name"]
                deck.append(HSCard(name, 0))
        for card in deck: print(card.getName())
        hero = Card.cards.searchCardbyID(heroes[0])["playerClass"]
        filedecks = open("MyDeck.txt", "w")

        for card in deck:
            filedecks.write(card.Name + "\n")
        return deck, hero, format

    def reset(self):
        l = self.gamestate.EnemyCardLen
        e = self.gamestate.EnemyDeckLen
        self.gamestate.reset()
        self.gamestate.ManaCrystals = [0, 0, 0]
        self.gamestate.EmptyManaCrystals = [0, 0, 0]
        self.gamestate.EnemyCardLen = l
        self.gamestate.EnemyDeckLen = e
        if l == 3:
            # self.gamestate.ManaCrystals[-1]+=1
            # self.gamestate.EmptyManaCrystals[-1] += 1
            self.gamestate.ActivePLayer = -1
        else:
            self.gamestate.ManaCrystals[1] += 1
            self.gamestate.EmptyManaCrystals[1] += 1
            self.gamestate.ActivePLayer = 1
        self.handcards = []
        self.boardcards = []
        self.enemycards = []

    def removeCardFromHand(self, ID, player):
        for card in self.gamestate.Hand[player]:
            if card.ID == ID: self.gamestate.destroy(card)

    def removeCardFromDeck(self, ID, player):
        for card in self.gamestate.Deck[player]:
            if card.ID == ID: self.gamestate.destroy(card)

    def removeCardFromBoard(self, ID, player):
        for card in self.gamestate.Board[player]:
            if card.ID == ID: self.gamestate.destroy(card)

    def removeCardFromGraveyard(self, ID, player):
        for card in self.gamestate.Graveyard[player]:
            if card.ID == ID: self.gamestate.destroy(card)

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