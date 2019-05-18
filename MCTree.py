import numpy as np
import random
import time
import math
import copy
import HearthSimulation as Sim
import Move
import drawtree
import Gamestate
import numpy
 
random.seed(time.time())
 
 
class TreeNode:
    def __init__(self, gamestate):
        self.parent = None
        self.children = []
        self.NumGames = 0
        self.gamestate = gamestate
        self.move = Move.Move("start")
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
        20*math.log(Node.parent.NumGames) / (1. * Node.NumGames)) if Node.NumGames > 0 else 99999999
 
 
def selectChild(RNode):
    i = -999999
    theWinner = None
    for child in RNode.children:
        if calcUCB1(child) >= i:
            theWinner = child
            i = calcUCB1(child)
    return theWinner
 
 
def selectfinalChild(RNode):
    i = -99999
    theWinner = None
    for child in RNode.children:
        if child.NumGames+child.v > i:
            theWinner = child
            i = child.NumGames+child.v
    return theWinner
 
 
def printg(g):
    print(g.Hand)
    print([x.Cost for x in g.Hand[1]] + [x.Cost for x in g.Hand[2]])
    print([x.canAttack for x in g.Hand[1]] + [x.canAttack for x in g.Hand[2]])
    print(g.Board)
    print(g.Deck)
    print(g.Health)
    print(g.ManaCrystals)
    print(g.ActivePlayer)
    print("________________________________")
 
 
def FindMoveOne(gamestate, N=200, prnt = False ):
    if prnt == True:
        printg(gamestate)
    start_time = time.time()
    g = copy.deepcopy(gamestate)
    if len(Sim.listoflegalmoves(g)) == 1:
        return Sim.listoflegalmoves(g)[0]
    root = TreeNode(gamestate)
 
    for simNumber in range(N):
        curNode = root
 
        while curNode.hasChild():
            #print(curNode.children)
            curNode = selectChild(curNode)
 
        for move in Sim.listoflegalmoves(curNode.gamestate):
            nextstate = curNode.gamestate.deepcopystate()
            # printg(nextstate)
            Sim.simTurn(nextstate, move)
            # print(move)
            # printg(nextstate)
            tempNode = TreeNode(nextstate)
            tempNode.move = move
            curNode.addChild(tempNode)
 
        if Sim.checkIfRunning(curNode.gamestate):
            curNode = selectChild(curNode)
 
        player, rounds, Health , Boardstat , HandCards = Sim.simGame(curNode.gamestate)
 
        newval = player#*curNode.gamestate.ActivePlayer#*(1/rounds)*(Health/30)*-1
 
        if curNode.move.type == "end":
            curNode.update((newval * curNode.gamestate.ActivePlayer+1)/2)
        else:
            curNode.update((-1*newval*curNode.gamestate.ActivePlayer+1)/2)
        #print(1-v)
        #print()
        while curNode.hasParent():
            curNode = curNode.parent
 
            if curNode.move.type == "end":
                curNode.update((newval * curNode.gamestate.ActivePlayer + 1) / 2)
 
            else:
                curNode.update((-1*newval * curNode.gamestate.ActivePlayer + 1) / 2)
 
        if prnt == True:
            if simNumber % 50 == 0:
                print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                for child in root.children:
                    print()
                    print(child.move)
                    print("Value")
                    print(child.v)
                    print("NumGames")
                    print(child.NumGames)
                    print(calcUCB1(child))
                    print()
                print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
 
    winner = selectfinalChild(root)
 
    Endlerlist = []
 
    for child in root.children:
        listt = [child.move,child.v,child.NumGames]
        if prnt == True:
            print(child.move)
            print(child.v)
            #print(Sim.simGame(child.gamestate))
            print(child.NumGames)
        Endlerlist.append(listt)
    if prnt == True:
        drawtree.displayTree(root)
        print("This took", time.time() - start_time, "to run")
    return winner.move
 
 
 
 
 
 
 
def RandomMove(gamestate):
    leg = Sim.listoflegalmoves(gamestate)
    move = random.choice(leg)
    return move