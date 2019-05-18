import copy
import Gamestate
import HearthSimulation
import HSCard
import Move


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



g = Gamestate.Gamestate()
g.Board = [[],[],[]]
g.Hand = [[],[HSCard.HSCard("Duskboar",0)],[]]
b = copy.deepcopy(g)
root = TreeNode(g)
curNode = copy.deepcopy(root)

nextstate = copy.deepcopy(curNode.gamestate)
move = Move.Move("play",g.Hand[1][0])
print("rootboard")
print(root.gamestate.Board)
print(move)
HearthSimulation.simTurn(nextstate, move)
print("rootboardafterchage")
print(root.gamestate.Board)
tempNode = TreeNode(nextstate)
tempNode.move = move
curNode.addChild(tempNode)