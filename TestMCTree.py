import numpy as np
import random
import time
import math
import copy
import Gamestate
import Move
import HSCard
random.seed(time.time())

# Moves: ["p",card] or ["a",card,(card or hero)]
#this should work
def listoflegalmoves(gamestate):
    #todo spells and other stupid shit
    listoflegalmoves = []
    for card in gamestate.Hand[gamestate.ActivePlayer]:
        if card.Cost <= gamestate.ManaCrystals[gamestate.ActivePlayer]:
            listoflegalmoves.append(Move.Move("p",card))
    for card in gamestate.Board[gamestate.ActivePlayer]:
        if card.canAttack:
            for enemycard in gamestate.Board[gamestate.ActivePlayer * -1]:
                listoflegalmoves.append(Move.Move("a",card,enemycard))
                # enemychampion
            listoflegalmoves.append(Move.Move("a",card,gamestate.ActivePlayer*-1))
    # no move
    listoflegalmoves.append(Move.Move("end"))
    #print("legallist")
    #print(listoflegalmoves)
    #for card in gamestate.Hand[gamestate.ActivePlayer]:
    #    print(card.Name)
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

def simTurn(gamestate, move):

    movecards = copy.copy(move)

    if move.type == "end":
        gamestate.ActivePlayer *= -1
        gamestate.EmptyManaCrystals[gamestate.ActivePlayer] += 1
        gamestate.ManaCrystals = gamestate.EmptyManaCrystals
        #todo uncomment just for testing
        #gamestate.draw(gamestate.ActivePlayer)
        for card in gamestate.Board[gamestate.ActivePlayer]:
            card.canAttack = True
        for card in gamestate.Board[gamestate.ActivePlayer * -1]:
            card.canAttack = True
    elif move.type == "p":
        gamestate.ManaCrystals[gamestate.ActivePlayer] -= movecards.actioncard.Cost
        if len(gamestate.Board[gamestate.ActivePlayer]) < 7:
            gamestate.Board[gamestate.ActivePlayer].append(movecards.actioncard)
        i = -1
        b = -1
        for card in gamestate.Hand[gamestate.ActivePlayer]:
            i += 1
            if card == movecards.actioncard:
                b = i

        if b != -1:
            gamestate.Hand[gamestate.ActivePlayer].pop(b)
    elif move.type == "a":
        if movecards.target == 1 or movecards.target == -1:
            gamestate.Health[movecards.target] -= movecards.actioncard.Attack
        else:
            if movecards.actioncard.Health - movecards.target.Attack <= 0:
                #gamestate.Board[gamestate.ActivePlayer].remove(movecards.actioncard)

                i = -1
                b = -1
                for card in gamestate.Board[gamestate.ActivePlayer]:
                    i += 1
                    if card == movecards.actioncard:
                        b = i

                if b != -1:
                    gamestate.Board[gamestate.ActivePlayer].pop(b)
            if movecards.target.Health - movecards.actioncard.Attack <= 0:
                #gamestate.Board[gamestate.ActivePlayer * -1].remove(movecards.target)
                i = -1
                b = -1
                for card in gamestate.Board[gamestate.ActivePlayer]:
                    i += 1
                    if card == movecards.actioncard:
                        b = i
                if b != -1:
                    gamestate.Board[gamestate.ActivePlayer].pop(b)
            movecards.actioncard.Health -= movecards.target.Attack
            movecards.target.Health -= movecards.actioncard.Attack

def simGame(gamestatestart):
    gamestate = gamestatestart.clone()
    rounds = 0

    while checkEndGame(gamestate) == False and not (gamestate.Board == [[], [], []] and gamestate.Hand == [[], [], []]):


        legalMove = random.choice(listoflegalmoves(gamestate))

        simTurn(gamestate, legalMove)
        rounds += 1
    return checkEndGame(gamestate), rounds


class TreeNode:
    def __init__(self, gamestate):
        self.parent = None
        self.children = []
        self.NumGames = 0
        self.gamestate = gamestate
        self.move = [0, 0]  # Move that led from parent to this gamestate.
        self.v = 0

    def hasChild(self):
        return len(self.children) > 0

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def hasParent(self):
        return not self.parent == None

    def update(self, v):
        self.v += v
        self.NumGames += 1

def calcUCB1(Node):
    return Node.v / (1. * Node.NumGames) + math.sqrt(
        30 * math.log(Node.parent.NumGames) / (1. * Node.NumGames)) if Node.NumGames > 0 else 99999999


def selectChild(RNode):
    i = 0
    theWinner = None
    for child in RNode.children:
        if calcUCB1(child) >= i:
            theWinner = child
            i = calcUCB1(child)
    return theWinner


def selectfinalChild(RNode):
    i = 0
    theWinner = None
    for child in RNode.children:
        if child.NumGames >= i:
            theWinner = child
            i = child.NumGames
    return theWinner

def FindMove(gamestate, N = 5000):
    root = TreeNode(gamestate)
    for simNumber in range(N):
        curNode = root
        while curNode.hasChild():
            curNode = selectChild(curNode)
       # if simNumber == 10:
            #print(listoflegalmoves(curNode.gamestate))
        for move in listoflegalmoves(curNode.gamestate):
            t = curNode.gamestate
            nextstate = copy.deepcopy(t)
            simTurn(nextstate, move)
            tempNode = TreeNode(nextstate)
            tempNode.move = move
            curNode.addChild(tempNode)
        if checkIfRunning(curNode.gamestate):
            curNode = selectChild(curNode)
        player, rounds = simGame(curNode.gamestate)
        v = 1 if player == (-1) * curNode.gamestate.ActivePlayer else 0 if player == curNode.gamestate.ActivePlayer else .5
        curNode.update(v)
        while curNode.hasParent():
            p = curNode.gamestate.ActivePlayer
            curNode = curNode.parent
            if curNode.gamestate.ActivePlayer != p:
                v = 1-v
            curNode.update(v)

    winner = selectfinalChild(root)
   # for child in root.children:
   #     print(child.move)
   #     print(child.v)

    return winner.move

names = """Arcane Anomaly
Argent Squire
Clockwork Gnome
Flame Imp"""
names = names.splitlines()
where = 1
Board = [[],[],[]]
Hand = [[],[],[]]
Deck = [[],[],[]]
for name in names:
    where *= -1
    Hand[where].append(HSCard.HSCard(name))
Hearthgame = Gamestate.Gamestate(Board,Hand,Deck,[2,2,2])
#for c in Hearthgame.Hand[2]:
#    print(c.Name)
print(Hearthgame.Board)
for i in Hearthgame.Hand:
    for card in i:
        print(card.Attack)
for k in range(20):

    print(Hearthgame.Board)
    print(Hearthgame.Hand)
    move = FindMove(Hearthgame, 1000)
#    print(move)
    simTurn(Hearthgame, move)