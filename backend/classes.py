import random
import lists
from typing import Union
import flask_socketio


class Player:
    # stores information about an individual player in a game
    def __init__(self, name):
        self.name = name
        self.deck: list[str] = lists.STANDARD_DECK.copy()
        random.shuffle(self.deck)  # upon creation of the user, shuffle the deck
        self.crisis: str = random.choice(lists.CRISIS_DECK)  # server side crisis
        self.hand: list[dict[str, Union[str, bool]]] = []  # server side hand
        self.discard: list[str] = []
        self.field: list[str] = []
        self.storage = {  # just variables for showing appropriate dialogs in frontend
            # below assume discard is from opponent, draw/restore is for you
            "showDialogNormal": False,  # draw 2/restore 1 dialog
            "showDialogDefence": False,  # in discard 2 defences, are you sure dialog (if can only discard 0/1 defences)
            "showOptionDefence": False,  # in discard 2 defences, has not selected any defences
            "selectionDefence": [],  # in discard 2 defences, selection of first defence if any
            "showOptionDefence2": False,  # in discard 2 defences, has only selected 1 defence
            "showOptionField": False,  # in discard 1 field card, has not selected any field cards
            "showDialogField": False,  # in discard 1 field card, are you sure dialog (if cannot discard field cards)
            "showDiscardPlay": False,  # in restore 1 from discard, has not selected a card to restore
            "showOptionHand": False,  # in discard 1 from hand, has not selected a card to discard
            "showDialogHand": False,  # viewing opponent's hand but no option to discard
            "opponentHandTemp": [],  # used when getting opponent's hand
            "discardHand": False,  # in discarding hand phase (at end of turn)
            "canClickEndTurn": True, # normally true, set to false when not your turn. also set to false upon game ending
            "index": -1  # card index selected, to store which card was clicked on to pull up a dialog/options
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
        # this function ensures that upon turn switch,
        # the player whose turn it is, can play cards
        # the player whose turn just ended, cannot play cards
        handcopy = self.hand.copy()
        for i in handcopy:
            i["enablePlay"] = status
        self.hand = handcopy
        return self.hand

    def addHandCard(self, cardName):
        self.hand.append({"name": cardName, "enablePlay": True,  # "blockPlay": False, # can play card without effect
                          # these will be set later (refer up for meanings)
                          # requires prefix just means it sets the corresponding variable in backend

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
    # like an account, in the future will be used to store stats
    def __init__(self, name, last_checkin, login_session_key):
        self.name: str = name
        self.last_checkin: float = last_checkin
        self.login_session_key: str = login_session_key
        self.games: list[str] = []

    def __str__(self):
        return self.name + " | " + str(self.last_checkin)
