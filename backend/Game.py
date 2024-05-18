import flask

from classes import *
from typing import Literal


class Game:
    # the main game class, contains variables for the entire game
    def __init__(self, player1_username, player2_username, internal_id):
        self.player1 = Player(player1_username)
        self.player2 = Player(player2_username)
        while self.player1.crisis == self.player2.crisis:
            # crises cannot be equal
            self.player1 = Player(player1_username)
            self.player2 = Player(player2_username)
        self.player1_username = player1_username
        self.player2_username = player2_username
        # higher crisis number goes first
        self.gofirst = self.player1_username if self.player1.crisis > self.player2.crisis else self.player2_username
        self.turn = self.gofirst  # whose turn is it
        self.nextturnislast = False  # used for running out of deck cards logic, whether next turn played will be last

        self.internal_id = internal_id  # game uuid

    def recomputeBlockAndDialogStatus(self):
        # this is where all the dialogs and options are set, to ensure they show up in the frontend
        # for meanings of the dialogs and options, see classes.py
        # the extra attribute "warn" is the warning that will be shown in the move notifier

        # do the logic for player 1
        handcopy = self.player1.hand.copy()
        for i in handcopy:
            # [1 CSC:] Draw 2 additional cards OR Take any card from your discard pile and place it back into your hand
            if i["name"] in ("military-2", "military-3", "civil-2", "economic-3", "economic-4"):
                i["requiresDialogNormal"] = self.player1.field.count("communitysupport") >= 1
                if len(self.player1.discard) == 0:
                    i[
                        "warn"] = "\nWarning: There are no cards in your discard pile. Picking the second option will have no effect."
                else:
                    i["warn"] = ""  # no warning for playing def card without effect as it could be helpful
                    # for example to win the game
            # If your opponent has 1 or less Community Support points, discard any 2 Defence cards from your opponent's field
            if i["name"] in ("event-5", "event-6", "event-7", "event-8"):
                i["requiresOptionDefence"] = True
                if self.player2.field.count("communitysupport") <= 1 and (
                        len(self.player2.field) - self.player2.field.count("communitysupport") >= 2
                ):
                    i["warn"] = ""
                elif self.player1.field.count("communitysupport") <= 1 and (
                        len(self.player2.field) - self.player2.field.count("communitysupport") == 1
                ):
                    i["warn"] = "\nWarning: Opponent has only 1 defence card to select."
                elif self.player1.field.count("communitysupport") <= 1 and (
                        len(self.player2.field) - self.player2.field.count("communitysupport") == 0
                ):
                    i["warn"] = "\nWarning: Opponent has no defence cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >1 community support. This card will have no effect."
            # If your opponent has 2 or less Community Support points, discard any 1 card from your opponent's field
            if i["name"] in ("event-9", "event-10", "event-11", "event-12"):
                i["requiresOptionField"] = True
                if self.player2.field.count("communitysupport") <= 2 and len(self.player2.field) >= 1:
                    i["warn"] = ""
                elif self.player2.field.count("communitysupport") <= 2 and len(self.player2.field) == 0:
                    i["warn"] = "\nWarning: Opponent has no field cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >2 community support. This card will have no effect."
            # If your opponent has no Community Support points, look at your opponent's hand and discard 1 card from there
            if i["name"] in ("event-1", "event-3", "event-2", "event-4"):
                i["requiresOptionHand"] = True
                if len(self.player2.hand) > 0 and self.player2.field.count("communitysupport") == 0:
                    i["warn"] = ""
                elif len(self.player2.hand) == 0 and self.player2.field.count("communitysupport") == 0:
                    i["warn"] = "\nWarning: Opponent has no hand cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >0 community support. This card will have no effect!"
            # Look at the cards in your opponent's hand. [2 CSC:] Draw 1 additional card AND play 1 additional card this turn
            if i["name"] in ("military-4", "civil-3", "economic-5", "social-3", "psychological-3", "digital-3"):
                i["requiresDialogHand"] = True

        self.player1.hand = handcopy

        # then for player 2
        handcopy = self.player2.hand.copy()
        for i in handcopy:
            # [1 CSC:] Draw 2 additional cards OR Take any card from your discard pile and place it back into your hand
            if i["name"] in ("military-2", "military-3", "civil-2", "economic-3", "economic-4"):
                i["requiresDialogNormal"] = self.player2.field.count("communitysupport") >= 1
                if len(self.player2.discard) == 0:
                    i[
                        "warn"] = "\nWarning: There are no cards in your discard pile. Picking the second option will have no effect."
                else:
                    i["warn"] = ""  # no warning for playing def card without effect as it could be helpful
                    # for example to win the game
            # If your opponent has 1 or less Community Support points, discard any 2 Defence cards from your opponent's field
            if i["name"] in ("event-5", "event-6", "event-7", "event-8"):
                i["requiresOptionDefence"] = True
                if self.player1.field.count("communitysupport") <= 1 and (
                        len(self.player1.field) - self.player1.field.count("communitysupport") >= 2
                ):
                    i["warn"] = ""
                elif self.player1.field.count("communitysupport") <= 1 and (
                        len(self.player1.field) - self.player1.field.count("communitysupport") == 1
                ):
                    i["warn"] = "\nWarning: Opponent has only 1 defence card to select."
                elif self.player1.field.count("communitysupport") <= 1 and (
                        len(self.player1.field) - self.player1.field.count("communitysupport") == 0
                ):
                    i["warn"] = "\nWarning: Opponent has no defence cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >1 community support. This card will have no effect."
            # If your opponent has 2 or less Community Support points, discard any 1 card from your opponent's field
            if i["name"] in ("event-9", "event-10", "event-11", "event-12"):
                i["requiresOptionField"] = True
                if self.player1.field.count("communitysupport") <= 2 and len(self.player1.field) >= 1:
                    i["warn"] = ""
                elif self.player1.field.count("communitysupport") <= 2 and len(self.player1.field) == 0:
                    i["warn"] = "\nWarning: Opponent has no field cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >2 community support. This card will have no effect."
            # If your opponent has no Community Support points, look at your opponent's hand and discard 1 card from there
            if i["name"] in ("event-1", "event-3", "event-2", "event-4"):
                i["requiresOptionHand"] = True
                if len(self.player1.hand) > 0 and self.player1.field.count("communitysupport") == 0:
                    i["warn"] = ""
                elif len(self.player1.hand) == 0 and self.player1.field.count("communitysupport") == 0:
                    i["warn"] = "\nWarning: Opponent has no hand cards to select. This card will have no effect."
                else:
                    i["warn"] = "\nWarning: Opponent has >0 community support. This card will have no effect!"
            # Look at the cards in your opponent's hand. [2 CSC:] Draw 1 additional card AND play 1 additional card this turn
            if i["name"] in ("military-4", "civil-3", "economic-5", "social-3", "psychological-3", "digital-3"):
                i["requiresDialogHand"] = True

        self.player2.hand = handcopy
        return self.player1.hand, self.player2.hand

    def game_init(self, socket_obj: flask_socketio.SocketIO, username: str):
        # starts off the game upon entering GameArea, initialises the players in the frontend
        if self.player1_username == username or self.player2_username == username:
            # you are a player in the current game
            returned = {}
            if self.player1.crisis > self.player2.crisis and self.player1_username == username:
                # start by assuming game was resumed, if that is found to be not true in len(deck)==46,
                # reinitialise notifier
                notifier = f"Resumed game against {self.player2_username}."
                if len(self.player1.deck) == 46:  # fresh game, should initialise
                    for q in range(5):
                        self.player1.addHandCard(self.player1.popDeck())
                    self.player1.setHandEnablePlayStatus(True)
                    self.recomputeBlockAndDialogStatus()
                    notifier = f"Started game against {self.player2_username}.\n" \
                               f"Your crisis has the higher number. You are going first. " \
                               f"Drew {lists.LOOKUP[self.player1.hand[-1]['name']]}."
                    returned["canClickEndTurn"] = True  # override value in storage
                returned |= {"username": username,
                             "hand": self.player1.hand,
                             "cardsLeft": len(self.player1.deck),
                             "field": self.player1.field,
                             "discard": self.player1.discard,
                             "crisis": self.player1.crisis,
                             "moveNotifier": notifier,
                             "uuid": self.internal_id,
                             "storage": self.player1.storage}
                socket_obj.emit("update your state", returned)
                socket_obj.emit("update opponent state", {"username": self.player2_username,
                                                          "cardsLeft": len(self.player1.deck),
                                                          "field": self.player1.field,
                                                          "discard": self.player1.discard,
                                                          "crisis": self.player1.crisis,
                                                          "opponentSideUsername": self.player1_username,
                                                          "uuid": self.internal_id})
                return "First"
            elif self.player1.crisis < self.player2.crisis and self.player1_username == username:
                notifier = f"Resumed game against {self.player2_username}."
                if len(self.player1.deck) == 46:  # fresh game, should initialise
                    for q in range(5):
                        self.player1.addHandCard(self.player1.popDeck())
                    self.player1.setHandEnablePlayStatus(False)
                    self.recomputeBlockAndDialogStatus()
                    notifier = f"Started game against {self.player2_username}.\n" \
                               f"Your crisis has the lower number. You are going second."
                    returned["canClickEndTurn"] = False  # override value in storage
                returned |= {"username": username,
                            "hand": self.player1.hand,
                            "cardsLeft": len(self.player1.deck),
                            "field": self.player1.field,
                            "discard": self.player1.discard,
                            "crisis": self.player1.crisis,
                            "moveNotifier": notifier,
                            "uuid": self.internal_id,
                            "storage": self.player1.storage}
                socket_obj.emit("update your state", returned)
                socket_obj.emit("update opponent state", {"username": self.player2_username,
                                                          "cardsLeft": len(self.player1.deck),
                                                          "field": self.player1.field,
                                                          "discard": self.player1.discard,
                                                          "crisis": self.player1.crisis,
                                                          "opponentSideUsername": self.player1_username,
                                                          "uuid": self.internal_id})
                return "Second"
            elif self.player1.crisis > self.player2.crisis and self.player2_username == username:
                notifier = f"Resumed game against {self.player1_username}."
                if len(self.player2.deck) == 46:  # fresh game, should initialise
                    for q in range(5):
                        self.player2.addHandCard(self.player2.popDeck())
                    self.player2.setHandEnablePlayStatus(False)
                    self.recomputeBlockAndDialogStatus()
                    notifier = f"Started game against {self.player1_username}.\n" \
                               f"Your crisis has the lower number. You are going second."
                    returned["canClickEndTurn"] = False  # override value in storage
                returned |= {"username": username,
                             "hand": self.player2.hand,
                             "cardsLeft": len(self.player2.deck),
                             "field": self.player2.field,
                             "discard": self.player2.discard,
                             "crisis": self.player2.crisis,
                             "moveNotifier": notifier,
                             "uuid": self.internal_id,
                             "storage": self.player2.storage}
                socket_obj.emit("update your state", returned)
                socket_obj.emit("update opponent state", {"username": self.player1_username,
                                                          "cardsLeft": len(self.player2.deck),
                                                          "field": self.player2.field,
                                                          "discard": self.player2.discard,
                                                          "crisis": self.player2.crisis,
                                                          "opponentSideUsername": self.player2_username,
                                                          "uuid": self.internal_id})
                return "Second"
            else:  # player 2 crisis bigger and you are player 2
                notifier = f"Resumed game against {self.player1_username}."
                if len(self.player2.deck) == 46:  # fresh game, should initialise
                    for q in range(5):
                        self.player2.addHandCard(self.player2.popDeck())
                    self.player2.setHandEnablePlayStatus(True)
                    self.recomputeBlockAndDialogStatus()
                    notifier = f"Started game against {self.player1_username}.\n" \
                               f"Your crisis has the higher number. You are going first. " \
                               f"Drew {lists.LOOKUP[self.player2.hand[-1]['name']]}."
                    returned["canClickEndTurn"] = True  # override value in storage
                returned |= {"username": username,
                             "hand": self.player2.hand,
                             "cardsLeft": len(self.player2.deck),
                             "field": self.player2.field,
                             "discard": self.player2.discard,
                             "crisis": self.player2.crisis,
                             "moveNotifier": notifier,
                             "uuid": self.internal_id,
                             "storage": self.player2.storage}
                socket_obj.emit("update your state", returned)
                socket_obj.emit("update opponent state", {"username": self.player1_username,
                                                          "cardsLeft": len(self.player2.deck),
                                                          "field": self.player2.field,
                                                          "discard": self.player2.discard,
                                                          "crisis": self.player2.crisis,
                                                          "opponentSideUsername": self.player2_username,
                                                          "uuid": self.internal_id})
                return "First"
        else:
            # you are a spectator
            # todo: spectator mode
            return "Not Playing"

    def pass_turn(self, socket_obj: flask_socketio.SocketIO, povplayer: Literal[1, 2]):
        # passes turn, activated by clicking on draw pile
        # just switch turn to next player, with moving to discard phase if necessary
        response = {
            "hand": [],
            "discard": [],
            "cardsLeft": 0,
            "nextTurn": False,  # tracks if in discarding phase (False) or can already switch turn (True)
            "winThisTurn": False  # someone won this turn, end game in frontend
        }

        curr_player: Player
        other_player: Player
        curr_player, other_player = (self.player1, self.player2) if (povplayer == 1) else (self.player2, self.player1)

        next_turn = len(curr_player.hand) > 7

        if next_turn:
            your_move_notifier = "Please discard cards until you have 7 cards."
            opponent_move_notifier = "Waiting for opponent to discard hand cards."
        else:
            if self.nextturnislast:
                # this turn was the last turn, so trigger game ending calculation
                if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                else:
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                response["winThisTurn"] = True
            elif len(curr_player.deck) == 0:
                # current player ran out of cards, run appropriate logic
                if self.gofirst == curr_player.name:
                    # award extra turn
                    self.nextturnislast = True
                    your_move_notifier = "Warning: Your opponent's next turn is the last turn, due to your deck running out of cards."
                    opponent_move_notifier = "Warning: Your opponent's next turn is the last, due to their deck running out of cards."
                else:
                    # end game and compute winner
                    if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                        your_move_notifier = "Your deck ran out of cards. You win due to having more defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. You lose due to having less defence fulfilled!"
                    elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                        your_move_notifier = "Your deck ran out of cards. Tie due to having equal defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. Tie due to having equal defence fulfilled!"
                    else:
                        your_move_notifier = "Your deck ran out of cards. You lose due to having less defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. You win due to having more defence fulfilled!"
                    response["winThisTurn"] = True
            else:
                # move to next turn
                poppedCard = other_player.popDeck()
                other_player.addHandCard(poppedCard)  # add the popped card to the hand

                other_player.setHandEnablePlayStatus(True)
                curr_player.setHandEnablePlayStatus(False)
                self.recomputeBlockAndDialogStatus()
                self.turn = other_player.name

                your_move_notifier = "Opponent's turn."
                opponent_move_notifier = f"Your turn. You drew {lists.LOOKUP[poppedCard]}."

            response["nextTurn"] = True

        # update both player's displays

        response["hand"] = curr_player.hand
        response["discard"] = curr_player.discard
        response["cardsLeft"] = len(curr_player.deck)
        response["field"] = curr_player.field
        response["moveNotifier"] = your_move_notifier
        response["canClickEndTurn"] = curr_player.name == self.turn

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": curr_player.hand, "discard": curr_player.discard,
                   "cardsLeft": len(curr_player.deck), "field": curr_player.field,
                   "moveNotifier": opponent_move_notifier}
        socket_obj.emit("update opponent state", updater)

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field,
                   "canClickEndTurn": other_player.name == self.turn}
        socket_obj.emit("update your state", updater)

        updater = {"uuid": self.internal_id, "username": curr_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field}
        socket_obj.emit("update opponent state", updater)

        return response

    def discard_hand(self, socket_obj: flask_socketio.SocketIO, povplayer: Literal[1, 2], hand_index: int):
        # in the discarding phase, this function is called
        response = {
            "cardPlayed": "",
            "hand": [],
            "discard": [],
            "cardsLeft": 0,
            "nextTurn": False,  # tracks if in discarding phase (False) or can already switch turn (True)
            "winThisTurn": False  # someone won this turn, end game in frontend
        }

        curr_player: Player
        other_player: Player
        curr_player, other_player = (self.player1, self.player2) if (povplayer == 1) else (self.player2, self.player1)

        cardPlayed = curr_player.hand.pop(hand_index)["name"]
        curr_player.discard = [cardPlayed] + curr_player.discard

        next_turn = len(curr_player.hand) > 7

        if next_turn:
            your_move_notifier = "Please discard cards until you have 7 cards."
            opponent_move_notifier = "Waiting for opponent to discard hand cards."
        else:
            if self.nextturnislast:
                # this turn was the last turn, so trigger game ending calculation
                if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                else:  # player 2 more than player 1
                    your_move_notifier = "Opponent's deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                    opponent_move_notifier = "Your deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                response["winThisTurn"] = True
            elif len(curr_player.deck) == 0:
                # current player ran out of cards, run appropriate logic
                if self.gofirst == curr_player.name:
                    # award extra turn
                    self.nextturnislast = True
                    your_move_notifier = "Warning: Your opponent's next turn is the last turn, due to your deck running out of cards."
                    opponent_move_notifier = "Warning: Your opponent's next turn is the last, due to their deck running out of cards."
                else:
                    # end game and compute winner
                    if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                        your_move_notifier = "Your deck ran out of cards. You win due to having more defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. You lose due to having less defence fulfilled!"
                    elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                        your_move_notifier = "Your deck ran out of cards. Tie due to having equal defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. Tie due to having equal defence fulfilled!"
                    else:  # player 2 more than player 1
                        your_move_notifier = "Your deck ran out of cards. You lose due to having less defence fulfilled!"
                        opponent_move_notifier = "Opponent's deck ran out of cards. You win due to having more defence fulfilled!"
                    response["winThisTurn"] = True
            else:
                # move to next turn
                poppedCard = other_player.popDeck()
                other_player.addHandCard(poppedCard)  # add the popped card to the hand

                other_player.setHandEnablePlayStatus(True)
                curr_player.setHandEnablePlayStatus(False)
                self.recomputeBlockAndDialogStatus()
                self.turn = other_player.name

                your_move_notifier = "Opponent's turn."
                opponent_move_notifier = f"Your turn. You drew {lists.LOOKUP[poppedCard]}."

                response["nextTurn"] = True

        # update both player's displays

        response["hand"] = curr_player.hand
        response["discard"] = curr_player.discard
        response["cardsLeft"] = len(curr_player.deck)
        response["cardPlayed"] = cardPlayed
        response["field"] = curr_player.field
        response["moveNotifier"] = your_move_notifier
        response["canClickEndTurn"] = curr_player.name == self.turn

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": curr_player.hand, "discard": curr_player.discard,
                   "cardsLeft": len(curr_player.deck), "field": curr_player.field,
                   "moveNotifier": opponent_move_notifier}
        socket_obj.emit("update opponent state", updater)

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field,
                   "canClickEndTurn": self.turn == other_player.name}
        socket_obj.emit("update your state", updater)

        updater = {"uuid": self.internal_id, "username": curr_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field}
        socket_obj.emit("update opponent state", updater)

        return response

    def play_hand(self, socket_obj: flask_socketio.SocketIO, povplayer: Literal[1, 2], hand_index: int,
                  frontend_request_json):
        # play card from hand, the most complicated function by far
        response = {
            "cardPlayed": "",
            "hand": [],
            "discard": [],
            "cardsLeft": 0,
            "nextTurn": False,  # tracks if in discarding phase (False) or can already switch turn (True)
            "winThisTurn": False  # someone won this turn, end game in frontend
        }

        curr_player: Player
        other_player: Player
        curr_player, other_player = (self.player1, self.player2) if (povplayer == 1) else (self.player2, self.player1)

        cardPlayed = curr_player.hand.pop(hand_index)["name"]

        if cardPlayed == "communitysupport":  # self explanatory. just plays community support
            curr_player.field.append("communitysupport")
            your_move_notifier = "You played Community Support."
            opponent_move_notifier = "Opponent played Community Support."
            next_turn = True
        elif cardPlayed in ("military-1", "economic-1", "economic-2", "civil-1"):  # draw 1 card
            curr_player.field.append(cardPlayed)
            if len(curr_player.deck) > 0:
                poppedCard = curr_player.popDeck()
                curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 1 card."
            else:
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} as you only had 0 cards in your deck."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} as they had only 0 cards in their deck."
            next_turn = True
        elif cardPlayed in ("military-2", "military-3", "civil-2", "economic-3", "economic-4"):
            curr_player.field.append(cardPlayed)
            if "extra" in frontend_request_json.json:
                extra = frontend_request_json.json["extra"]  # extra=-1 if draw 2, else restore extra-th discarded card
                if extra == -1:
                    if len(curr_player.deck) > 1:
                        poppedCard = curr_player.popDeck()
                        curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                        poppedCard2 = curr_player.popDeck()
                        curr_player.addHandCard(poppedCard2)  # add the popped card to the hand
                        your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]}, {lists.LOOKUP[poppedCard2]}."
                        opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 2 cards."
                    elif len(curr_player.deck) == 1:
                        poppedCard = curr_player.popDeck()
                        curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                        your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]} as you only had 1 card in your deck."
                        opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 1 card as they had only 1 card in their deck."
                    else:
                        your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} as you only had 0 cards in your deck."
                        opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} as they had only 0 cards in their deck."
                else:
                    restore = curr_player.discard.pop(extra)
                    curr_player.addHandCard(restore)
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and restored {lists.LOOKUP[restore]}."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and restored {lists.LOOKUP[restore]}."
            else:
                # no additional effect
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}."
            next_turn = True
        elif cardPlayed in (
                "psychological-2", "social-2",
                "digital-2"):  # draw 1 card, 1 extra if have community support
            curr_player.field.append(cardPlayed)
            if curr_player.field.count("communitysupport") >= 1:
                if len(curr_player.deck) > 1:
                    poppedCard = curr_player.popDeck()
                    curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                    poppedCard2 = curr_player.popDeck()
                    curr_player.addHandCard(poppedCard2)  # add the popped card to the hand
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]}, {lists.LOOKUP[poppedCard2]}."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 2 cards."
                elif len(curr_player.deck) == 1:
                    poppedCard = curr_player.popDeck()
                    curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]} as you only had 1 card in your deck."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 1 card as they had only 1 card in their deck."
                else:
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} as you only had 0 cards in your deck."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} as they had only 0 cards in their deck."
            else:
                if len(curr_player.deck) > 0:
                    poppedCard = curr_player.popDeck()
                    curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and drew {lists.LOOKUP[poppedCard]}."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and drew 1 card."
                else:
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} as you only had 0 cards in your deck."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} as they had only 0 cards in their deck."
            next_turn = True
        elif cardPlayed in ("social-1", "psychological-1", "digital-1"):  # play 1 extra card this turn
            curr_player.field.append(cardPlayed)
            your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}. It is still your turn."
            opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}. It is still their turn."
            next_turn = False
        elif cardPlayed in (
                "military-4", "civil-3", "economic-5", "social-3", "psychological-3",
                "digital-3"):  # view hand, play 1 extra and draw 1 if 2+ community support
            curr_player.field.append(cardPlayed)
            if curr_player.field.count("communitysupport") >= 2:
                # draw 1, extra turn
                if len(curr_player.deck) > 0:
                    poppedCard = curr_player.popDeck()
                    curr_player.addHandCard(poppedCard)  # add the popped card to the hand
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}, viewed your opponent's hand and drew {lists.LOOKUP[poppedCard]}. It is still your turn."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}, viewed your hand and drew 1 card. It is still their turn."
                else:
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} as you only had 0 cards in your deck. It is still your turn."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} as they had only 0 cards in their deck. It is still their turn."
                next_turn = False
            else:
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]} and viewed your opponent's hand."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]} and viewed your hand."
                next_turn = True
        elif cardPlayed in (
                "event-1", "event-3", "event-4", "event-2"):  # discard 1 from hand if opponent has no community support
            curr_player.discard = [cardPlayed] + curr_player.discard
            if "extra" in frontend_request_json.json:  # if it does not exist, card cannot be discarded (no card exists/opponent has too much community support)
                extra = frontend_request_json.json["extra"]
                card1 = other_player.hand.pop(extra)["name"]
                other_player.discard = [card1] + other_player.discard
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}, discarding opponent's {lists.LOOKUP[card1]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}, discarding your {lists.LOOKUP[card1]}."
            else:
                # no additional effect
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}."
            next_turn = True
        elif cardPlayed in (
                "event-5", "event-6", "event-7",
                "event-8"):  # discard 2 from defence if opponent has <=1 community support
            curr_player.discard = [cardPlayed] + curr_player.discard
            if "extra" in frontend_request_json.json:  # the first defence card, if it does not exist, card cannot be discarded (no card exists/opponent has too much community support)
                extra = frontend_request_json.json["extra"]  # [which (defence type), key (index)]
                card1 = list(filter(lambda name: name.startswith(extra[0]), other_player.field))[
                    extra[1]]
                other_player.discard = [card1] + other_player.discard
                if "extra2" in frontend_request_json.json:  # the second defence card, if it does not exist but "extra" exists, opponent only has 1 defence card
                    extra2 = frontend_request_json.json["extra2"]  # same as extra 1
                    card2 = list(filter(lambda name: name.startswith(extra2[0]), other_player.field))[
                        extra2[1]]
                    # todo (low priority) preserve order
                    other_player.field.remove(card1)
                    other_player.field.remove(card2)
                    other_player.discard = [card2] + other_player.discard
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}, discarding opponent's {lists.LOOKUP[card1]} & {lists.LOOKUP[card2]}."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}, discarding your {lists.LOOKUP[card1]} & {lists.LOOKUP[card2]}."
                else:
                    # only 1 defence card
                    other_player.field.remove(card1)
                    your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}, discarding opponent's {lists.LOOKUP[card1]}."
                    opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}, discarding your {lists.LOOKUP[card1]}."
            else:
                # no additional effect
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}."
            next_turn = True
        elif cardPlayed in (
                "event-9", "event-10", "event-11",
                "event-12"):  # discard 1 from field if opponent has <=2 community support
            curr_player.discard = [cardPlayed] + curr_player.discard
            if "extra" in frontend_request_json.json:  # if it does not exist, card cannot be discarded (no card exists/opponent has too much community support)
                extra = frontend_request_json.json["extra"]  # [which, key]
                card1 = list(filter(lambda name: name.startswith(extra[0]), other_player.field))[
                    extra[1]]
                other_player.discard = [card1] + other_player.discard
                other_player.field.remove(card1)
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}, discarding opponent's {lists.LOOKUP[card1]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}, discarding your {lists.LOOKUP[card1]}."
            else:
                # no additional effect
                your_move_notifier = f"You played {lists.LOOKUP[cardPlayed]}."
                opponent_move_notifier = f"Opponent played {lists.LOOKUP[cardPlayed]}."
            next_turn = True
        else:  # not used, code should not get here at all
            curr_player.discard = [cardPlayed] + curr_player.discard
            your_move_notifier = f"You discarded {lists.LOOKUP[cardPlayed]}."
            opponent_move_notifier = f"Opponent discarded {lists.LOOKUP[cardPlayed]}."
            next_turn = False

        if curr_player.gameWon():
            your_move_notifier += "\nYou win!"
            opponent_move_notifier += "\nYou lose!"
            next_turn = False
            curr_player.setHandEnablePlayStatus(False)
            other_player.setHandEnablePlayStatus(False)
            response["winThisTurn"] = True

        if next_turn:
            # only run for cards which end turn (i.e. not "Play 1 extra card this turn")
            # also not run if you win
            if len(curr_player.hand) > 7:
                # the max cards you can have is 9. 7 cards, draw 1 for turn, play 1 allowing draw 2.
                # we can just check for hand size though, not based on the above info that 9 is max
                your_move_notifier += f"\nPlease discard cards until you have 7 cards."
                opponent_move_notifier += f"\nWaiting for opponent to discard hand cards."

                response["needDiscard"] = True
            else:
                if self.nextturnislast:
                    # this turn was the last turn, so trigger game ending calculation
                    if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                        your_move_notifier += "\nOpponent's deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                        opponent_move_notifier += "\nYour deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                    elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                        your_move_notifier += "\nOpponent's deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                        opponent_move_notifier += "\nYour deck ran out of cards 1 turn ago. Tie due to having equal defence fulfilled!"
                    else:  # player 2 more than player 1
                        your_move_notifier += "\nYOpponent's deck ran out of cards 1 turn ago. You lose due to having less defence fulfilled!"
                        opponent_move_notifier += "\nYour deck ran out of cards 1 turn ago. You win due to having more defence fulfilled!"
                    response["winThisTurn"] = True
                elif len(curr_player.deck) == 0:
                    # current player ran out of cards, run appropriate logic
                    if self.gofirst == curr_player.name:
                        # award extra turn
                        self.nextturnislast = True
                        your_move_notifier += "\nWarning: Your opponent's next turn is the last turn, due to your deck running out of cards."
                        opponent_move_notifier += "\nWarning: Your opponent's next turn is the last, due to their deck running out of cards."
                    else:
                        # end game and compute winner
                        if curr_player.gameDefenceFulfilled() > other_player.gameDefenceFulfilled():
                            your_move_notifier += "\nYour deck ran out of cards. You win due to having more defence fulfilled!"
                            opponent_move_notifier += "\nOpponent's deck ran out of cards. You lose due to having less defence fulfilled!"
                        elif curr_player.gameDefenceFulfilled() == other_player.gameDefenceFulfilled():
                            your_move_notifier += "\nYour deck ran out of cards. Tie due to having equal defence fulfilled!"
                            opponent_move_notifier += "\nOpponent's deck ran out of cards. Tie due to having equal defence fulfilled!"
                        else:  # player 2 more than player 1
                            your_move_notifier += "\nYour deck ran out of cards. You lose due to having less defence fulfilled!"
                            opponent_move_notifier += "\nOpponent's deck ran out of cards. You win due to having more defence fulfilled!"
                        response["winThisTurn"] = True
                else:
                    # switch turn
                    poppedCard = other_player.popDeck()
                    other_player.addHandCard(poppedCard)  # add the popped card to the hand

                    other_player.setHandEnablePlayStatus(True)
                    curr_player.setHandEnablePlayStatus(False)
                    self.recomputeBlockAndDialogStatus()
                    self.turn = other_player.name

                    your_move_notifier += "\nOpponent's turn."
                    opponent_move_notifier += f"\nYour turn. You drew {lists.LOOKUP[poppedCard]}."

        # update both player's displays

        response["hand"] = curr_player.hand
        response["discard"] = curr_player.discard
        response["cardsLeft"] = len(curr_player.deck)
        response["cardPlayed"] = cardPlayed
        response["field"] = curr_player.field
        response["moveNotifier"] = your_move_notifier
        response["canClickEndTurn"] = curr_player.name == self.turn

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": curr_player.hand, "discard": curr_player.discard,
                   "cardsLeft": len(curr_player.deck), "field": curr_player.field,
                   "moveNotifier": opponent_move_notifier}
        socket_obj.emit("update opponent state", updater)

        updater = {"uuid": self.internal_id, "username": other_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field,
                   "canClickEndTurn": self.turn == other_player.name}
        socket_obj.emit("update your state", updater)

        updater = {"uuid": self.internal_id, "username": curr_player.name,
                   "hand": other_player.hand, "discard": other_player.discard,
                   "cardsLeft": len(other_player.deck), "field": other_player.field}
        socket_obj.emit("update opponent state", updater)

        return response
