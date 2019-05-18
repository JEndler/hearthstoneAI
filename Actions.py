import win32api
import win32con
import win32gui
import time
import random
import math
import numpy
import copy
import os
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename


def bezier(a,b,c,x,lengthx):
    x=x/lengthx
    res = numpy.array([0,0])
    res = (1-x)*(1-x)*a+3*(1-x)*x*b+x*x*c
    return res

def humanmove(xstart,ystart,xend,yend):
    if xstart != ystart and xend != yend:
        start = numpy.array([xstart, ystart])
        end = numpy.array([xend, yend])
        def abs(x):
            if x >= 0:
                return x
            else:
                return -x
        length = math.sqrt(abs(xstart-xend)**2+abs(ystart-yend)**2)
        x = 0
        print(length,"this is length")
        while x<=int(length):
            try:
                win32api.SetCursorPos((int(bezier(start, (start+end)/2+([-1,1]), end, x, length)[0]), int(bezier(start, (start+end)/2+([-1,1]), end, x, length)[1])))
            except:
                pass
            x= x+10
            time.sleep(.03)

#Comment about GetMyString()
#First Digit = [1 = HandCards ; 2 = FriendlyBoard ; 3 = Opposing Board]
#Second Digit = [N = Number of Cards in Hand/ Cards on Board]
#Third Digit = Position from Left to Right

def GetMyString():
    res = ""
    with open("Coordinates.txt") as file:
        for line in file:
            res += line
    return res

def applist(handles=[]):
    def windowcount(hwnd, resultList):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
    mlst=[]
    win32gui.EnumWindows(windowcount, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst

appwindows = applist()

def hearthopen():
    yes = False
    for i in appwindows:
        if "Hearthstone" == i[1]:
            yes = True
    if yes:
        return True
    else:
        return False

def windowfront():
    if hearthopen():

        pass
    else:
        pass


def attack(posattacker, target):
    if hearthopen():
        windowfront()
        win = win32gui.GetWindowRect(win32gui.FindWindow(0, "Hearthstone"))
        x = win[0]
        y = win[1]
        w = win[2] - x
        h = win[3] - y
        wor = 1252-176
        hor = 742- 96
        attackpos = [] #upx,upy,downx,downy
        targetpos = []

        def cor(k,a):
            win = win32gui.GetWindowRect(win32gui.FindWindow(0, "Hearthstone"))
            xii = win[0]
            yii = win[1]
            w = win[2] - xii
            h = win[3] - yii
            wor = 1252 - 176
            hor = 742 - 96
            stretchx = w / wor
            stretchy = h / hor
            if a == "x":
                return int(xii+(k-176)*stretchx)
            if a == "y":
                return int(yii +(k-96)*stretchy)
        for line in GetMyString().splitlines():
            if posattacker in line:
                newline = copy.deepcopy(line)
                open = newline.index("(")
                comma = newline.index(",")
                attackpos.append(newline[open + 1:comma])
                newline = newline[comma + 2:]
                close = newline.index(")")
                attackpos.append(newline[:close])
                newline = newline[close + 3:]
                attackpos.append(newline[:newline.index(",")])
                newline = newline[newline.index(",") + 2:]
                attackpos.append(newline[:newline.index(")")])
            if target in line:
                print("i was here")
                open = line.index("(")
                comma = line.index(",")
                targetpos.append(line[open + 1:comma])
                line = line[comma + 2:]
                close = line.index(")")
                targetpos.append(line[:close])
                line = line[close + 3:]
                targetpos.append(line[:line.index(",")])
                line = line[line.index(",") + 2:]
                targetpos.append(line[:line.index(")")])
        print(attackpos)
        print(targetpos)
        print("target")



        print(cor(int(attackpos[0]),"x"))
        print(cor(int(attackpos[1]),"y"))
        print(cor(int(attackpos[2]),"x"))
        print(cor(int(attackpos[3]),"y"))
        attackx = random.randint((cor(int(attackpos[0]), "x")), cor(int(attackpos[2]), "x"))
        attacky = random.randint(cor(int(attackpos[1]), "y"), cor(int(attackpos[3]), "y"))
        targetx = random.randint(cor(int(targetpos[0]), "x"), cor(int(targetpos[2]), "x"))
        targety = random.randint(cor(int(targetpos[1]), "y"), cor(int(targetpos[3]), "y"))



        humanmove(win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], attackx, attacky)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, attackx, attacky,0,0)
        humanmove(attackx, attacky, targetx, targety)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, targetx, targety, 0,0)
    else:
        #print("Hearthstone is not open")
        pass

def press( target):
    if hearthopen():
        windowfront()
        win = win32gui.GetWindowRect(win32gui.FindWindow(0, "Hearthstone"))
        x = win[0]
        y = win[1]
        w = win[2] - x
        h = win[3] - y
        wor = 1252-176
        hor = 742- 96
        attackpos = [] #upx,upy,downx,downy
        targetpos = []

        def cor(k,a):
            win = win32gui.GetWindowRect(win32gui.FindWindow(0, "Hearthstone"))
            xii = win[0]
            yii = win[1]
            w = win[2] - xii
            h = win[3] - yii
            wor = 1252 - 176
            hor = 742 - 96
            stretchx = w / wor
            stretchy = h / hor
            if a == "x":
                return int(xii+(k-176)*stretchx)
            if a == "y":
                return int(yii +(k-96)*stretchy)
        for line in GetMyString().splitlines():
            if target in line:
                print("i was here")
                open = line.index("(")
                comma = line.index(",")
                targetpos.append(line[open + 1:comma])
                line = line[comma + 2:]
                close = line.index(")")
                targetpos.append(line[:close])
                line = line[close + 3:]
                targetpos.append(line[:line.index(",")])
                line = line[line.index(",") + 2:]
                targetpos.append(line[:line.index(")")])
        print(targetpos)
        print("target")



        print(cor(int(targetpos[0]),"x"))
        print(cor(int(targetpos[1]),"y"))
        targetx = random.randint(cor(int(targetpos[0]), "x"), cor(int(targetpos[2]), "x"))
        targety = random.randint(cor(int(targetpos[1]), "y"), cor(int(targetpos[3]), "y"))



        humanmove(win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], targetx, targety)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, targetx, targety, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, targetx, targety, 0,0)
    else:
        #print("Hearthstone is not open")
        pass


#attack("5 5 5","5 5 5")