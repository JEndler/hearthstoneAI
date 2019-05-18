#import Actions
import time

class Move:
    def __init__(self,type,actioncard=None,targetcard=None, extratarget = None):
        #List of Possible moves:
        #End  ==  end
        #-Play Minion  == play
        #-Play Spell  ==  playspell
        #Play targeted Spell
        #    -target is friendly  ==  friendlytargetspell
        #-Play and Choose one z.B. Jade Idol  ==  playchoose
        #-Play and Choose one targeted z.B. Keeper of the Grove/Wrath  ==  playchoosetarget
        #-Attack  ==  attack
        #-Hero Power == heropower

        self.type = type
        self.actioncard = actioncard
        self.extratarget = extratarget
        self.target = targetcard


    def __str__(self):
        return self.type+"--"+str(self.actioncard)+"--"+str(self.target)

    def __repr__(self):
        return self.type + "--" + str(self.actioncard) + "--" + str(self.target)

    def Execute(self,gamestate,player):
        #todo (check first) type was a,p instead of attack,play if not change yet change
        if self.type == "attack":
            atpos = "2 "+ str(len(gamestate.Board[player])) + " " + str(self.actioncard.Pos+1)
            if self.target == 1:
                tarpos = "4 4 1"
            elif self.target == -1:
                tarpos = "4 4 2"
            else:
                tarpos = "3 "+ str(len(gamestate.Board[player*-1])) + " " + str(self.target.Pos)
            print("--------")
            print(atpos)
            print(tarpos)
            print("------------")
            Actions.attack(atpos,tarpos)
        if self.type == "play":
            print(self.actioncard.Pos)
            print(len(gamestate.Hand[player]))
            atpos = "1 " + str(len(gamestate.Hand[player])) + " " + str(self.actioncard.Pos+1)
            tarpos = "3 2 2" #todo change to random
            print("--------")
            print(atpos)
            print(tarpos)
            print("------------")
            print(atpos)
            print(tarpos)
            Actions.attack(atpos, tarpos)
        if self.type == "end":
            Actions.press("5 5 5")

        if self.type == "heropower":
            Actions.press("4 4 3")
