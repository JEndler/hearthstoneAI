import json
import numpy


class cards():
    def getJsonFromFile():
        with open("cards.json", mode='r', encoding='utf8') as jsonFile:
            res = json.load(jsonFile)
        return res

    cards = getJsonFromFile()

    def getListofAllCardFromClass(Class):
        res = []
        for card in cards.cards:
            if "cardClass" in card and card["cardClass"] == Class and "collectible" in card and card[
                "collectible"] == True:
                res.append(card["name"])
        return res

    def searchCardbyID(ID):
        for HScard in cards.cards:
            if "dbfId" in HScard and HScard["dbfId"] == ID: return HScard
        return -1

    def getListofAllNeutralCards():
        res = []
        for card in cards.cards:
            if "cardClass" in card and card["cardClass"] == "NEUTRAL" and "collectible" in card and card[
                "collectible"] == True:
                res.append(card["name"])
        return res

    def getListofAllWeapons(self):
        #todo
        pass

    def getListofAllMinions(self):
        #todo
        pass


    def searchname(name):
        for card in cards.cards:
            if "name" in card and card["name"] == name: return card
        return -1

    def mechanicscard(self, name):
        card = cards.searchname(name)
        if card is not -1 and "mechanics" in card: return card["mechanics"]
        return -1

    def statcard(self, name):
        card = cards.searchname(name)
        if card is not -1 and card["type"] == "MINION": return numpy.array([card["attack"], card["health"]])
        return -1

    def costcard(self, name):
        card = cards.searchname(name)
        if card is not -1 and "cost" in card: return card["cost"]
        return -1

    def racecard(self, name):
        card = cards.searchname(name)
        if card is not -1 and "race" in card: return card["race"]
        return -1

    def textcard(self, name):
        card = cards.searchname(name)
        if card is not -1 and "text" in card: return card["text"]
