import HSCard
import Move
import random
import copy
import Card
IDNR = 250
#list of todo
# todo test all Heropowers

def listoflegalmoves(gamestate):


    #todo spells and other stupid shit
    #todo this was list of legal moves form the simplified version
    #todo adjust for new move types
    listoflegalmoves = []

    #if gamestate.Weapon[gamestate.ActivePlayer] != None:
    #    card = gamestate.Weapon[gamestate.ActivePlayer]
    #    for enemycard in gamestate.Board[gamestate.ActivePlayer * -1]:
    #        listoflegalmoves.append(Move.Move("attack", card, enemycard))
    #    listoflegalmoves.append(Move.Move("attack", card, gamestate.ActivePlayer * -1))

    for card in gamestate.Hand[gamestate.ActivePlayer]:
        if card.Type == "MINION":
            if card.Cost <= gamestate.ManaCrystals[gamestate.ActivePlayer]:
                listoflegalmoves.append(Move.Move("play", card))
                #todo play with target,singletargetspell etc.
        #if card.Type == "SPELL":
        #    #todo wrong check if needs target first
        #    if card.Cost <= gamestate.ManaCrystals[gamestate.ActivePlayer]:
        #        listoflegalmoves.append(Move.Move("playspell",card))

    if gamestate.ManaCrystals[gamestate.ActivePlayer]>=2:
        if gamestate.HeroPower != "Death's Shadow":
            if gamestate.HeroPowerUsed == False:
                if gamestate.HeroPower in ["Fireblast","Lesser Heal"]:
                    for card in gamestate.Board[:]:
                        listoflegalmoves.append(Move.Move("heropower",card))
                    #listoflegalmoves.append(Move.Move("heropower"),1)
                    #listoflegalmoves.append(Move.Move("heropower"),-1)

                else:
                    #pass
                    listoflegalmoves.append(Move.Move("heropower"))
        #todo Deaths Shadow in end turn
    tauntcards = []
    for enemycard in gamestate.Board[gamestate.ActivePlayer * -1]:
        if "TAUNT" in enemycard.Mechanics:
            tauntcards.append(enemycard)
    if tauntcards == []:
        tauntcards = gamestate.Board[gamestate.ActivePlayer * -1]
    for card in gamestate.Board[gamestate.ActivePlayer]:
        if card.canAttack == True and card.Attack > 0:
            for enemycard in tauntcards:
                listoflegalmoves.append(Move.Move("attack",card,enemycard))
                # enemychampion
            if len(tauntcards) is not 0: listoflegalmoves.append(Move.Move("attack",card,gamestate.ActivePlayer*-1))

    listoflegalmoves.append(Move.Move("end"))
    return listoflegalmoves

def checkEndGame(gamestate):
    if gamestate.Health[1] <= 0:
        return 1
    if gamestate.Health[-1] <= 0:
        return -1
    return 0

def checkIfRunning(gamestate):
    if gamestate.Health[1] <= 0:
        return False
    if gamestate.Health[-1] <= 0:
        return False
    return True


def simTurn(gamestate,move):

    movecards = move

    if move.type == "end":
        if gamestate.EmptyManaCrystals[gamestate.ActivePlayer] < 10:
            gamestate.EmptyManaCrystals[gamestate.ActivePlayer] += 1
        for i in [0,1,2]:
            gamestate.ManaCrystals[i] = gamestate.EmptyManaCrystals[i]
        gamestate.draw(gamestate.ActivePlayer)
        if gamestate.ActivePlayer == -1:
            gamestate.EnemyDeckLen -= 1
            gamestate.EnemyCardLen += 1
        for card in gamestate.Board[gamestate.ActivePlayer]:
            card.canAttack = True
        for card in gamestate.Board[gamestate.ActivePlayer * -1]:
            card.canAttack = True
        gamestate.HeroPowerUsed = False
        gamestate.ActivePlayer *= -1
    elif move.type == "play":
        gamestate.ManaCrystals[gamestate.ActivePlayer] -= movecards.actioncard.Cost
        if len(gamestate.Board[gamestate.ActivePlayer]) < 7:
            gamestate.Board[gamestate.ActivePlayer].append(movecards.actioncard)
            if gamestate.ActivePlayer == -1:
                gamestate.SeenEnemyCards.append(movecards.actioncard.Name)
                gamestate.EnemyCardLen -= 1

            for p in [0, 1, 2]:
                for card in gamestate.Board[p]:
                    if card.ID == movecards.actioncard.ID:
                        card.canAttack = False
            movecards.actioncard.canAttack = False

        for p in [0, 1, 2]:
            for card in gamestate.Hand[p]:
                if card.ID == movecards.actioncard.ID:
                    gamestate.Hand[p].remove(card)

        triggerBattelcry(movecards.actioncard, gamestate, gamestate.ActivePlayer, Target=None)
    #elif move.type == "heroattack":
    #    #todo hero with attackvalue attacks
    #    pass
    #elif move.type == "playspell":
    #    playSpell(movecards.actioncard,gamestate,gamestate.ActivePlayer)
    #elif move.type == "singletargetspell":
    #    singleTargetSpell(movecards.actioncard, gamestate, gamestate.ActivePlayer)
    #elif move.type == "playchoose":
    #    #do we need this?
    #    playChoose(movecards.actioncard, gamestate, gamestate.ActivePlayer)
    elif move.type == "heropower":
        if move.actioncard != None:
            HeroPower(gamestate, gamestate.ActivePlayer, move.actioncard)
        else:
            HeroPower(gamestate,gamestate.ActivePlayer)
        gamestate.HeroPowerUsed = True
        gamestate.ManaCrystals[gamestate.ActivePlayer]-=2
        gamestate.HeroPowerUsed = False
    #elif move.type == "choose":
    #    #choose needs to be single move
    #    #moves like playchoose are bad, because they need input after the command play is given
    #    #We probably dont need playchoose
    #    Choose(movecards.actioncard, gamestate, gamestate.ActivePlayer)
    #elif move.type == "playchoosetarget":
    #    playChooseTarget(movecards.actioncard, gamestate, gamestate.ActivePlayer)
    #todo hero attack doesnt work yet
    elif move.type == "attack":
        if movecards.target == 1 or movecards.target == -1:
            gamestate.adjHealth(movecards.actioncard.Attack*-1,movecards.target)
        else:
            #remove cards with health under 0
            if movecards.actioncard.Health - movecards.target.Attack <= 0:
                for p in [0,1,2]:
                    for card in gamestate.Board[p]:
                        if card.ID == movecards.actioncard.ID:
                            gamestate.Board[p].remove(card)
                    #if movecards.actioncard in gamestate.Board[p]:
                    #    gamestate.Board[p].remove(movecards.actioncard)


            if movecards.target.Health - movecards.actioncard.Attack <= 0:
                for p in [0,1,2]:
                    for card in gamestate.Board[p]:
                        if card.ID == movecards.target.ID:
                            gamestate.Board[p].remove(card)


            movecards.actioncard.Health -= movecards.target.Attack
            movecards.target.Health -= movecards.actioncard.Attack
        for p in [0, 1, 2]:
            for card in gamestate.Board[p]:
                if card.ID == movecards.actioncard.ID:
                    card.canAttack = False
        movecards.actioncard.canAttack = False



def simGame(gamestatestart):
    gamestate = gamestatestart.clone()
    rounds = 0
    #print("in simgame")
    while checkIfRunning(gamestate) == True and not (
            gamestate.Board == [[], [], []] and gamestate.Hand == [[], [], []]):
        # print(gamestate.Health)
        # print(gamestate.Hand)
        # print(gamestate.Board)

        legalMove = random.choice(listoflegalmoves(gamestate))
        #print("picked a legalmove")
        #print(gamestate.Health)
        #print(legalMove)
        # print(legalMove)

        simTurn(gamestate, legalMove)
        if legalMove.type == "end":
            rounds += 1
        # print(checkEndGame(gamestate))
        # print(gamestate.Health)
    #print("SIMGAMESIMGAMMESIMGAME")
    #print(checkEndGame(gamestate))
    Health = gamestate.Health[checkEndGame(gamestate)*-1]
    Boardstatme = 1
    Boardstatu = 1
    for card in gamestate.Board[checkEndGame(gamestate)]:
        Boardstatme+=card.Health
        Boardstatme += card.Attack
    for card in gamestate.Board[checkEndGame(gamestate)*-1]:
        Boardstatu+=card.Health
        Boardstatu += card.Attack
    if Boardstatu == 0:
        Boardstatu = 1
    HandCards = len(gamestate.Hand[checkEndGame(gamestate)])
    return checkEndGame(gamestate), rounds, Health, Boardstatme/Boardstatu, HandCards
    gamestateone = gamestatestart.deepcopystate()

    wins = [0,0,0]
    for i in range(25):
        gamestate = gamestateone.deepcopystate()
        rounds = 0
        while checkIfRunning(gamestate) == True and not (gamestate.Board == [[], [], []] and gamestate.Hand == [[], [], []]):

            #print(gamestate.Board)
            #print(gamestate.Deck)
            #print(gamestate.Hand)
            legallist = listoflegalmoves(gamestate)
            #if len(legallist)>1:
            #    legallist = legallist[:-1]
            legalMove = random.choice(legallist)
            #print(legalMove)
            #print(gamestate.Health)
            simTurn(gamestate, legalMove)
            rounds += 1
            wins[checkEndGame(gamestate)] += 1
    if wins[1] > wins[-1]:
        return 1, rounds
    else:
        return -1, rounds

def checkEndGame(gamestate):
    if gamestate.Health[1] <= 0:
        return 1
    if gamestate.Health[-1] <= 0:
        return -1
    return 0

def checkIfRunning(gamestate):
    if gamestate.Health[1] <= 0:
        return False
    if gamestate.Health[-1] <= 0:
        return False
    return True
def replaceCard( card1, card2, pos, player):
    #todo
        pass
def addToxin( player):
    #todo
        pass
def Adapt( card):
    #todo
        pass
def Discover( TypeString, player):
    #todo
        pass
# return card,cost
# triggerefffects
# http://hearthstone.gamepedia.com/Triggered_effect
def triggerAtPlay(self):
    #todo
        pass
def triggerAtTurnEnd( player):
    #todo
        pass
def triggerAtTurnStart( player):
    #todo
        pass
def moveToGraveyard( player, card):
    #todo
        pass
def die( card, player):
    #todo
        pass
def moveToDeck( card, player):
    #todo
        pass
def draw( player):
    #todo
        pass
def newTurn( player):
    #todo
        pass
def play( card):
    #todo
        pass
def attack( attacker, atPos, target, tarPos):
    #todo
        pass
def posCards(self):
    #todo
        pass
def posAttacks(self):
    #todo
    pass
def playRandomCard(self):
    #todo
    pass
def playRandomAttack(self):
    #todo
    pass


def playSpell(card,gamestate,player):
    name = card.getName()
    # DRUID CARDS
    if "Innervate" == name:
        pass
    elif "Jungle Giants" == name:
        #todo
        pass
    elif "Claw" == name:
        gamestate.HeroAttack[player] += 2
        gamestate.HeroArmor[player] += 2
    elif "Jade Idol" == name:
        #todo
        pass
    elif "Mark of the Lotus" == name:
        for card in gamestate.Board[player]:
            card.adjHealth(1)
            card.adjAttack(1)
    elif "Power of the Wild" == name:
        #todo
        pass
    elif "Wild Growth" == name:
        if gamestate.ManaCrystals[player] == 10: gamestate.addCardHand(HSCard.HSCard("Excess Mana"))
        else: gamestate.ManaCrystals[player] += 1
    elif "Gnash" == name:
        gamestate.HeroAttack[player] += 3
        gamestate.HeroArmor[player] += 3
    elif "Jade Blossom" == name:
        gamestate.summonJade()
        if gamestate.ManaCrystals[player] == 10: gamestate.addCardHand(HSCard.HSCard("Excess Mana"))
        else: gamestate.ManaCrystals[player] += 1
    elif "Pilfered Power" == name:
        if gamestate.ManaCrystals[player] == 10: gamestate.addCardHand(HSCard.HSCard("Excess Mana"))
        else: gamestate.ManaCrystals[player] += len(gamestate.board[player])
    elif "Savage Roar" == name:
        #todo
        pass
    elif "Astral Communion" == name:
        while(len(gamestate.Board[player]) > 0): gamestate.discardRandom(player)
        if gamestate.ManaCrystals[player] == 10: gamestate.addCardHand(HSCard.HSCard("Excess Mana"))
        else: gamestate.ManaCrystals[player] == 10
    elif "Bite" == name:
        gamestate.HeroAttack[player] += 4
        gamestate.HeroArmor[player] += 4
    elif "Evolving Spores" == name:
        for card in gamestate.Board[player]:
            card.Adapt()
    elif "Oaken Summons" == name:
        gamestate.HeroArmor[player] += 6
        gamestate.Recruit(Mana = [4,3,2,1,0])
    elif "Poison Seeds" == name:
        EnemyBoardLen = len(gamestate.Board[-1])
        FriendlyBoardLen = len(gamestate.Board[1])
        for card in gamestate.Board[-1]:
            gamestate.destroy(card)
        for card in gamestate.Board[1]:
            gamestate.destroy(card)
        for i in range(EnemyBoardLen):
            gamestate.addCardBoard(HSCard.HSCard("Treant"), -1)
        for i in range(FriendlyBoardLen):
            gamestate.addCardBoard(HSCard.HSCard("Treant"), 1)
    elif "Soul of the Forest" == name:
        for card in gamestate.Board[player]:
            card.AddedDeathrattles.append("Summon a 2/2 Treant")
    elif "Force of Nature" == name:
        for i in range(3):
            gamestate.summon(HSCard.HSCard("Treant"), player)
    elif "Living Mana" == name:
        spaceOnBoard = 7 - len(gamestate.Board[player])
        for i in range(spaceOnBoard):
            if gamestate.ManaCrystals[player] == 0: break
            gamestate.ManaCrystals[player] -= 1
            gamestate.summon(HSCard.HScard("Mana Treant"))
    elif "Lunar Visions" == name:
        gamestate.draw(player)
        gamestate.draw(player)
        for card in [gamestate.Hand[player][-1], gamestate.Hand[player][-2]]:
            if card.getType() == "MINION":
                card.cost -= 2
    elif "Webweave" == name:
        for i in range(2):
            gamestate.summon(HSCard.HSCard("Frost Widow"))
    elif "Spreading Plague" == name:
        while(len(gamestate.Board[player]) < len(gamestate.Board[player*-1])):
            gamestate.summon(HSCard.HSCard("Scarab Beetle"), player)
    elif "Tree of Life" == name:
        #todo
        pass
    #HUNTER SPELLS
    elif "Animal Companion" == name:
        beasts = [HSCard.HSCard("Misha"), HSCard.HSCard("Huffer"), HSCard.HSCard("Leokk")]
        gamestate.summon(random.choice(beasts), player)
    elif "Multi-Shot" == name:
        target1 = random.choice(gamestate.board[player*-1])
        target2 = random.choice(gamestate.board[player*-1])
        while(target1 == target2): target2 = random.choice(gamestate.board[player])
        target1.adjHealth(-3)
        target2.adjHealth(-3)
    elif "Deadly Shot" == name:
        gamestate.destroy(random.choice(gamestate.board[player*-1]))
    elif "Smuggler's Crate" == name:
        beastInHand = []
        for card in gamestate.Hand[player]:
            if card.race == "Beast":
                beastInHand.append(card)
        if beastInHand == []: return
        selectedCard = random.choice(beastInHand)
        selectedCard.adjHealth(2)
        selectedCard.adjHealth(2)
    elif "Unleash the Hounds" == name:
        while(len(gamestate.Board[player]) < len(gamestate.Board[player*-1])):
            gamestate.summon(HSCard.HSCard("Hound"), player)
    elif "Lesser Emerald Spellstone" == name:
        for i in range(2):
            gamestate.summon(HSCard.HSCard("Wolf"),player)
    elif "Emerald Spellstone" == name:
        for i in range(3):
            gamestate.summon(HSCard.HSCard("Wolf"),player)
    elif "Greater Emerald Spellstone" == name:
        for i in range(4):
            gamestate.summon(HSCard.HSCard("Wolf"),player)
    elif "Flare" == name:
        #todo
        pass
    elif "Infest" == name:
        for card in gamestate.Board[player]:
            card.AddedDeathrattles.append("Add a random Beast to your hand")
    elif "Call of the Wild" == name:
        gamestate.summon(HSCard.HSCard("Huffer"),player)
        gamestate.summon(HSCard.HSCard("Leokk"),player)
        gamestate.summon(HSCard.HSCard("Misha"),player)
    elif "Crushing Walls" == name:
        gamestate.destroy(gamestate.Board[player*-1][0])
        gamestate.destroy(gamestate.Board[player*-1][-1])
    elif "Dinomancy" == name:
        #todo
        pass
    elif "Stampede" == name:
        #todo
        pass
    elif "To My Side!" == name:
        beasts = [HSCard.HSCard("Misha"), HSCard.HSCard("Huffer"), HSCard.HSCard("Leokk")]
        toBeSummoned = random.choice(beasts)
        gamestate.summon(toBeSummoned, player)
        MinionInDeck = False
        for card in gamestate.Deck[player]:
            if card.getType() == "MINION":
                MinionInDeck = True
                break
        if not MinionInDeck:
            toBeSummoned2 = random.choice(beasts)
            while toBeSummoned == toBeSummoned2: toBeSummoned2 = random.choice(beasts)
            gamestate.summon(toBeSummoned2, player)
    # MAGE SPELLS
    elif "Arcane Explosion" == name:
        for card in gamestate.Board[player*-1]:
            card.adjHealth(-1)
    elif "Arcane Intellect" == name:
        gamestate.draw(player)
        gamestate.draw(player)
    elif "Arcane Missiles" == name:
        for i in range(3):
            possibleTargets = []
            possibleTargets.append("Hero")
            possibleTargets.extend(gamestate.Board[player*-1])
            target = random.choice(possibleTargets)
            if target == "Hero": gamestate.Health[player*-1] -= 1
            else: target.adjHealth(-1)
    elif "Flamestrike" == name:
        for card in gamestate.Board[player*-1]:
            card.adjHealth(-4)
    elif "Frost Nova" == name:
        for card in gamestate.Board[player*-1]:
            card.Effect.append("Frozen")
    elif "Mirror Image" == name:
        gamestate.summon(HSCard.HSCard("Mirror Image"), player)
        gamestate.summon(HSCard.HSCard("Mirror Image"), player)
    elif "Breath of Sindragosa" == name:
        card = random.choice(gamestate.Board[player*-1])
        card.adjHealth(-2)
        card.Effect.append("Frozen")
    elif "Shifting Scroll" == name:
        #todo
        pass
    elif "Blizzard" == name:
        for card in gamestate.Board[player*-1]:
            card.adjHealth(-2)
            card.Effect.append("Frozen")
    elif "Lesser Ruby Spellstone" == name:
        #todo
        pass
    elif "Ruby Spellstone" == name:
        #todo
        pass
    elif "Greater Ruby Spellstone" == name:
        #todo
        pass
    elif "Volcanic Potion" == name:
        for card in gamestate.Board[player*-1]: card.adjHealth(-2)
        for card in gamestate.Board[player]: card.adjHealth(-2)
    elif "Cabalist's Tome" == name:
        #todo
        pass
    elif "Deck of Wonders" == name:
        for i in range(5):
            gamestate.addCardDeck(HSCard.HSCard("Scroll of Wonder"),player)
    elif "Dragon's Fury" == name:
        spellRevealed = random.choice(gamestate.Deck[player])
        while spellRevealed.getType() is not "SPELL": spellRevealed = random.choice(gamestate.Deck[player])
        if spellRevealed.getType() == "SPELL":
            for card in gamestate.Board[player*-1]: card.adjHealth(spellRevealed.getCost())
            for card in gamestate.Board[player]: card.adjHealth(spellRevealed.getCost())
    elif "Glacial Mysteries" == name:
        #todo
        pass
    elif "Greater Arcane Missiles" == name:
        for i in range(3):
            possibleTargets = []
            possibleTargets.append("Hero")
            possibleTargets.extend(gamestate.Board[player*-1])
            target = random.choice(possibleTargets)
            if target == "Hero": gamestate.Health[player*-1] -= 3
            else: target.adjHealth(-3)
    elif "Simulacrum" == name:
        #todo
        pass
    # PALADIN SPELLS
    elif "Consecration" == name:
        for card in gamestate.Board[player*-1]:
            card.adjHealth(-2)
        gamestate.Health[player*-1] -= 2
    elif "Lost in the Jungle" == name:
        gamestate.summon(HSCard.HSCard("Silver Hand Recruit"), player)
        gamestate.summon(HSCard.HSCard("Silver Hand Recruit"), player)
    elif "Smuggler's Run" == name:
        for card in gamestate.Hand[player]:
            if card.getType() == "MINION":
                card.adjHealth(1)
                card.adjAttack(1)
    elif "Stand Against Darkness" == name:
        for i in range(5):
            gamestate.summon(HSCard.HSCard("Silver Hand Recruit"), player)
    elif "Divine Favor" == name:
        #todo
        pass
    elif "Equality" == name:
        for card in gamestate.Board[player*-1]: card.setHealth(1)
        for card in gamestate.Board[player]: card.setHealth(1)
    elif "Lesser Pearl Spellstone" == name:
        #todo
        pass
    elif "Pearl Spellstone" == name:
        #todo
        pass
    elif "Greater Pearl Spellstone" == name:
        #todo
        pass
    elif "Avenging Wrath" == name:
        for i in range(8):
            possibleTargets = []
            possibleTargets.append("Hero")
            possibleTargets.extend(gamestate.Board[player*-1])
            target = random.choice(possibleTargets)
            if target == "Hero": gamestate.Health[player*-1] -= 1
            else: target.adjHealth(-1)
    elif "Level Up!" == name:
        for card in gamestate.Board[player]:
            if card.getName() == "Silver Hand Recruit":
                card.adjHealth(2)
                card.adjAttack(2)
                card.Mechanics.append("TAUNT")
    elif "Small-Time Recruits" == name:
        for card in gamestate.Deck[player]:
            if index == 3: return
            if card.getCost() == 1 and card.getType() == "MINION":
                gamestate.addCardHand(card, player)
                gamestate.remove(card)
                index += 1
    # PRIEST SPELLS
    elif "Holy Nova" == name:
        gamestate.HealHealth(player, 2)
        for card in gamestate.Board[player]:
            card.adjHealth(2)
        gamestate.Health[player*-1] -= 2
        for card in gamestate.Board[player*-1]:
            card.adjHealth(-2)
    elif "Mind Blast" == name:
        gamestate.Health[player*-1] -= 5
    elif "Mind Vision" == name:
        gamestate.addCardHand(random.choice(gamestate.Hand[player*-1]),player)
    elif "Circle of Healing" == name:
        for card in gamestate.Board[player*-1]: card.adjHealth(4)
        for card in gamestate.Board[player]: card.adjHealth(4)
    elif "Psionic Probe" == name:
        for card in gamestate.Deck[player*-1]:
            if card.getType() == "SPELL":
                gamestate.addCardHand(card, player)
                return
    elif "Spirit Lash" == name:
        lifesteal = len(gamestate.Board[player*-1]) + len(gamestate.Board[player])
        gamestate.Health += lifesteal
        for card in gamestate.Board[player*-1]: card.adjHealth(1)
        for card in gamestate.Board[player]: card.adjHealth(1)
    elif "Thoughtsteal" == name:
        index = 0
        for card in gamestate.Deck[player*-1]:
                if index == 2: return
                gamestate.addCardHand(card, player)
                index += 1
    elif "Devour Mind" == name:
        index = 0
        for card in gamestate.Deck[player*-1]:
                if index == 3: return
                gamestate.addCardHand(card, player)
                index += 1
    elif "Lesser Diamond Spellstone" == name:
        #todo
        pass
    elif "Diamond Spellstone" == name:
        #todo
        pass
    elif "Greater Diamond Spellstone" == name:
        #todo
        pass
    elif "Mass Dispel" == name:
        for card in gamestate.Board[player*-1]:
            card.silence()
        gamestate.draw(player)
    elif "Pint-Size Potion" == name:
        #todo
        pass
    elif "Shadow Essence" == name:
        #todo
        pass
    elif "Shadow Word: Horror" == name:
        for card in gamestate.Board[player]:
            if card.Stats[1] <= 2:
                gamestate.destroy(card)
        for card in gamestate.Board[player*-1]:
            if card.Stats[1] <= 2:
                gamestate.destroy(card)
    elif "Twilight's Call" == name:
        #todo
        pass
    elif "Dragonfire Potion" == name:
        for card in gamestate.Board[player]:
            if card.getRace() is not "DRAGON":
                card.adjHealth(-5)
        for card in gamestate.Board[player*-1]:
            if card.getRace() is not "DRAGON":
                card.adjHealth(-5)
    elif "Embrace the Shadow" == name:
        #todo
        pass
    elif "Forbidden Shaping" == name:
        #todo
        pass
    elif "Mindgames" == name:
        for card in gamestate.Deck[player*-1]:
            if card.getType() == "MINION":
                gamestate.summon(card, player)
                return
    elif "Psychic Scream" == name:
        for card in gamestate.Board[player]:
            gamestate.Deck[player*-1].append(card)
            gamestate.Board[player].remove(card)
        for card in gamestate.Board[player*-1]:
            gamestate.Deck[player*-1].append(card)
            gamestate.Board[player*-1].remove(card)
    elif "Shadowform" == name:
        #todo
        pass
    # ROGUE SPELLS

def singleTargetSpell(card,gamestate,player):
    #todo
    pass

def Choose(card,gamestate,player):
    #todo
    pass

def playChooseTarget(card,gamestate,player):
    #todo
    pass

def Draweffect(card,gamestate,player):
    #todo
    pass

def Discardeffect(card,gamestate,player):
    #todo
    pass

def Triggeredeffect(card,gamestate,player):
    #todo
    pass

def Draweffect(card,gamestate,player):
    #todo
    pass

def Draweffect(card,gamestate,player):
    #todo
    pass

def Startturneffects(card,gamestate,player):
    #todo
    pass


def Inhandeffect(card,gamestate,player):
    IDNR = 250
    #Effects that happen constantly
    if card.Name == "Dread Corsair":
        if gamestate.Weapon[player] != None:
            card.cost = card.OriginalCost-gamestate.Weapon[player].Attack
            if card.cost < 0:
                card.cost = 0


    if card.Name == "Crystal Lion":
        count = 0
        for card in gamestate.Board[player]:
            if card.Name == "Silver Hand Recruit":
                count += 1
        card.cost = card.OriginalCost-count
        if card.cost < 0:
            card.cost = 0

    if card.Name == "Kabal Crystal Runner":
        card.cost = card.OriginalCost-gamestate.Numberofsecretsplayed[player]
        if card.cost < 0:
            card.cost = 0

    if card.FirstName == "Molten Blade":
        randomcard = random.choice(Card.cards.getListofAllWeapons)
        newcard = HSCard.HSCard(randomcard)
        newcard.FirstName="Molten Blade"
        card = newcard

    if card.Name == "Obsidian Shard":
        card.cost = card.OriginalCost-gamestate.Numberofotherclasscardsplayed[player]
        if card.cost < 0:
            card.cost = 0
    if card.Name == "Second-Rate Bruiser":
        if gamestate.Board[player*-1]>=3:
            card.cost = 3
        else:
            card.cost = 5
    if card.Name == "Thing from Below":
        card.cost = card.OriginalCost-gamestate.Numberoftotemsplayed

    if card.Name == "Arcane Giant":
        card.cost = card.OriginalCost-gamestate.Numberofspellsplayed
    if card.Name == "Arcane Tyrant":
        if gamestate.Numberofspellsthisturnmorefivecost[player]>0:
            card.Cost = 0
        else:
            card.cost = 5

    if card.Name == "Molten Giant":
        card.cost = card.OriginalCost-(gamestate.MaxHealth[player]-gamestate.Health[player])
    if card.Name == "Mountain Giant":
        card.cost = card.originalCost-len(gamestate.Board[player])
    if card.Name == "Sea Giant":
        card.cost = card.OriginalCost-len(gamestate.Hand[player])
    if card.Name == "Snowfury Giant":
        card.cost = card.OriginalCost-gamestate.Numberofoverloadedmanacrystals
    if card.Name == "Shifter Zerus":
        randomcard = random.choice(Card.cards.getListofAllMinions)
        newcard = HSCard.HSCard(randomcard)
        newcard.FirstName = "Molten Blade"
        card = newcard

def HeroPower(gamestate,player,target = None):
    IDNR = 500
    if gamestate.HeroPower[player] == "Shapeshift":
        gamestate.HeroAttack[player] += 1
        gamestate.HeroArmor[player] += 1
    elif gamestate.HeroPower[player] == "Steady Shot":
        gamestate.adjHealth(-2,player)
    elif gamestate.HeroPower[player] == "Fireblast":
        if target in [1,-1]:
            gamestate.adjHealth(-1,player)
        else:
            if target is not None: target.Health -= 1
    elif gamestate.HeroPower[player] == "Reinforce":
        if len(gamestate.Board[player]) <7:
            gamestate.Board[player].append(HSCard.HSCard("Silver Hand Recruit",IDNR))
            IDNR += 1
    elif gamestate.HeroPower[player] == "Lesser Heal":
        if target in [1,-1]:
            gamestate.adjHealth(2,player)
        else:
            target.Health+=2
    elif gamestate.HeroPower[player] == "Dagger Mastery":
        pass
        #gamestate.Weapon = (HSCard.HSCard("Wicked Knife"))
    elif gamestate.HeroPower[player] == "Totemic Call":
        i = random.randint(1,4)
        if i == 1:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Healing Totem"))
        elif i == 2:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Searing Totem"))
        elif i == 3:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Wrath of Air Totem"))
        elif i == 4:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Stoneclaw Totem"))
    elif gamestate.HeroPower[player] == "Life Tap":
        gamestate.draw(player)
        gamestate.adjHealth(2,player)
    elif gamestate.HeroPower[player] == "Armor Up":
        gamestate.Armor[player] += 2
    elif gamestate.HeroPower[player] == "Dirt Shapeshift":
        gamestate.HeroAttack[player] += 2
        gamestate.HeroArmor[player] += 2
    elif gamestate.HeroPower[player] == "Ballista Shot":
        gamestate.adjHealth(-3, player)
    elif gamestate.HeroPower[player] == "Fireblast Rank 2":
        if target in [1,-1]:
            gamestate.adjHealth(-2,player)
        else:
            target.Health-=2
    elif gamestate.HeroPower[player] == "The Silver Hand":
        if len(gamestate.Board[player]) <7:
            gamestate.Board[player].append(HSCard.HSCard("Silver Hand Recruit"))
        if len(gamestate.Board[player]) <7:
            gamestate.Board[player].append(HSCard.HSCard("Silver Hand Recruit"))
    elif gamestate.HeroPower[player] == "Heal":
        if target in [1,-1]:
            gamestate.adjHealth(4,player)
        else:
            target.Health+=4
    elif gamestate.HeroPower[player] == "Poisoned Daggers":
        gamestate.Weapon = (HSCard.HSCard("Poisoned Dagger"))
    elif gamestate.HeroPower[player] == "Totemic Slam":
        #random is an approximation change if rest finished
        i = random.randint(1, 4)
        if i == 1:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Healing Totem"))
        elif i == 2:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Searing Totem"))
        elif i == 3:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Wrath of Air Totem"))
        elif i == 4:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player].append(HSCard.HSCard("Stoneclaw Totem"))
    elif gamestate.HeroPower[player] == "Soul Tap":
        gamestate.draw(player)
    elif gamestate.HeroPower[player] == "Tank Up":
        gamestate.Armor[player] += 4
    elif gamestate.HeroPower[player] == "Plague Lord":
        i = random.randint(1,2)
        if i == 1:
            gamestate.HeroAttack += 3
        if i == 2:
            gamestate.Armor += 3
    elif gamestate.HeroPower[player] == "Build-A-Beast":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Dinomany":
        target.adjHealth(2)
        target.adjAttack(2)
    elif gamestate.HeroPower[player] == "Icy Touch":
        # todo
        pass
    elif gamestate.HeroPower[player] == "The Four Horsemen":
        # todo
        pass
    elif gamestate.HeroPower[player] == "The Tidal Hand":
        if len(gamestate.Board[player]) <7:
            gamestate.Board[player].append(HSCard.HSCard("Silver Hand Murloc"))
    elif gamestate.HeroPower[player] == "Voidform":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Mind Spike":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Mind Shatter":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Death's Shadow":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Transmite Spirit":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Lightning Jolt":
        # todo
        pass
    elif gamestate.HeroPower[player] == "Siphon Life":
        # todo
        pass
    elif gamestate.HeroPower[player] == "INFERNO!":
        if len(gamestate.Board[player]) <7:
            gamestate.Board[player].append(HSCard.HSCard("Infernal"))
    elif gamestate.HeroPower[player] == "Bladestrom":
        for card in gamestate.Board[:]:
            card.adjHealth(-1)
    elif gamestate.HeroPower[player] == "DIE, INSECT!":
        posenemy = []
        for en in gamestate.Board[player*-1]:
            posenemy.append(en)
        posenemy.append(player*-1)
        tar = random.choice(posenemy)
        if tar in [1,-1]:
            gamestate.adjHealth(-8,player)




def triggerBattelcry(card, gamestate,player, Target=None):
    battelText = ""
    #todo only uise cardnames
    if "Draw a card" in battelText:
        draw(player)

    if "Destroy your opponent's weapon" in battelText:
        gamestate.Weapon[player * -1] = ""

    if "Darkscale Healer" == card.getName():
        pass
        #gamestate.healHealth(2, player)
        #for card in gamestate.Board[player]:
        #    gamestate.healCardHealth(card, 2, player)

    if "Dragonling Mechanic" == card.getName():
        gamestate.summon(HSCard.HSCard("Mechanical Dragonling"))

    if "Dread Infernal" == card.getName():
        #gamestate.adjHealth(-1, player)
        #for card in gamestate.Board[player]:
        #    gamestate.adjCardHealth(card, -1, player)
        #gamestate.adjHealth(-1, player)
        #for card in gamestate.Board[player]:
        #    gamestate.adjCardHealth(card, -1, player)
        pass
    if "Deal" and "damage." in battelText and "Medivh's Valet" != card.getName:
    #todo
        pass

    if "Restore" and "Health." in battelText and "Hozen Healer" != card.getName():
        #todo
        pass

        #todo Fuck these methods later just every card alone

        if "Fire Elemental" == card.getName():
            gamestate.adjHealth(Target, -3, player)

    if "Frostwolf Warlord" == card.getName():
        ammount = len(gamestate.Board[player]) - 1
        #gamestate.adjCardHealth(card, ammount, player)
        #gamestate.adjCardAttack(card, ammount, player)
        pass
    if "Guardian of Kings" == card.getName():
        gamestate.adjHealth(6, player)

    if "Houndmaster" == card.getName():
    #todo
        pass

    if "Murloc Tidehunter" == card.getName():
        #gamestate.summon(HSCard.HSCard("Murloc Scout"))
        pass
    if "Nightblade" == card.getName():
        gamestate.adjHealth(-3, player * -1)

    if "Razorfen Hunter" == card.getName():
        #gamestate.summon(HSCard.HSCard("Boar"))
        pass
    if "Shattered Sun Cleric" == card.getName():
        #gamestate.adjCardHealth(Target, 1, player)
        #gamestate.adjCardAttack(Target, 1, player)
        pass
    if "Succubus" == card.getName():
        #gamestate.discardRandom(player)
        pass
    if "Windspeaker" == card.getName():
        if Target and "Windfury" not in Target.Mechanics: Target.Mechanics.append("Windfury")

    if "Abusive Sergeant" == card.getName():
    #todo
        pass

    if "Abyssal Enforcer" == card.getName():
        pass
        #for card in gamestate.board:
        #    gamestate.adjHealth(card, -3)
        #gamestate.adjHealth(1, -3)
        #gamestate.adjHealth(-1, -3)

    if "Alleycat" == card.getName():
        gamestate.summon(player, HSCard.HSCard("Tabbycat"))
        #todo
        pass

    if "Return a friendly minion from the battlefield to your hand." == battelText:
    #todo
        pass

    if "Arathi Weaponsmith" == card.getName():
        pass
        #gamestate.weapon[player] = HSCard("Battle Axe")

    if "Arcanologist" == card.getName():
        for card in gamestate.deck[player]:
            if card.type == "SPELL" and "SECRET" in card.mechanics:
                gamestate.addCardHand(player, HSCard.HSCard(card.name))
            gamestate.deck[player].remove(card)
            break

    if "Arcanosmith" == card.getName():
        gamestate.summon(player, HSCard.HSCard("Animated Shield"))

    if "Argent Protector" == card.getName():
        if Target and "DIVINE SHIELD" not in Target.mechanics:
            Target.mechanics.append("DIVINE SHIELD")

    if "Beckoner of Evil" == card.getName():
        gamestate.AdjCthunHealth(player, +2)
        gamestate.AdjCthunAttack(player, +2)

    if "Bilefin Tidehunter" == card.getName():
        #gamestate.summon(player, HSCard.HSCard("Ooze"))
        pass
    if "Bloodsail Raider" == card.getName():
        gamestate.adjWeapon(player * -1, 0, -1)

    if "C'Thun's Chosen" == card.getName():
        gamestate.AdjCthunHealth(player, +2)
        gamestate.AdjCthunAttack(player, +2)

    if "Crackling Razormaw" == card.getName():
        if Target: Target.adapt()

    if "Cruel Taskmaster" == card.getName():
        if Target:
            gamestate.adjCardHealth(Target, -1)
            gamestate.adjCardAttack(Target, +2)

    if "Cryomancer" == card.getName():
    #todo
        pass

    if "Crystalweaver" == card.getName():
        for card in gamestate.board[player]:
            if card.race == "DEMON":
                gamestate.adjCardAttack(card, +1)
                gamestate.adjCardHealth(card, +1)

    if "Cult Apothecary" == card.getName():
        pass
    #         count = 0
#        for card in gamestate.Board[player * -1]:
#            count += 1
#        gamestate.healHealth(player, count * 2)

    if "Dark Arakkoa" == card.getName():
        gamestate.AdjCthunHealth(player, +3)
        gamestate.AdjCthunAttack(player, +3)

    if "Dark Iron Dwarf" == card.getName():
    #todo
        pass

    if "Elder Longneck" == card.getName():
        minionInHand = False
        for card in gamestate.hand[player]:
            if card.Attack >= 5:
                minionInHand = True
                break
        if minionInHand:
            gamestate.board[player][card].adapt()

    if "Emerald Reaver" == card.getName():
        gamestate.adjHealth(-1, player)
        gamestate.adjHealth(-1, player * -1)

    if "Faceless Summoner" == card.getName():
    #todo
        pass

    if "Fire Fly" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Flame Elemental",666), player)

    if "Flame Imp" == card.getName():
        gamestate.adjHealth(-3, player)

    if "Frost Elemental" == card.getName():
        if Target and "FREEZE" not in Target.mechanics:
            Target.mechanics.append("FREEZE")

    if "Grimestreet Outfitter" == card.getName():
        for card in gamestate.Hand[player]:
            gamestate.adjCardAttack(card, +1)
            gamestate.adjCardHealth(card, +1)

    if "Grimestreet Smuggler" == card.getName():
        card = random.choice(gamestate.hand[player])
        gamestate.adjCardAttack(card, +1)
        gamestate.adjCardHealth(card, +1)

    if "Grimscale Chum" == card.getName():
        #murloclist = []
        #for card in gamestate.Hand[player]:
        #    if card.race == "MURLOC":
        #        murloclist.append(card)
        #card = random.choice(murloclist)
        #gamestate.adjCardAttack(card, +1)
        #gamestate.adjCardHealth(card, +1)
        pass
    if "Hozen Healer" == card.getName():
        if Target: gamestate.adjCardHealth(Target, Target.MaxHealth - Target.stats[0])

    if "Hydrologist" == card.getName():
    #todo
        pass

    if "Silence a Minion" in card.getText():
        if Target: gamestate.silence(target)

    if "Jade Chieftain" == card.getName():
    #todo
        pass

    if "Jeweled Macaw" == card.getName():
    #todo
        pass

    if "Kabal Chemist" == card.getName():
    #todo
        pass

    if "Kabal Lackey" == card.getName():
    #todo
        pass

    if "" == card.getName():
    #todo
        pass

    if "Silence a minion" in card.getText():
    #todo
        pass

    if "Kooky Chemist" == card.getName():
        if Target:
            temp = Target.getHealth()
            gamestate.setHealth(Target, Target.getAttack())
            gamestate.setAttack(Target, temp)

    if "Lakkari Felhound" == card.getName() or "Doomguard" == card.getName():
        gamestate.discardRandom(player)
        gamestate.discardRandom(player)

    # NEEDS TO ALSO HIT HEROES BUT TOO LAZY ATM
    if "Mad Bomber" == card.getName():
        for i in range(3):
            gamestate.adjCardHealth(random.choice(random.choice(gamestate.board)), -1)

    if "Medivh's Valet" == card.getName():
    #todo
        pass

    if "Menagerie Magician" == card.getName():
    #todo
        pass

    if "Menagerie Warden" == card.getName():
    #todo
        pass

    if "N'Zoth's First Mate" == card.getName():
        gamestate.weapon[player] = HSCard.HSCard("Rusty Hook")

    if "Naga Corsair" == card.getName():
        pass
        #if gamestate.weapon[player] is not None:
        #    gamestate.adjWeapon(player, +1, 0)

    if "Nesting Roc" == card.getName():
        if gamestate.board[player].length >= 2:
            card.mechanics.append("TAUNT")

    if "Netherspite Historian" == card.getName():
    #todo
        pass

    if "Nightbane Templar" == card.getName():
        dragonInHand = False
        for card in gamestate.hand[player]:
            if card.race == "DRAGON":
                dragonInHand = True
                break
        if dragonInHand:
            gamestate.summon(player, HSCard.HSCard("Whelp"))
            gamestate.summon(player, HSCard.HSCard("Whelp"))

    if "Ornery Direhorn" == card.getName():
        card.adapt()

    if "Pantry Spider" == card.getName():
        gamestate.summon(player, HSCard.HSCard("Cellar Spider"))

    if "Priestess of Elune" == card.getName():
        gamestate.healHealth(player, +4)

    if "Primalfin Lookout" == card.getName():
        murlocOnBoard = False
        for card in gamestate.board[player]:
            if card.race=="MURLOC":
                murlocOnBoard = True
                break
        if murlocOnBoard:
            #todo
            pass
        pass
    if "Pterrordax Hatchling" == card.getName():
        card.adapt()

    if "Ravaging Ghoul" == card.getName():
        for card in gamestate.board[:]:
            gamestate.adjCardHealth(card, -1)

    if "Ravasaur Runt" == card.getName():
        if gamestate.board[player].length >= 2:
            card.adapt()

    if "Ravenous Pterrordax" == card.getName():
        gamestate.destroy(Target)
        card.adapt()
        card.adapt()

    if "Razorpetal Lasher" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Razopetal"))

    if "Rockpool Hunter" == card.getName():
        if Target != None:
            gamestate.adjCardHealth(Target, 1)
            gamestate.adjCardAttack(Target, 1)

    if "Silver Hand Knight" == card.getName():
        gamestate.summon(player, HSCard, HSCard("Squire"))

    if "Spellbreaker" == card.getName():
        if Target != None:
            gamestate.silence(Target)  #todowrite silence method
    if "Streetwise Investigator" == card.getName():
        for card in gamestate.Board[player * -1]:
            if "Stealth" in card.Mechanics:
                card.Mechanics.remove("Stealth")

    if "Swashburglar" == card.getName():
        gamestate.addCardHand(player, HSCard, HSCard.getRandomCard(Class == gamestate.Class[player]))

    if "Tanaris Hogchopper" == card.getName():
        if gamestate.Hand[player * -1] == []:
            card.Mechanics.append("Charge")  #todoaddMechanic methode

    if "Temple Enforcer" == card.getName():
        if Target != None:
            gamestate.adjCardHealth(Target, 3)

    if "Thunder Lizard" == card.getName():
    #todo
        pass

    if "Tortollan Forager" == card.getName():
        gamestate.addCardHand(player, HSCard.HSCard.getRandomCard(Attack=5))

    if "Toxic Sewer Ooze" == card.getName():
        gamestate.adjWeapon(player, -1)

    if "Twilight Flamecaller" == card.getName():
        for card in gamestate.Board[player * -1]:
            gamestate.adjCardHealth(card, -1)

    if "Twilight Geomancer" == card.getName():
        gamestate.CThunMechanics[player].append("Taunt")

    if "Verdant Longneck" == card.getName():
        Adapt(card)

    if "Youthful Brewmaster" == card.getName():
        if Target != None:
            Target.reset()
            gamestate.Board[player].remove(Target)
            gamestate.Hand[player].append(Target)

    if "Zoobot" == card.getName():
        beastlist = []
        dragonlist = []
        murloclist = []
        for card in gamestate.Board[player]:
            if card.Type == "Beast":
                beastlist.append(card)
            if card.Type == "Dragon":
                dragonlist.append(card)
            if card.Type == "Murloc":
                murloclist.append(card)
        dragon = random.choice(dragonlist)
        beast = random.choice(beastlist)
        murloc = random.choice(murloclist)
        gamestate.adjCardhealth(dragon, 1)
        gamestate.adjCardAttack(dragon, 1)
        gamestate.adjCardhealth(beast, 1)
        gamestate.adjCardAttack(beast, 1)
        gamestate.adjCardhealth(murloc, 1)
        gamestate.adjCardAttack(murloc, 1)

    if "Aldor Peacekeeper" == card.getName():
        if Target != None:
            gamestate.setCardAttack(Target, 1)

    if "Ancient Mage" == card.getName():
        index = gamestate.Board[player].find[card]
        if index > 1:
            gamestate.Board[player][index - 1].SpellDamage += 1
        if index < len(gamestate.Board[player]):
            gamestate.Board[player][index + 1].SpellDamage += 1

    if "Ancient Shieldbearer" == card.getName():
        if gamestate.CthunStats[player] >= 10:
            gamestate.adjArmor(10, player)

    if "Arcane Golem" == card.getName():
        gamestate.addManaCrystal(player * -1)

    if "Avian Watcher" == card.getName():
        if gamestate.Secret[player] != []:
            gamestate.adjCardHealth(card, 1)
            gamestate.adjCardAttack(card, 1)

    if "Babbling Book" == card.getName():
    #todo
        pass

    if "Bloodsail Corsair" == card.getName():
        #gamestate.adjWeapon(player * -1, 0, -1)
        pass

    if "Bloodsail Cultist" == card.getName():
        Pirate = False
        for cardNew in gamestate.Board[player]:
            if cardNew.Type == "Pirate":
                Pirate = True
        if Pirate:
            gamestate.adjWeapon(player, 1, 1)

    if "Bomb Squad" == card.getName():
        if Target != None:
            gamestate.adjCardHealth(Target, -5)

    if "Book Wyrm" == card.getName():
        if Target != None:
            gamestate.destroy(Target)

    if "Celestial Dreamer" == card.getName():
        bool = False
        for cardNew in gamestate.Board[player]:
            if cardNew.getAttack() >= 5:
                bool = True
        if bool:
            gamestate.adjCardHealth(card, 2)
            gamestate.adjCardAttack(card, 2)

    if "Coldlight Oracle" == card.getName():
        gamestate.draw(player)
        gamestate.draw(player)
        gamestate.draw(player * -1)
        gamestate.draw(player * -1)

    if "Coldlight Seer" == card.getName():
        for cardNew in gamestate.Board[player]:
            if cardNew.Type == "Murloc":
                gamestate.adjCardHealth(cardNew, 2)

    if "Cornered Sentry" == card.getName():
        gamestate.summon(HSCard.HSCard("Raptor"), player * -1)
        gamestate.summon(HSCard.HSCard("Raptor"), player * -1)
        gamestate.summon(HSCard.HSCard("Raptor"), player * -1)

    if "Corrupted Seer" == card.getName():
        for cardNew in gamestate.Board[:]:
            if cardNew.Type != "Murloc":
                gamestate.adjCardHealth(cardNew, -2)

    if "Crazed Alchemist" == card.getName():
        if Target != None:
            at = Target.getAttack()
            he = Target.getHealth()
            gamestate.setCardHealth(Target, at)
            gamestate.setCardAttack(Target, he)

    if "Darkshire Librarian" == card.getName():
        gamestate.discardRandom(player)

    if "Defender of Argus" == card.getName():
        index = gamestate.Board[player].find[card]
        if index > 1:
            gamestate.Board[player][index - 1].Mechanics.append("Taunt")
        if index < len(gamestate.Board[player]):
            gamestate.Board[player][index + 1].Mechanics.append("Taunt")

    if "Disciple of C'Thun" == card.getName():
        if Target != None:
            gamestate.adjCardHealth(Target, -2) if Target.Type != Hero else gamestate.adjHealth(-2,
                                                                                                          player * -1)

    if "Dispatch Kodo" == card.getName():
        if Target != None:
            gamestate.adjHealth(card.Attack,
                                     Target.player) if Target.Type == "Hero" else gamestate.adjCardHealth(
                card.Attack, Target.player)

    if "Doomcaller" == card.getName():
        gamestate.adjCThunAttack(2, player)
        gamestate.adjCThunHealth(2, player)
        #todo
        pass

    if "Doomguard" == card.getName():
        gamestate.discardRandom()
        gamestate.discardRandom()

    if "Doppelgangster" == card.getName():
    #todo
        pass

    if "Drakonid Operative" == card.getName():
        Dragon = False
        for cardNew in gamestate.Hand[player]:
            if cardNew.Type == "Dragon":
                Dragon = True
        if Dragon:
            Discover("OpponentDeck", player)

    if "Eater of Secrets" == card.getName():
        gamestate.Secret[player * -1] = []

    if "Ethereal Peddler" == card.getName():
    #todo
        pass

    if "Felguard" == card.getName():
        gamestate.ManaCrystals[player] -= 1

    if "Fire Plume Harbinger" == card.getName():
        for cardNew in gamestate.Hand[player]:
            if cardNew.Type == "Elemental":
                cardNew.Cost -= 1

    if "Forlorn Stalker" == card.getName():
        for cardNew in gamestate.Hand[player]:
            if "Deathrattle" in cardNew.Mechanics:
                gamestate.adjCardHealth(cardNew, 1)
                gamestate.adjCardAttack(cardNew, 1)

    if "Golakka Crawler" == card.getName():
        if Target != None:
            gamestate.destroy(Target)
            gamestate.adjCardHealth(card, 1)
            gamestate.adjCardAttack(card, 1)

    if "Grimestreet Informant" == card.getName():
        Discover("Hunter", player)
        Discover("Paladin", player)
        Discover("Warrior", player)

    if "Grimestreet Pawnbroker" == card.getName():
        list = []
        for cardNew in gamestate.Hand[player]:
            if cardNew.Type == "Weapon":
                list.append(cardNew)
        cardNew = random.choice(list)
        gamestate.adjCardHealth(cardNew, 1)
        gamestate.adjCardAttack(cardNew, 1)

    if "Grimestreet Protector" == card.getName():
        #index = gamestate.Board[player].find[card]
        #if index > 1:
        #    gamestate.Board[player][index - 1].Mechanics.append("Divine Shield")
        #if index < len(gamestate.Board[player]):
        #    gamestate.Board[player][index + 1].Mechanics.append("Divine Shield")
        pass
    if "Injured Blademaster" == card.getName():
        gamestate.adjCardHealth(card, -4)

    if "Ivory Knight" == card.getName():
        Cost = Discover("Spell")[1]
        gamestate.healHealth(player, Cost)

    if "Jade Claws" == card.getName():
        gamestate.summonJade(player)

    if "Jinyu Waterspeaker" == card.getName():
        if Target != None:
            gamestate.healCardHealth(Target, 6) if Target.Type != "Hero" else gamestate.healHealth(Target,
                                                                                                             6)

    if "Kabal Courier" == card.getName():
        Discover("Mage".player)
        Discover("Priest", player)
        Discover("Warlock", player)

    if "Kirin Tor Mage" == card.getName():
    #todo
        pass

    if "Klaxxi Amber-Weaver" == card.getName():
        if gamestate.CthunStats >= 10:
            gamestate.adjCardHealth(card)

    if "Lightfused Stegodon" == card.getName():
        for cardNew in gamestate.Board[player]:
            if card.getName() == "Silver Hand Recruit":
                Adapt(cardNew)

    if "Lotus Agents" == card.getName():
        Discover("Druid", player)
        Discover("Rogue", player)
        Discover("Shaman", player)

    if "Master of Disguise" == card.getName():
    #todo
        pass

    if "Master of Evolution" == card.getName():
    #todo
        pass

    if "Midnight Drake" == card.getName():
        for card in gamestate.Hand[player]:
            gamestate.adjCardAttack(card, 1)

    if "Mind Control Tech" == card.getName():
        pass
        #if len(gamestate.Board[player * -1]) > 3:
        #    cardNew = random.choice(gamestate.Board[player * -1])
        #    gamestate.summon(cardNew, player)
        #    gamestate.Board[player].remove(cardNew)

    if "Moat Lurker" == card.getName():
    #todo
        pass

    if "Onyx Bishop" == card.getName():
        cardNew = random.choice(gamestate.Graveyard[player])
        cardNew.reset()
        gamestate.summon(cardNew, player)

    if "Perdition's Blade" == card.getName():
    #todo
        pass

    if "Rallying Blade" == card.getName():
        for cardNew in gamestate.Board[player]:
            if "Divine Shield" in cardNew.Mechanics:
                gamestate.adjCardHealth(cardNew, 1)
                gamestate.adjCardAtack(cardNew, 1)

    if "Seadevil Stinger" == card.getName():
    #todo
        pass

    if "Servant of Kalimos" == card.getName():
    #todo
        pass

    if "Servant of Yogg-Saron" == card.getName():
    #todo
        pass

    if "Shadow Sensei" == card.getName():
        if Target != None:
            gamestate.adjCardHealth(Target, 2)
            gamestate.adjCardAttack(Target, 2)

    if "Skeram Cultist" == card.getName():
        gamestate.adjCThunAttack(2, player)
        gamestate.adjCThunHealth(2, player)

    if "Spiked Hogrider" == card.getName():
        for card in gamestate.Board[player * -1]:
            if "Taunt" in card.Mechanics:
                if "Charge" not in card.Mechanics: card.Mechanics.append("Charge")

    if "Stampeding Kodo" == card.getName():
        list = []
        for card in gamestate.Board[player * -1]:
            if card.Attack == 2:
                list.append(card)
        if list != []:
            Target = random.choice(list)
            gamestate.destroy(Target)

    if "Steam Surger" == card.getName():
    #todo
        pass

    if "Stonehill Defender" == card.getName():
    #todo
        pass

    if "Sunfury Protector" == card.getName():
        pass
        #index = gamestate.Board[player].find(card)
        #if index != 0:
        #    if "Taunt" not in gamestate.Board[player][index - 1].Mechanics: gamestate.Board[player][
        #        index - 1].Mechanics.append("Taunt")
        #if index != len(gamestate.Board[player]):
        #    if "Taunt" not in gamestate.Board[player][index + 1].Mechanics: gamestate.Board[player][
        #        index + 1].Mechanics.append("Taunt")

    if "Terrorscale Stalker" == card.getName():
        if Target != None:
            triggerDeathrattle(Target, player)

    if "Tol'vir Stoneshaper" == card.getName():
    #todo
        pass

    if "Tol'vir Warden" == card.getName():
        list = []
        for card in gamestate.Deck[player]:
            if card.Cost == 1:
                list.append(card)
        if list != []:
            Target = random.choice(list)
            gamestate.addCardHand(Target)
            list.remove(Target)
            Target = random.choice(list)
            gamestate.addCardHand(Target)

    if "Trogg Beastrager" == card.getName():
        list = []
        for card in gamestate.Hand[player]:
            if card.Type == "Beast":
                list.append(card)
        if list != []:
            Target = random.choice(list)
            gamestate.adjCardHealth(Target, 1)
            gamestate.adjCardAttack(Target, 1)

    if "Twilight Darkmender" == card.getName():
        if gamestate.CthunStats[player][1] >= 10:
            gamestate.adjHealth(10, player)

    if "Twilight Drake" == card.getName():
        for card in gamestate.Board[player]:
            gamestate.adjCardHealth(card, 1)

    if "Virmen Sensei" == card.getName():
        #todo just copy houndmaster
        pass

    if "Void Terror" == card.getName():
        index = gamestate.Board[player].find(card)
        if index != 0:
            cardLe = gamestate.Board[player][index - 1]
            gamestate.adjCardHealth(card, cardLe.getHealth())
            gamestate.adjCardAttack(card, cardLe.getAttack())
            gamestate.destroy(cardLe)
        if index != len(gamestate.Board[player]):
            cardRi = gamestate.Board[player][index + 1]
            gamestate.adjCardHealth(card, cardRi.getHealth())
            gamestate.adjCardAttack(card, cardRi.getAttack())
            gamestate.destroy(cardRi)

    if "Volcanosaur" == card.getName():
    #todo
        pass

    if "Big Game Hunter" == card.getName():
        if Target != None:
            gamestate.destroy(Target)

    if "Blade of C'Thun" == card.getName():
        if Target != None:
            gamestate.adjCThunHealth(Target.getHealth(), player)
            gamestate.adjCThunHealth(Target.getAttack(), player)
            gamestate.destroy(Target)

    if "Blazecaller" == card.getName():
    #todo
        pass

    if "Blood Knight" == card.getName():
        for cardNew in gamestate.Board[:]:
            if "Divine Shield" in cardNew.Mechanics:
                cardNew.Mechanics.remove("Divine Shield")
                gamestate.adjCardHealth(card, 3)
                gamestate.adjCardAttack(card, 3)

    if "Bright-Eyed Scout" == card.getName():
        cardNew = gamestate.draw(player)
        gamestate.setCost(cardNew, 5)

    if "Cabal Shadow Priest" == card.getName():
        if Target != None:
            if len(gamestate.Board[player]) <7:
                gamestate.Board[player * -1].remove(Target)
                gamestate.Board[player].append(Target)

    if "Charged Devilsaur" == card.getName():
    #todo
        pass

    if "Chittering Tunneler" == card.getName():
    #todo
        pass

    if "Curious Glimmerroot" == card.getName():
        if gamestate.Deck[player * -1] != []:
            cardNew = random.choice(gamestate.Deck[player * -1])
            ran = random.randint(1, 3)
            if ran == 2:
                gamestate.addCardHand(cardNew, player)

    if "Cyclopian Horror" == card.getName():
        for card in gamestate.Board[player * -1]:
            gamestate.adjCardHealth(card, 1)

    if "Darkspeaker" == card.getName():
        if Target != None:
            tempAt = card.getAttack()
            tempHe = card.getHealth()
            tempMaxAt = card.getMaxAttack()
            tempMaxHe = card.getMaxHealth()
            card.setAttack(Target.getAttack())
            card.setHealth(Target.getHealth())
            card.setMaxHealth(Target.MaxHealth)
            card.setMaxAttack(Target.MaxAttack)
            Target.setAttack(tempAt)
            Target.setHealth(tempHe)
            Target.setMaxAttack(tempMaxAt)
            Target.setMaxHealth(tempMaxHe)

    if "Defias Cleaner" == card.getName():
    #todo
        pass

    if "Dirty Rat" == card.getName():
        cardNew = random.choice(gamestate.Hand[player * -1])
        gamestate.summonfromHand(cardNew)

    if "Eternal Sentinel" == card.getName():
        gamestate.ManaCrystals = gamestate.EmptyManaCrystals

    if "Faceless Manipulator" == card.getName():
        if Target != None:
            card = HSCard.HSCard(Target.getName)
            card.adjHealth(Target.Health - Target.MaxHealth)
            card.adjHealth(Target.Attack - Target.MaxAttack)

    if "Faceless Shambler" == card.getName():
        if Target != None:
            gamestate.setCardHealth(card, Target.getHealth())
            gamestate.setCardAttack(card, Target.getAttack())

    if "Fight Promoter" == card.getName():
        SixHealth = False
        for card in gamestate.Board[player]:
            if card.getHealth() >= 6:
                SixHealth = True
        if SixHealth:
            gamestate.draw(player)
            gamestate.draw(player)

    if "Forbidden Ancient" == card.getName():
        gamestate.adjCardAttack(card, gamestate.getMana())
        gamestate.adjCardHealth(card, gamestate.getMana())
        gamestate.ManaCrystals[player] = 0

    if "Gentle Megasaur" == card.getName():
        for card in gamestate.Board[player]:
            if card.Type == "Murloc":
                Adapt(card)

    if "Gluttonous Ooze" == card.getName():
        if gamestate.Weapon[player * -1] != None:
            gamestate.adjArmor(gamestate.Weapon[player * -1], player)
            gamestate.destroy(gamestate.Weapon[player * -1])

    if "Hungry Crab" == card.getName():
        if Target != None:
            gamestate.destroy(Target)
            gamestate.adjCardAttack(card, 2)
            gamestate.adjCardHealth(card, 2)

    if "Leatherclad Hogleader" == card.getName():
        if len(gamestate.Hand[player * -1]) >= 6:
            card.Mechanics.append("Charge")

    if "Luckydo Buccaneer" == card.getName():
        if gamestate.Weapon[player].Attack >= 3:
            gamestate.adjCardHealth(card, 4)
            gamestate.adjCardAttack(card, 4)

    if "Manic Soulcaster" == card.getName():
        card = HSCard.HSCard(Target.getName())
        i = random.randint(1, len(gamestate.Deck[player]))
        gamestate.Deck[player] = gamestate.Deck[player][:, i] + [card] + gamestate.decl[player][i, :]

    if "Pit Lord" == card.getName():
        gamestate.adjHealth(-5, player)

    if "Primordial Drake" == card.getName():
        #for card in gamestate.Board[:]:
        #    gamestate.adjCardHealth(card, -2)
        pass
    if "Shadowcaster" == card.getName():
        Target = HSCard.HSCard(Target.getName())
        Target.setHealth(1)
        Target.setAttack(1)
        gamestate.addCardHand(Target)

    if "Stone Sentinel" == card.getName():
    #todo
        pass

    if "Tortollan Primalist" == card.getName():
    #todo
        pass

    if "Vilefin Inquisitor" == card.getName():
    #todo
        pass

    if "Alexstrasza" == card.getName():
        Target.Health = 15

    if "Amara, Warden of Hope" == card.getName():
        gamestate.Health[player] = 40

    if "Aya Blackpaw" == card.getName():
        card = gamestate.summon(HSCard.HSCard("Jade"), player)
        gamestate.setCardAttack(gamestate.JadeCount[player])
        gamestate.setCardHealth(gamestate.JadeCount[player])

    if "Barnabus the Stomper" == card.getName():
        for cardNew in gamestate.Deck[player]:
            if cardNew.type == "MININ": cardNew.setCost = 0

    if "Barnes" == card.getName():
        cardNew = random.choice(gamestate.Deck[player])
        cardNew = gamestate.summonfromdeck(cardNew, player)
        cardNew.setHealth(1)
        cardNew.setAttack(1)  #todo setAttack also set max attack? set health also sethealth?

    if "C'Thun" == card.getName():
        for counter in range(gamestate.CthunStats[player][1]):
            index = random.randint(1, len(gamestate.Board[player * -1]) + 1)
            if index < len(gamestate.Board[player * -1]):
                gamestate.adjHealth(1, gamestate.Board[player * -1][index])
            else:
                selfff.gamestate.adjHealth(1, player * -1)

    if "Captain Greenskin   " == card.getName():
        if gamestate.Weapon[player] != None:
            gamestate.weapon[player].Health += 1
            gamestate.weapon[player].Attack += 1

    if "Cho'gall" == card.getName():
    #todo
        pass

    if "Deathwing" == card.getName():
        for minion in gamestate.Board[:]:
            if minion != card:
                gamestate.destroy(minion)
        for minion in gamestate.Hand[player]:
            gamestate.discard(minion)

    if "Don Han'Cho" == card.getName():
        cardNew = random.choice(gamestate.Hand[player])
        cardNew.Health += 5
        cardNew.Attack += 5

    if "Galvadon" == card.getName():
        for i in range(5):
            card.Adapt()

    if "Harrison Jones" == card.getName():
        if gamestate.Weapon[player * -1] != None:
            Health = gamestate.Weapon[player * -1].getHealth()
            counter = 1
            for counter in range(Health):
                gamestate.draw(player)
            gamestate.destroy(gamestate.Weapon[player * -1])
    if "Hemet, Jungle Hunter" == card.getName():
        for cardNew in gamestate.Deck[player]:
            if cardNew.Health <= 3:
                gamestate.destroy(cardNew)

    if "Herald Volazj" == card.getName():
        for cardNew in gamestate.Board[player]:
            if cardNew != card:
                cardSum = gamestate.summon(cardNew)
                cardSum.setHealth(1)
                cardSum.setAtttack(1)

    if "Hobart Grapplehammer" == card.getName():
        for card in gamestate.Deck[player] or gamestate.Hand[player]:
            if card.Type == "Weapon":
                card.Attack += 1

    if "Inkmaster Solia" == card.getName():
    #todo
        pass

    if "Kalimos, Primal Lord" == card.getName():
    #todo
        pass

    if "Kazakus" == card.getName():
    #todo
        pass

    if "King Mosh" == card.getName():
        for card in gamestate.Board[:]:
            if card.getHealth() != card.getMaxHealth():
                gamestate.destroy(card)

    if "King Mukla" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Bananas"), player * - 1)
        gamestate.addCardHand(HSCard.HSCard("Bananas"), player * -1)

    if "Krul the Unshackled" == card.getName():
        double = False
        list = []
        for cardNew in gamestate.Deck[player]:
            if cardNew.getName() in list:
                double = True
            list.append(cardNew.getName)
        if not double:
            for cardNew in gamestate.Hand[player]:
                if cardNew.race == "Demon":
                    gamestate.summonfromHand(cardNew)

    if "Leeroy Jenkins" == card.getName():
        gamestate.addToBoard(HSCard.HSCard("Whelp"))
        gamestate.addToBoard(HSCard.HSCard("Whelp"))

    if "Lord Jaraxxus" == card.getName():
    #todo
        pass

    if "Madam Goya" == card.getName():
        indexD = random.choice(0, len(gamestate.Deck[player]) - 1)
        cardNew = gamestate.Deck[player][indexD]
        indexB = gamestate.Board[player].find(Target)
        gamestate.Board[player][indexB] = Target  # reset Target stats
        gamestate.Deck[player][indexD] = cardNew  # reset Card stats

    if "Malkorok" == card.getName():
    #todo
        pass

    if "Medivh, the Guardian" == card.getName():
        gamestate.Weapon[player] = HSCard.HSCard("Atiesh")

    if "Megafin" == card.getName():
        while len(gamestate.Hand(player)) < 10:
            gamestate.addToBoard(  # todo summon random murloc)
            )
    if "Millhouse Manastorm" == card.getName():
    #todo
        pass

    if "Mukla, Tyrant of the Vale" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Bananas"), player)
        gamestate.addCardHand(HSCard.HSCard("Bananas"), player)

    if "N'Zoth, the Corruptor" == card.getName():
    #todo
        pass

    if "Onyxia" == card.getName():
        while len(gamestate.Board(player)) < 7:
            gamestate.addToBoard(HSCard.HSCard("Whelp"))

    if "Ozruk" == card.getName():
    #todo
        pass

    if "Princess Huhuran" == card.getName():
        triggerDeathrattle(Target, player)

    if "Queen Carnassa" == card.getName():
        for counter in range(15):
            gamestate.addCardDeck(HSCard.HSCard("Carnassa's Brood"))

    if "Raza the Chained" == card.getName():
        list = [card.getName for card in gamestate.Board[player]]

    if "Sulfuras" == card.getName():
        gamestate.HeroPower[player] = HSCard.HSCard("DIE, INSECT!")

    if "Sunkeeper Tarim" == card.getName():
        for cardNew in gamestate.Board[:]:
            cardNew.setHealth(3)
            cardNew.setAttack(3)

    if "The Black Knight" == card.getName():
        #gamestate.destroy(Target)
        pass
    if "The Curator" == card.getName():
        #drawBeast = True
        #drawDragon = True
        #drawMurloc = True
        #for cardNew in gamestate.Deck[player]:
        #    # random cause decks are shuffled
        #    if cardNew.race == "Beast" and drawBeast:
        #        gamestate.addCardHand(cardNew)
        #        drawBeast = False
        #    if cardNew.race == "Dragon" and drawDragon:
        #        gamestate.addCardHand(cardNew)
        #        drawDragon = False
        #    if cardNew.race == "Murloc" and drawMurloc:
        #        gamestate.addCardHand(cardNew)
       #         drawMurloc = False
        pass
    if "Tinkmaster Overspark" == card.getName():
        cardNew = random.choice(gamestate.Board[:])
        Ammount = random.choice([1, 5])
        gamestate.setCardHealth(cardNew, Ammount)
        gamestate.setCardAttack(cardNew, Ammount)
    if "Twin Emperor Vek'lor" == card.getName():
    #todo
        pass

    if "Wrathion" == card.getName():
        card = gamestate.draw
        while card.race != "Dragon":
            card = gamestate.draw

    if "Xaril, Poisoned Mind" == card.getName():
        addToxin(player)

    if "Yogg-Saron, Hope's End" == card.getName():

#todo
        pass

def triggerDeathrattle(gamestate, card, player):
    deathText = ""
    #todo only card names
    if "Summon a " in deathText and "for your opponent" not in deathText:
        newCard = deathText[33:]
        index = gamestate.Board[player][gamestate.getCardBoardPos(card)]
        gamestate.Board[player] = gamestate.Board[player][:index] + [HSCard.HSCard(newCard)] + \
                                       gamestate.Board[player][index:]

    if "Summon two " in deathText and "for your opponent" not in deathText:
        newCard = deathText[35:]
        index = gamestate.Board[player][gamestate.getCardBoardPos(card)]
        gamestate.Board[player] = gamestate.Board[player][:index] + [HSCard.HSCard(newCard)] + [
            HSCard.HSCard(newCard)] + gamestate.Board[player][index:]

    if "Draw a card" in deathText:
        draw(player)
    if "White Eyes" == card.getName():
        gamestate.Deck[player].append(HSCard.HSCard("The Storm Guardian"))
    if "Summon a " in deathText and "for your opponent" in deathText:
        index = deathText.find(" for your op")
        newCard = deathText[33:index]
        index = gamestate.Board[player][gamestate.getCardBoardPos(card)]
        gamestate.Board[player] = gamestate.Board[player][:index] + [HSCard.HSCard(newCard)] + \
                                       gamestate.Board[player][index:]

    if "Tirion Fordring" == card.getName():
        gamestate.Weapon[player] = HSCard.HSCard("Ashbringer")

    if "Sherazin, Corpse Flower" == card.getName():
    #todo
        pass

    if "Sergeant Sally" == card.getName():
    #todo
        pass

    if "Xaril, Poisoned Mind" == card.getText():
        addToxin(player)

    if "Pyros" == card.getName():
    #todo
        pass

    if "Deathwing, Dragonlord" == card.getName():
    #todo
        pass

    if "Anomalus" == card.getName():
        for cardNew in gamestate.Board[player]:
            gamestate.adjCardHealth(cardNew, -8, player)
        for cardNew in gamestate.Board[player * -1]:
            gamestate.adjCardHealth(cardNew, -8, player * -1)

    if "summon a Jade Golem" in card.getText():
    #todo
        pass

    if "Weasel Tunneler" == card.getName():
        deck = gamestate.Deck[player]
        index = random.randint(0, len(deck))
        gamestate.Deck[player] = deck[index, :] + [HSCard.HSCard("Weasel Tunneler")] + deck[:, index]

    if "Return this to your hand" in card.getText():
        gamestate.addCardHand(card.reset(), player)

    if "Rat Pack" == card.getName():
        counter = 0
        for counter in range(card.getAttack):
            gamestate.summon(HSCard.HSCard("Rat"))

    if "Primalfin Champion" == card.getName():
    #todo
        pass

    if "Meanstreat Marshall" == card.getName():
        if card.Attack >= 2:
            gamestate.draw(player)

    if "Giant Anaconda" == card.getName():
        list = []
        for cardNew in gamestate.Hand[player]:
            if cardNew.getCost >= 5:
                list.append(cardNew)
        gamestate.summon(random.choice(list), player)

    if "Undercity Huckster" == card.getName():
       # todo cmethod that gets all cards, minnions, spells from class
        pass
    if "Shifting Shade" == card.getName():
        cardNew = random.choice(gamestate.Deck[player * -1])
        gamestate.addCardHand(cardNew, player)

    if "Selfless Hero" == card.getName():
        cardNew = random.choice(gamestate.Board[player])
        if cardNew.Mechanics.find("Divine Shield") == -1: cardNew.Mechanics.append("Divine Shield")

    if "Raptor Hatchling" == card.getName():
        deck = gamestate.Deck[player]
        index = random.randint(0, len(deck))
        gamestate.Deck[player] = deck[index, :] + [HSCard.HSCard("Raptor Patriarch")] + deck[:, index]

    if "Moat Lurker" == card.getName():
    #todo
        pass

    if "Direhorn Hatchling" == card.getName():
        deck = gamestate.Deck[player]
        index = random.randint(0, len(deck))
        gamestate.Deck[player] = deck[:, index] + [HSCard.HSCard("Direhorn Matriarch")] + deck[index, :]

    if "Crystalline Oracle" == card.getName():
        cardNew = random.choice(gamestate.Deck[player * -1])
        gamestate.addCardHand(cardNew, player)

    if "Corrupted Healbot" == card.getName():
        gamestate.adjHealth(8, player * -1)

    if "Bomb Squad" == card.getName():
        gamestate.adjHealth(-5, player)

    if card.getName == "Abomination":
        for cardNew in gamestate.Board[player]:
            gamestate.adjHealth(cardNew, -1)
        for cardNew in gamestate.Board[player * -1]:
            gamestate.adjHealth(cardNew, -1)
        gamestate.adjHealth(-2, player)
        gamestate.adjHealth(-2, player * -1)

    if "Zealus Initiate" == card.getName():
        cardNew = random.choice(gamestate.Board[player])
        gamestate.adjCardHealth(cardNew, 1)
        gamestate.adjCardAttack(cardNew, 1)

    if "Volatile Elemental" == card.getName():
        cardNew = random.choice(gamestate.Board[player * -1])
        gamestate.adjCardHealth(cardNew, -1)

    if "Tortollan Shellraiser" == card.getName():
        cardNew = random.choice(gamestate.Board[player])
        gamestate.adjCardHealth(cardNew, 1)
        gamestate.adjCardAttack(cardNew, 1)

    if "Tentacle of N'Zoth" == card.getName():
        for cardNew in gamestate.Board[player]:
            gamestate.adjCardHealth(cardNew, -1)
        for cardNew in gamestate.Board[player * -1]:
            gamestate.adjCardHealth(cardNew, -1)
    if "Spawn of N'Zoth" == card.getName():
        for cardNew in gamestate.Board[player]:
            gamestate.adjCardAttack(cardNew, 1, player)
            gamestate.adjCardHealth(cardNew, 1, player)

    if "Southsea Squidface" == card.getName():
        if gamestate.Weapon[player] != None:
            gamestate.Weapon[player].Health += 2

    if "Shimmering Tempest" == card.getName():
    #todo
        pass
    if "Shaky Zipgunner" == card.getName():
        Minion = random.choice(gamestate.getMinnionsHand(player))
        gamestate.adjCardHealth(Minion, 2, player)
        gamestate.adjCardAttack(Minion, 2, player)

    if "Sated Threshadon" == card.getName():
        for counter in range(3):
            gamestate.summon(HSCard.HSCard("Primalfin"), player)

    if "Mistress of Mixtures" == card.getName():
        gamestate.adjHealth(4, player)
        gamestate.adjHealth(4, player * -1)

    if "Leper Gnome" == card.getName():
        gamestate.adjHealth(-2, player * -1)

    if "Igneous Elemental" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Flame Elemental"), player)
        gamestate.addCardHand(HSCard.HSCard("Flame Elemental"), player)

    if "Fiery Bat" == card.getName():
        index = random.randint(0, len(gamestate.Board[player * -1]))
        if index == gamestate.Board[player * -1]:
            gamestate.adjHealth(-1, player * -1)
        else:
            gamestate.adjCardHealth(gamestate.Board[player * -1][index], -1)

    if "Deadly Fork" == card.getName():
        gamestate.addCardHand(HSCard.HSCard("Sharp Fork"), player)

    if "Backstreet Leper" == card.getName():
        gamestate.adjHealth(-2, player * -1)

    if "Mana Treant" == card.getName():
        gamestate.addManaSpace(player)

    # todo cards that give deathrattles ,mostly spells, will change card texts but the effects are not implemented yet
    #for x in gamestate.Board:
    #    for y in x:
    #        for cards in y:
    #            checkdie(cards, player)
    #            # todo check if a minion died