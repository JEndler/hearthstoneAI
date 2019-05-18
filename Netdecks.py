#This file handles the Downloading of Netdecks to predict furure Cards
import bs4
import HSCard
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
globaldecks = [[[]], [[]], [[]], [[]], [[]], [[]], [[]], [[]], [[]]]
# 1 = DRUID ; 2 = PALADIN ; 3 = WARLOCK ; 4 = WARRIOR ; 5 = PRIEST ; 6 =
# SHAMAN ; 7 = ROGUE ; 8 = HUNTER ; 9 = MAGE

# LINKS TO DECKS
DRUID_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=4"
PALADIN_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=32"
WARLOCK_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=512"
WARRIOR_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=1024"
PRIEST_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=64"
SHAMAN_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=256"
ROGUE_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=128"
HUNTER_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=8"
MAGE_DECKS_URL = "http://www.hearthpwn.com/decks?filter-is-forge=2&filter-unreleased-cards=f&filter-deck-tag=1&filter-class=16"
LinkList = []
LinkList.extend((DRUID_DECKS_URL, PALADIN_DECKS_URL, WARLOCK_DECKS_URL, WARRIOR_DECKS_URL, PRIEST_DECKS_URL, SHAMAN_DECKS_URL, ROGUE_DECKS_URL, HUNTER_DECKS_URL, MAGE_DECKS_URL))


#TODO REMOVE ;AMP FROM LINK
def getLinkToNextPage(hearthpwn_url):
	page_soup = getRawData(hearthpwn_url)
	next_page_list = page_soup.findAll("a", {"href": True})
	href = ""
	for link in next_page_list:
		if 'rel="next"' in str(link):
			href+=str(link)
	splitstring = href.split("\"");
	# return ("http://www.hearthpwn.com" + splitstring[3])
	x = "http://www.hearthpwn.com" + splitstring[3].replace('amp;','')
	return x
	# with open("link.txt", "w") as file:
	# 	for string in splitstring:
	# 		file.writelines(x)

def getRawDataOfDecks(url_list):
	class_list = []
	index = 0
	for deck_url in url_list:
		page_soup = getRawData(deck_url)
		decks = findDeckLinks(page_soup)
		for deck in decks:
			decklists = []
			globaldecks[index].append(getDeckList(deck))
		index+=1

#One Page contains 25 Decks
def getDecks(numberOfPagesPerClass):
	index = 0
	for hero in globaldecks:
		url_list = findDeckLinks(getRawData(LinkList[index]))
		next_url = getLinkToNextPage(LinkList[index])
		for i in range(numberOfPagesPerClass):
			url_list.extend(findDeckLinks(getRawData(next_url)))
			next_url = getLinkToNextPage(next_url)
		for url in url_list:
			decklist = []
			decklist.extend(getDeckList(url))
			globaldecks[index].append(decklist)
		index+=1


def getRawData(url):

    # User Agent Mozilla to Circumvent Security Blocking
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Connect and Save the HTML Page
    uClient = urlopen(req)
    page_html = uClient.read()
    uClient.close()

    # Parse HTML
    page_soup = soup(page_html, "html.parser")
    return page_soup


def findDeckLinks(page_soup):
    deck_link_list = []
    listing_Body = page_soup.findAll("div", {"class": "listing-body"})
    result = []
    for body in listing_Body:
    	result.extend(body.findAll("a", {'href': True}))
    for link in result:
        href = str(link['href'])
        if "/decks/" in href:
            deck_link_list.append("http://www.hearthpwn.com" + href)
    return deck_link_list


def getDeckList(url):
    res = []
    hero = None
    page_soup = getRawData(url)
    # page_soup_string = str(page_soup)
    # with open("page_html.txt","w") as file:
    # 	file.write(page_soup_string)
    for class_soup in page_soup.findAll("span", {"class": True}):
        if "class" in class_soup["class"]:
            hero = str(class_soup["class"])[17:23]
    page_soup = page_soup.find("aside", {"class": "infobox p-base p-base-a"})
    for href in page_soup.findAll("a", {"href": True}):
        if "Name" not in href.string and "Cost" not in href.string and "data-count" in href:
            print(href.string + "  x" + href["data-count"])
            for i in range(int(href["data-count"])):
                res.append(href.string)
    return res                


# DruidLinklist = findDeckLinks(getRawData(DRUID_DECKS_URL))
# print(DruidLinklist)
# Decklist = getDeckList(DruidLinklist[5])
# print(Decklist)
#page_html= getRawData(findDeckLinks(getRawData(DRUID_DECKS_URL))[0])

def doStuff():
    for DeckLink in findDeckLinks(getRawData(LinkList[0])): #DRUID
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "DRUID")
    for DeckLink in findDeckLinks(getRawData(LinkList[1])): #PALADIN
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "PALADIN")
    for DeckLink in findDeckLinks(getRawData(LinkList[2])): #WARLOCK
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "WARLOCK")
    for DeckLink in findDeckLinks(getRawData(LinkList[3])): #WARRIOR
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "WARRIOR")
    for DeckLink in findDeckLinks(getRawData(LinkList[4])): #PRIEST
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "PRIEST")
    for DeckLink in findDeckLinks(getRawData(LinkList[5])): #SHAMAN
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "SHAMAN")
    for DeckLink in findDeckLinks(getRawData(LinkList[6])): #ROGUE
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "ROGUE")
    for DeckLink in findDeckLinks(getRawData(LinkList[7])): #HUNTER
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "HUNTER")
    for DeckLink in findDeckLinks(getRawData(LinkList[8])): #MAGE
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "MAGE")

    #NEXT PAGES
    
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[0]))): #DRUID
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "DRUID")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[1]))): #PALADIN
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "PALADIN")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[2]))): #WARLOCK
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "WARLOCK")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[3]))): #WARRIOR
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "WARRIOR")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[4]))): #PRIEST
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "PRIEST")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[5]))): #SHAMAN
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "SHAMAN")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[6]))): #ROGUE
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "ROGUE")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[7]))): #HUNTER
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "HUNTER")
    for DeckLink in findDeckLinks(getRawData(getLinkToNextPage(LinkList[8]))): #MAGE
        saveDeckListToFileFromLink(getRawData(DeckLink), currentClass = "MAGE")                                    

def saveDeckListToFileFromLink(page_html, currentClass):
    cardlist = page_html.findAll("a", {"data-id": True})
    decklist = []
    for item in cardlist:
        for i in range(int(item["data-count"])):
            #print(str(item.getText()))
            cardname = str(item.getText())
            linelist = cardname.splitlines()
            #print(str(linelist[1])[5:] + "|")
            decklist.append(str(linelist[1])[5:] + "|")
    decklist.append("\n")
    with open("Decks\_" + str(currentClass) + "\decks.txt", "a") as file:
        file.writelines(decklist)


doStuff()