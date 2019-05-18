import numpy as np
import random
import time
import math
import copy

random.seed(time.time())


class card:
    def __init__(self, attack, health, name):
        self.name = name
        self.attack = attack
        self.health = health
        self.cost = int((attack + health) / 2)
        self.attackable = False

    def getHealth(self):
        return self.health

    def getAttack(self):
        return self.attack

    def getCost(self):
        return self.cost

    def __eq__(self, other):
        if type(other) == card:
            if self.name == other.name:
                if self.attack == other.attack:
                    if self.health == other.health:
                        return True
        return False

    def __repr__(self):
        return "name %s  a: %s, h: %s, cost %s " % (
        str(self.name), str(self.attack), str(self.health), str(self.cost))  # ,str(self.cost),str(self.attackable))

    def __str__(self):
        return [str(self.attack), str(self.health), str(self.cost), str(self.attackable)]


class gamestate:
    def __init__(self):
        self.Hand = [[], [], []]
        self.Deck = [[], [], []]
        self.Board = [[], [], []]
        self.Health = [-1, -1, -1]
        self.ManaCrystals = [-1, -1, -1]
        self.EmptyManaCrystals = [-1, -1, -1]
        self.Gameover = False
        self.activplayer = 1
        self.currentPlayer = 1

    def draw(self, player):
        card = random.choice(self.Deck[player])
        self.Deck[player].remove(card)
        self.Hand[player].append(card)

    def play(self, player, card):
        self.Hand[player].remove(card)
        self.Board[player].append(card)
        self.ManaCrystals[player] -= card.cost

    def attack(self, card1, card2, player1):
        card1.health -= card2.attack
        card2.health -= card2.attack
        if card1.health <= 0:
            self.Board[player1].remove(card1)
        if card2.health <= 0:
            self.Board[player1 * -1].remove(card2)

    def attackhero(self, card, player):
        self.Health[player * -1] -= card
        if self.Health[player * -1] <= 0:
            self.Gameover = True

    def clone(self):
        return copy.deepcopy(self)


# Moves: ["p",card] or ["a",card,(card or hero)]
def listoflegalmoves(gamestate):
    listoflegalmoves = []
    for card in gamestate.Hand[gamestate.currentPlayer]:
        if card.cost <= gamestate.ManaCrystals[gamestate.currentPlayer]:
            listoflegalmoves.append(["p", card])
    for card in gamestate.Board[gamestate.currentPlayer]:
        if card.attackable:
            for enemycard in gamestate.Board[gamestate.currentPlayer * -1]:
                listoflegalmoves.append(["a", card, enemycard])
                # enemychampion
            listoflegalmoves.append(["a", card, gamestate.currentPlayer * -1])
    # no move
    listoflegalmoves.append([])
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
    movecards = move
    if move == []:
        gamestate.currentPlayer *= -1
        gamestate.EmptyManaCrystals[0] += 1
        gamestate.EmptyManaCrystals[1] += 1
        gamestate.EmptyManaCrystals[2] += 1
        gamestate.ManaCrystals = gamestate.EmptyManaCrystals
        for card in gamestate.Board[gamestate.currentPlayer]:
            card.attackable = True
        for card in gamestate.Board[gamestate.currentPlayer * -1]:
            card.attackable = True
    elif move[0] == "p":
        gamestate.ManaCrystals[gamestate.currentPlayer] -= movecards[1].cost
        if len(gamestate.Board[gamestate.currentPlayer]) < 7:
            gamestate.Board[gamestate.currentPlayer].append(movecards[1])
        gamestate.Hand[gamestate.currentPlayer].remove(movecards[1])
    elif move[0] == "a":
        if movecards[2] == 1 or movecards[2] == -1:
            gamestate.Health[movecards[2]] -= movecards[1].attack
        else:
            if movecards[1].health - movecards[2].attack <= 0:
                gamestate.Board[gamestate.currentPlayer].remove(movecards[1])
            if movecards[2].health - movecards[1].attack <= 0:
                gamestate.Board[gamestate.currentPlayer * -1].remove(movecards[2])
            movecards[1].health -= movecards[2].attack
            movecards[2].health -= movecards[1].attack


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

def Move(gamestate, N = 10000):
    root = TreeNode(gamestate)
    for simNumber in range(N):
        curNode = root
        while curNode.hasChild():
            curNode = selectChild(curNode)
        for move in listoflegalmoves(curNode.gamestate):
            nextstate = curNode.gamestate.clone()
            simTurn(nextstate, move)
            tempNode = TreeNode(nextstate)
            tempNode.move = move
            curNode.addChild(tempNode)
        if checkIfRunning(curNode.gamestate):
            curNode = selectChild(curNode)
        player, rounds = simGame(curNode.gamestate)
        v = 1 if player == (-1) * curNode.gamestate.currentPlayer else 0 if player == curNode.gamestate.currentPlayer else .5
        curNode.update(v)
        while curNode.hasParent():
            p = curNode.gamestate.currentPlayer
            curNode = curNode.parent
            if curNode.gamestate.currentPlayer != p:
                v = 1-v
            curNode.update(v)

    winner = selectfinalChild(root)

    return winner.move

t = []
hearthgame = gamestate()
hearthgame.Hand = [[], [], []]
hearthgame.Deck = [[], [], []]
hearthgame.Board = [[], [], []]
hearthgame.Health = [-1, 30, 30]
hearthgame.ManaCrystals = [0, 4, 4]
hearthgame.EmptyManaCrystals = [-1, 4, 4]
hearthgame.Gameover = False
# hearthgame.activplayer = 1
hearthgame.currentPlayer = 1
name = 100
for x in range(5):
    for y in range(6):
        hearthgame.Deck[1].append(card(x+1, y+1, int(name)))
        hearthgame.Deck[-1].append(card(x+1, y+1, int(name) + 1))
        name = name + 2
for z in range(4):
    hearthgame.draw(1)
    hearthgame.draw(-1)
c = card(18,12,666)
c.cost = 4
hearthgame.Hand[1].append(c)
hearthgame.Hand[-1].append(c)

for i in range(10):
    hearthgamenew = copy.deepcopy(hearthgame)
    print(hearthgamenew.Board)
    print(hearthgamenew.Hand)
    c = time.time()
    print(Move(hearthgamenew))
    print(time.time()-1)
    print("g")
print(t)