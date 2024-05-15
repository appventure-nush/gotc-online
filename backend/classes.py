import random
import lists
from typing import Union
import flask_socketio


class Player:
    def __init__(self, name):
        self.name = name
        self.deck: list[str] = lists.STANDARD_DECK.copy()
        random.shuffle(self.deck)  # upon creation of the user, shuffle the deck
        self.crisis: str = random.choice(lists.CRISIS_DECK)  # server side crisis
        self.hand: list[dict[str, Union[str, bool]]] = []  # server side hand
        self.discard: list[str] = []
        self.field: list[str] = []
        self.storage = {
            "showDialogNormal": False,
            "showDialogDefence": False,
            "showOptionDefence": False,
            "selectionDefence": [],
            "showOptionDefence2": False,
            "showOptionField": False,
            "showDialogField": False,
            "showDiscardPlay": False,
            "showOptionHand": False,
            "showDialogHand": False,
            "opponentHandTemp": [],
            "discardHand": False,
            "canClickEndTurn": True,
            "index": -1
        }

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def popDeck(self):
        return self.deck.pop()

    def newDeck(self):
        self.deck = lists.STANDARD_DECK.copy()
        self.discard = []
        self.hand = []
        random.shuffle(self.deck)

    def newCrisis(self):
        self.crisis = random.choice(lists.CRISIS_DECK)
        return self.crisis

    def setHandEnablePlayStatus(self, status: bool):
        handcopy = self.hand.copy()
        for i in handcopy:
            i["enablePlay"] = status
        self.hand = handcopy
        return self.hand

    def addHandCard(self, cardName):
        self.hand.append({"name": cardName, "enablePlay": True,  # "blockPlay": False, # can play card without effect
                          # these will be set later
                          # everywhere that could affect this (e.g. draw card) will be accompanied by a recompute call
                          # we just cannot call it here because this is Player not Game
                          "requiresDialogNormal": False, "requiresOptionDefence": False,
                          "requiresOptionField": False, "requiresDialogHand": False,
                          "requiresOptionHand": False})
        return self.hand

    def defenceCheck(self):
        # check defences
        # will return a string like "CDEMPS" where a letter appears if it is in the field
        # and does not appear if it is not
        # ignores community support
        return "".join(list(sorted(set([i[0].upper() for i in self.field if i != "communitysupport"]))))

    def gameDefenceFulfilled(self):
        if self.defenceCheck() == "CDEMPS":
            return 5
        elif self.crisis == "crisis-1":
            return len(self.defenceCheck().replace("M", ""))
        elif self.crisis == "crisis-2":
            return len(self.defenceCheck().replace("C", ""))
        elif self.crisis == "crisis-3":
            return len(self.defenceCheck().replace("E", ""))
        elif self.crisis == "crisis-4":
            return len(self.defenceCheck().replace("S", ""))
        elif self.crisis == "crisis-5":
            return len(self.defenceCheck().replace("P", ""))
        elif self.crisis == "crisis-6":
            return len(self.defenceCheck().replace("D", ""))

    def gameWon(self):
        return self.gameDefenceFulfilled() == 5




class User:
    def __init__(self, name, last_checkin, login_session_key):
        self.name: str = name
        self.last_checkin: float = last_checkin
        self.login_session_key: str = login_session_key
        self.games: list[str] = []

    def __str__(self):
        return self.name + " | " + str(self.last_checkin)
