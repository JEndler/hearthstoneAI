from tkinter import *
import tkinter.ttk as ttk

def displayTree(treeData):
    root = Tk()
    tree = ttk.Treeview(root)
    tree["columns"]=("Data")
    tree.column("Data", width=3000)
    tree.heading("Data", text="Data")

    rootEntry = tree.insert("" , 0, text="Root", values=str(treeData))

    def insertNodes(curNode, prevNodeEntry, i):
        curNodeEntry = tree.insert(prevNodeEntry, i, values = "p=%d(%d/%d)" % (curNode.gamestate.ActivePlayer, curNode.v, curNode.NumGames),text = "Move %s, Board %s , Hand %s, Mana %s, Health %s" % (str(curNode.move) , curNode.gamestate.Board, [[x.Cost for x in curNode.gamestate.Hand[1]],[x.Cost for x in curNode.gamestate.Hand[2]]], curNode.gamestate.ManaCrystals,curNode.gamestate.Health))
        i = 0
        for child in curNode.children:
            insertNodes(child, curNodeEntry, i)
            i += 1

    insertNodes(treeData, "", 0)

    #id2 = tree.insert("", 1, "dir2", text="Dir 2")
    #tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

    ##alternatively:
    #tree.insert("", 3, "dir3", text="Dir 3")
    #tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

    tree.pack()
    root.mainloop()