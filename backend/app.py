import random
import secrets
import time
import threading
import uuid
from datetime import datetime
from typing import Union

from flask import Flask, request, send_file, abort, Response, jsonify
from flask_cors import CORS, cross_origin
import json
from flask_socketio import SocketIO

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "runtime.log"

# standard deck is a list of the name strings of cards
standard_deck: list[str] = [
    "communitysupport",
    "communitysupport",
    "communitysupport",
    "communitysupport",

    "event-1",
    "event-2",
    "event-3",
    "event-4",
    "event-5",
    "event-6",
    "event-7",
    "event-8",
    "event-9",
    "event-10",
    "event-11",
    "event-12",

    "civil-1",
    "civil-1",
    "civil-2",
    "civil-2",
    "civil-3",
    "digital-1",
    "digital-1",
    "digital-2",
    "digital-2",
    "digital-3",
    "economic-1",
    "economic-2",
    "economic-3",
    "economic-4",
    "economic-5",
    "military-1",
    "military-1",
    "military-2",
    "military-3",
    "military-4",
    "psychological-1",
    "psychological-1",
    "psychological-2",
    "psychological-2",
    "psychological-3",
    "social-1",
    "social-1",
    "social-2",
    "social-2",
    "social-3",
]

# select crisis from here
crisis_deck: list[str] = [
    "crisis-1",
    "crisis-2",
    "crisis-3",
    "crisis-4",
    "crisis-5",
    "crisis-6",
]

# get name from id string
lookup: dict[str, str] = {
    "communitysupport": "Community Support",
    "event-1": "Racial and Religious Tension",
    "event-2": "Complaint Culture",
    "event-3": "Stolen Personal Data",
    "event-4": "Desensitised Citizens",
    "event-5": "Disgruntled NSmen",
    "event-6": "Criminal Collaboration",
    "event-7": "Blood Bank Runs Dry",
    "event-8": "Ransomware Attack",
    "event-9": "Heightened Terrorist Alert",
    "event-10": "Self Radicalisation",
    "event-11": "Lone Wolf Attack",
    "event-12": "Recruiting Desperate People",
    "civil-1": "Alert Community",
    "civil-2": "Prepared for Crisis",
    "civil-3": "Civil Emergency",
    "digital-1": "Use of Strong Passwords",
    "digital-2": "Robust Emergency Protocols",
    "digital-3": "Responsible Social Media Use",
    "economic-1": "Career Mobility",
    "economic-2": "Business Resilience",
    "economic-3": "Financial Aid Schemes",
    "economic-4": "Increase Surveillance at Maritime Ports",
    "economic-5": "Skills Upgrading",
    "military-1": "NSmen on Guard",
    "military-2": "Increased Security Checks",
    "military-3": "Naval Convoys",
    "military-4": "Conduct of Raids",
    "psychological-1": "Education",
    "psychological-2": "Attend National Day Celebrations",
    "psychological-3": "Strong Resolve",
    "social-1": "Religious Counselling",
    "social-2": "Neighbourliness",
    "social-3": "Show of Solidarity"
}


class Player:
    def __init__(self, name):
        self.name = name
        self.deck: list[str] = standard_deck.copy()
        random.shuffle(self.deck)  # upon creation of the user, shuffle the deck
        self.crisis: str = random.choice(crisis_deck)  # server side crisis
        self.hand: list[dict[str, Union[str, bool]]] = []  # server side hand
        self.discard: list[str] = []
        self.field: list[str] = []

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def popDeck(self):
        return self.deck.pop()

    def newDeck(self):
        self.deck = standard_deck.copy()
        self.discard = []
        self.hand = []
        random.shuffle(self.deck)

    def newCrisis(self):
        self.crisis = random.choice(crisis_deck)
        return self.crisis

    def setHandEnablePlayStatus(self, status: bool):
        handcopy = self.hand.copy()
        for i in handcopy:
            i["enablePlay"] = status
        self.hand = handcopy
        return self.hand

    def addHandCard(self, cardName):
        if len(self.hand) >= 7:
            # todo not only 0 (only discard at end of turn)
            self.discard = [self.hand.pop(0)["name"]] + self.discard
        self.hand.append({"name": cardName, "enablePlay": True,  # "blockPlay": False, # can play card without effect
                          # these will be set later
                          # everywhere that could affect this (eg draw card) will be accompanied by a recompute call
                          # we just cannot call it here because this is Player not Game
                          "requiresDialogNormal": False, "requiresDialogDefence": False,
                          "requiresDialogField": False, "requiresDialogHand": False})
        return self.hand


class Game:
    def __init__(self, player1_username, player2_username, internal_id):
        self.player1 = Player(player1_username)
        self.player2 = Player(player2_username)
        while self.player1.crisis == self.player2.crisis:
            # crises cannot be equal
            self.player1 = Player(player1_username)
            self.player2 = Player(player2_username)
        self.player1_username = player1_username
        self.player2_username = player2_username
        self.gofirst = self.player1_username if self.player1.crisis > self.player2.crisis else self.player2_username

        self.internal_id = internal_id

    def recomputeBlockAndDialogStatus(self):
        handcopy = self.player1.hand.copy()
        for i in handcopy:
            # [1 CSC:] Draw 2 additional cards OR Take any card from your discard pile and place it back into your hand
            if i["name"] in ("military-2", "military-3", "civil-2", "economic-3", "economic-4"):
                i["requiresDialogNormal"] = self.player1.field.count("communitysupport") >= 1
                if len(self.player1.discard) == 0:
                    i["warn"] = "\nWarning: There are no cards in your discard pile. Picking the second option will have no effect."
                else:
                    i["warn"] = ""  # no warning for playing def card without effect as it could be helpful
                    # for example to win the game
            # If your opponent has 1 or less Community Support points, discard any 2 Defence cards from your opponent's field
            if i["name"] in ("event-2", "event-5", "event-6", "event-7", "event-8"):
                i["requiresDialogDefence"] = self.player2.field.count("communitysupport") <= 1
                if i["requiresDialogDefence"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"
            # If your opponent has 2 or less Community Support points, discard any 1 card from your opponent's field
            if i["name"] in ("event-9", "event-10", "event-11", "event-12"):
                i["requiresDialogField"] = self.player2.field.count("communitysupport") <= 2
                if i["requiresDialogField"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"
            # If your opponent has no Community Support points, look at your opponent's hand and discard 1 card from there
            if i["name"] in ("event-1", "event-3", "event-4"):
                i["requiresDialogHand"] = len(self.player2.hand) > 0 and self.player2.field.count("communitysupport") == 0
                if i["requiresDialogHand"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"

        self.player1.hand = handcopy

        handcopy = self.player2.hand.copy()
        for i in handcopy:
            # [1 CSC:] Draw 2 additional cards OR Take any card from your discard pile and place it back into your hand
            if i["name"] in ("military-2", "military-3", "civil-2", "economic-3", "economic-4"):
                i["requiresDialogNormal"] = self.player2.field.count("communitysupport") >= 1
                if len(self.player2.discard) == 0:
                    i["warn"] = "\nWarning: There are no cards in your discard pile. Picking the second option will have no effect."
                else:
                    i["warn"] = ""  # no warning for playing def card without effect as it could be helpful
                    # for example to win the game
            # If your opponent has 1 or less Community Support points, discard any 2 Defence cards from your opponent's field
            if i["name"] in ("event-2", "event-5", "event-6", "event-7", "event-8"):
                i["requiresDialogDefence"] = self.player1.field.count("communitysupport") <= 1
                if i["requiresDialogDefence"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"
            # If your opponent has 2 or less Community Support points, discard any 1 card from your opponent's field
            if i["name"] in ("event-9", "event-10", "event-11", "event-12"):
                i["requiresDialogField"] = self.player1.field.count("communitysupport") <= 2
                if i["requiresDialogField"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"
            # If your opponent has no Community Support points, look at your opponent's hand and discard 1 card from there
            if i["name"] in ("event-1", "event-3", "event-4"):
                i["requiresDialogHand"] = len(self.player1.hand) > 0 and self.player1.field.count("communitysupport") == 0
                if i["requiresDialogHand"]:
                    i["warn"] = ""
                else:
                    i["warn"] = "This card will have no effect!"

        self.player2.hand = handcopy
        return self.player1.hand, self.player2.hand


class User:
    def __init__(self, name, last_checkin, login_session_key):
        self.name: str = name
        self.last_checkin: float = last_checkin
        self.login_session_key: str = login_session_key
        self.games: list[str] = []

    def __str__(self):
        return self.name + " | " + str(self.last_checkin)


logged_in: list[User] = []
queue: list[User] = []
games: dict[str, Game] = {}


def usersListString():
    ret_string = ""
    for i in logged_in:
        ret_string += str(i) + "\n"
    return ret_string.strip()


def writeLog(log_string):
    with open(LOG_FILE, "a") as f:
        print(log_string, file=f)


writeLog("Started @ " + str(int(datetime.now().timestamp())))


def clear_inactive_users_from_login():
    while True:
        users_to_log_off = []
        curr_time = int(datetime.now().timestamp())
        for i in logged_in:
            if (curr_time - i.last_checkin > 10 * 60):  # if not checked in for more than 10*60 secs = 10 mins
                users_to_log_off.append(i)
        for i in users_to_log_off:
            logged_in.remove(i)
            if i in queue:
                queue.remove(i)
        writeLog("after clearing cycle @" + str(curr_time) + ": {")
        writeLog(usersListString())
        writeLog("}")
        socketio.emit('number logged in', {'data': len(logged_in)})
        time.sleep(2 * 60)  # do the check ever 2 mins


log_in_clearer_daemon = threading.Thread(target=clear_inactive_users_from_login, daemon=True)
log_in_clearer_daemon.start()


@app.route('/')
def main():  # put application's code here
    return 'Hello World!'


@app.route('/calculate', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def calculate():
    if request.method == "POST":
        return str(request.json['value'] ** 2)


@app.route('/set_counter', methods=['POST'])
@cross_origin()
def set_counter():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if (i.name == username) and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            break
    # if indeed logged in then do the set counter stuff
    if (target_user_logged_in):
        if request.method == "POST":
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
            with open("data.json", "w") as data_file:
                data[request.json["username"]] = request.json["value"]
                json.dump(data, data_file)
    return "end of function"  # every method should return something


@app.route('/get_counter', methods=['POST'])
@cross_origin()
def get_counter():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if (i.name == username) and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            break
    # if indeed logged in then do the get counter stuff
    if (target_user_logged_in):
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            if username in data:
                return str(data[username])
            else:
                return "0"
    return "end of function"  # every method should return something


@app.route('/sign_in', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_in():
    proposed_username = request.json['proposed_username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text": "PLACEHOLDER",
        "confirmed_username": "",
        "login_session_key": "0",
        "login_success": False
    }
    if request.method == "POST":
        for i in logged_in:

            keys_equal = False if not type(
                sent_login_sesh_key) == 'str' else secrets.compare_digest(i.login_session_key, sent_login_sesh_key)

            if (i.name == proposed_username) and not keys_equal:
                response["text"] = "This username is already logged in"
                writeLog(usersListString())
                return response
            elif (i.name == proposed_username) and keys_equal:
                new_login_session_key = secrets.token_hex()
                i.login_session_key = new_login_session_key
                i.last_checkin = datetime.now().timestamp()
                response["text"] = "Logged in as " + proposed_username
                response["confirmed_username"] = proposed_username
                response["login_session_key"] = new_login_session_key
                response["login_success"] = True
                return response
        # else
        login_session_key = secrets.token_hex()
        logged_in.append(User(proposed_username, int(datetime.now().timestamp()), login_session_key))
        response["text"] = "Logged in as " + proposed_username
        response["confirmed_username"] = proposed_username
        response["login_session_key"] = login_session_key
        response["login_success"] = True
        writeLog(usersListString())
        socketio.emit('number logged in', {'data': len(logged_in)})
        return response


@app.route('/sign_out', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_out():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text": "PLACEHOLDER",
        "signout_success": False
    }

    if request.method == "POST":
        users_to_remove = []
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == username) and keys_equal:
                users_to_remove.append(i)
        if len(users_to_remove) > 0:
            for i in users_to_remove:
                logged_in.remove(i)
                if i in queue:
                    queue.remove(i)
            response["text"] = "signed out successfully"
            response["signout_success"] = True
            socketio.emit('number logged in', {'data': len(logged_in)})
        else:
            response["text"] = "nobody was signed out"
            response["signout_success"] = False
        return response


@app.route('/disconnect', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def disconnect():
    # yes this is the same as sign out. might be changed later
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text": "PLACEHOLDER",
        "signout_success": False
    }

    if request.method == "POST":
        users_to_remove = []
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == username) and keys_equal:
                users_to_remove.append(i)
        if len(users_to_remove) > 0:
            for i in users_to_remove:
                logged_in.remove(i)
                if i in queue:
                    queue.remove(i)
            response["text"] = "signed out successfully"
            response["signout_success"] = True
            socketio.emit('number logged in', {'data': len(logged_in)})
        else:
            response["text"] = "nobody was signed out"
            response["signout_success"] = False
        return response


@app.route('/user_activity_ping', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def user_activity_ping():
    pinger_username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text": "PLACEHOLDER",
        "still_active": False
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == pinger_username) and keys_equal:
                i.last_checkin = int(datetime.now().timestamp())
                response["text"] = "activity sucessfully registered"
                response["still_active"] = True
                return response
        # else
        response["text"] = "You were signed out due to inactivity!"
        response["still_active"] = False
        return response


@app.route('/activity_status_request', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def activity_status_request():
    pinger_username = request.json['username']
    response = {
        "text": "PLACEHOLDER",
        "still_active": False
    }
    if request.method == "POST":
        for i in logged_in:
            if i.name == pinger_username:
                response["text"] = "account still logged in"
                response["still_active"] = True
                return response
        # else
        response["text"] = "You were signed out due to inactivity!"
        response["still_active"] = False
        return response


@app.route('/get_image')
def get_image():
    return send_file("Oran_Berry_Sprite.png", mimetype='image/png')


@app.route('/get_number_logged_in')
def get_number_logged_in():
    return str(len(logged_in))


@app.route('/request_match', methods=['POST'])
@cross_origin()
def request_match():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if i.name == username and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            break
    # if indeed logged in
    if request.method == "POST":
        if target_user_logged_in:
            # is the requested person logged in?
            requested = request.json['requested_username']
            for i in logged_in:
                if i.name == requested:
                    socketio.emit("challenge", {"username": username, "opponent": requested})
                    return jsonify({"status": "Challenging opponent", "opponent": requested})
            return jsonify({"status": "Opponent not logged in"})
        abort(Response(json.dumps({"Message": "Finding Opponent Unavailable"}), 404))


@app.route('/accept_match', methods=['POST'])
@cross_origin()
def accept_match():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if i.name == username and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            user = i
            break
    # if indeed logged in
    if request.method == "POST":
        if target_user_logged_in:
            # is the requested person logged in?
            requested = request.json['requested_username']
            for i in logged_in:
                if i.name == requested:
                    opponent = i
                    random_uuid = str(uuid.uuid4())
                    # can get away with using the same
                    socketio.emit("match request", {"username": opponent.name, "id": random_uuid})
                    games[random_uuid] = Game(opponent.name, username, random_uuid)
                    user.games.append(random_uuid)
                    opponent.games.append(random_uuid)
                    return jsonify({"status": "Found opponent", "opponent": opponent.name, "id": random_uuid})
            return jsonify({"status": "Opponent not logged in"})
        abort(Response(json.dumps({"Message": "Finding Opponent Unavailable"}), 404))


@app.route('/deny_match', methods=['POST'])
@cross_origin()
def deny_match():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if i.name == username and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            user = i
            break
    # if indeed logged in
    if request.method == "POST":
        if target_user_logged_in:
            # is the requested person logged in?
            requested = request.json['requested_username']
            for i in logged_in:
                if i.name == requested:
                    opponent = i
                    socketio.emit("deny opponent", {"username": username, "opponent": opponent.name})
                    # todo block opponent if too many deny requests?
                    return jsonify({"status": "Denied opponent", "opponent": opponent.name})
            return jsonify({"status": "Opponent not logged in"})
        abort(Response(json.dumps({"Message": "Finding Opponent Unavailable"}), 404))


@app.route('/random_opponent', methods=['POST'])
@cross_origin()
def random_opponent():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    # first check if logged_in
    target_user_logged_in = False
    for i in logged_in:
        if i.name == username and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            user = i
            break
    # if indeed logged in
    if request.method == "POST":
        if target_user_logged_in:
            if len(queue) == 0:
                queue.append(user)
                return jsonify({"status": "Added to queue"})
            else:
                # failsafe
                if user in queue:
                    return jsonify({"status": "Added to queue"})
                opponent = random.choice(queue)
                queue.remove(opponent)
                random_uuid = str(uuid.uuid4())
                socketio.emit("match request", {"username": opponent.name, "id": random_uuid})
                games[random_uuid] = Game(opponent.name, username, random_uuid)
                user.games.append(random_uuid)
                opponent.games.append(random_uuid)
                return jsonify({"status": "Found opponent", "opponent": opponent.name, "id": random_uuid})
        abort(Response(json.dumps({"Message": "Finding Opponent Unavailable"}), 404))


@app.route('/get_card', methods=["GET"])
def get_card():
    cardname = request.args.get('cardname')
    return send_file(f"card_art/{cardname}.png", mimetype='image/png')


@app.route('/get_deck', methods=["POST"])
@cross_origin()
def get_deck():
    # return a game's full undrawn deck if username and login session key fits
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "deck": []
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["deck"] = game.player1.deck
                elif game.player2_username == request_username:
                    response["deck"] = game.player2.deck
                return response
        # else
        abort(Response(json.dumps({"Message": "Deck Unavailable"}), 404))


@app.route('/get_cardsleft', methods=["POST"])
@cross_origin()
def get_cardsleft():
    # return cards left in a game's deck if username and login session key fits
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "cardsLeft": 0
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["cardsLeft"] = len(game.player1.deck)
                elif game.player2_username == request_username:
                    response["cardsLeft"] = len(game.player2.deck)
                return response
        # else
        abort(Response(json.dumps({"Message": "Cards Left Unavailable"}), 404))


@app.route('/pop_deck', methods=["POST"])
@cross_origin()
def pop_deck():
    # pop the top of a user's undrawn deck if username and login session key fits & return
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "card": "",
        "cardsLeft": 0
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    if len(game.player1.deck) > 0:
                        poppedCard = game.player1.popDeck()
                        game.player1.addHandCard(poppedCard)  # add the popped card to the hand
                        game.recomputeBlockAndDialogStatus()
                        response["card"] = poppedCard
                        response["cardsLeft"] = len(game.player1.deck)

                        updater = {"uuid": game_id, "username": game.player2_username,
                                   "cardsLeft": len(game.player1.deck), "discard": game.player1.discard}
                        socketio.emit("update opponent state", updater)

                        return response
                    else:
                        return abort(Response(json.dumps({"Message": "Deck Empty"}), 404))
                elif game.player2_username == request_username:
                    if len(game.player2.deck) > 0:
                        poppedCard = game.player2.popDeck()
                        game.player2.addHandCard(poppedCard)  # add the popped card to the hand
                        game.recomputeBlockAndDialogStatus()
                        response["card"] = poppedCard
                        response["cardsLeft"] = len(game.player2.deck)

                        updater = {"uuid": game_id, "username": game.player1_username,
                                   "cardsLeft": len(game.player2.deck), "discard": game.player2.discard}
                        socketio.emit("update opponent state", updater)

                        return response
                    else:
                        return abort(Response(json.dumps({"Message": "Deck Empty"}), 404))
                return response
        # else
        abort(Response(json.dumps({"Message": "Deck Unavailable"}), 404))


@app.route('/new_deck', methods=["POST"])
@cross_origin()
def new_deck():
    # make a new shuffled deck for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "deck": []
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    game.player1.newDeck()
                    response["deck"] = game.player1.deck

                    updater = {"uuid": game_id, "username": game.player2_username,
                               "cardsLeft": len(game.player1.deck)}
                    socketio.emit("update opponent state", updater)
                elif game.player2_username == request_username:
                    game.player2.newDeck()
                    response["deck"] = game.player2.deck

                    updater = {"uuid": game_id, "username": game.player1_username,
                               "cardsLeft": len(game.player2.deck)}
                    socketio.emit("update opponent state", updater)
                return response
        # else
        abort(Response(json.dumps({"Message": "Deck Unavailable"}), 404))


@app.route('/new_crisis', methods=["POST"])
@cross_origin()
def new_crisis():
    # create a crisis for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "crisis": ""
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["crisis"] = game.player1.newCrisis()
                    updater = {"uuid": game_id, "username": game.player2_username,
                               "crisis": response["crisis"]}
                    socketio.emit("update opponent state", updater)
                elif game.player2_username == request_username:
                    response["crisis"] = game.player2.newCrisis()
                    updater = {"uuid": game_id, "username": game.player1_username,
                               "crisis": response["crisis"]}
                    socketio.emit("update opponent state", updater)
                return response
        # else
        abort(Response(json.dumps({"Message": "New Crisis Unavailable"}), 404))


@app.route('/deck_size')
@cross_origin()
def new_deck_size():
    return str(len(standard_deck))


@app.route('/get_crisis', methods=["POST"])
@cross_origin()
def get_crisis():
    # return crisis for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "crisis": ""
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["crisis"] = game.player1.crisis
                elif game.player2_username == request_username:
                    response["crisis"] = game.player2.crisis
                return response
        # else
        abort(Response(json.dumps({"Message": "Crisis Unavailable"}), 404))


@app.route('/get_hand', methods=["POST"])
@cross_origin()
def get_hand():
    # return hand for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "hand": []
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["hand"] = game.player1.hand
                elif game.player2_username == request_username:
                    response["hand"] = game.player2.hand
                return response
        # else
        abort(Response(json.dumps({"Message": "Hand Unavailable"}), 404))


@app.route('/play_hand', methods=["POST"])
@cross_origin()
def play_hand():
    # make a new shuffled deck for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    hand_index = request.json['card_index']
    response = {
        "cardPlayed": "",
        "hand": [],
        "discard": [],
        "cardsLeft": 0,
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    if (hand_index < 0) or (hand_index >= len(game.player1.hand)):
                        abort(Response(json.dumps({"Message": "Card Index Out Of Range"}), 422))
                    else:
                        cardPlayed = game.player1.hand.pop(hand_index)["name"]

                        if cardPlayed == "communitysupport":
                            game.player1.field.append("communitysupport")
                            your_move_notifier = "You played Community Support.\nOpponent's turn."
                            opponent_move_notifier = "Opponent played Community Support."
                            next_turn = True
                        elif cardPlayed in ("military-1", "economic-1", "economic-2", "civil-1"):  # draw 1 card
                            game.player1.field.append(cardPlayed)

                            poppedCard = game.player1.popDeck()  # todo zero cards check
                            game.player1.addHandCard(poppedCard)  # add the popped card to the hand
                            your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}.\nOpponent's turn."
                            opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card."
                            next_turn = True
                        elif cardPlayed in ("psychological-2", "social-2", "digital-2"):  # draw 1 card, 1 extra if have community support
                            game.player1.field.append(cardPlayed)

                            poppedCard = game.player1.popDeck()
                            game.player1.addHandCard(poppedCard)  # add the popped card to the hand

                            if game.player1.field.count("communitysupport") >= 1:
                                if len(game.player1.deck) > 0:
                                    poppedCard2 = game.player1.popDeck()
                                    game.player1.addHandCard(poppedCard2)  # add the popped card to the hand
                                    your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}, {lookup[poppedCard2]}.\nOpponent's turn."
                                    opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 2 cards."
                                else:
                                    your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]} as you only had 1 card in your deck.\nOpponent's turn."
                                    opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card as they had only 1 card in their deck."
                            else:
                                your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}.\nOpponent's turn."
                                opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card."
                            next_turn = True
                        else:  # todo every other card
                            game.player1.discard = [cardPlayed] + game.player1.discard
                            your_move_notifier = f"You discarded {lookup[cardPlayed]}."
                            opponent_move_notifier = f"Opponent discarded {lookup[cardPlayed]}."
                            next_turn = False

                        if next_turn:
                            # todo do winning checks (out of cards, defence fulfilled)

                            poppedCard = game.player2.popDeck()
                            game.player2.addHandCard(poppedCard)  # add the popped card to the hand

                            game.player2.setHandEnablePlayStatus(True)
                            game.player1.setHandEnablePlayStatus(False)
                            game.recomputeBlockAndDialogStatus()

                            updater = {"uuid": game_id, "username": game.player2_username,
                                       "hand": game.player2.hand, "discard": game.player2.discard,
                                       "cardsLeft": len(game.player2.deck), "field": game.player2.field}
                            opponent_move_notifier += f"\nYour turn. You drew {lookup[poppedCard]}."
                            socketio.emit("update your state", updater)

                        response["hand"] = game.player1.hand
                        response["discard"] = game.player1.discard
                        response["cardsLeft"] = len(game.player1.deck)
                        response["cardPlayed"] = cardPlayed
                        response["field"] = game.player1.field
                        response["moveNotifier"] = your_move_notifier

                        updater = {"uuid": game_id, "username": game.player2_username,
                                   "hand": game.player1.hand, "discard": game.player1.discard,
                                   "cardsLeft": len(game.player1.deck), "field": game.player1.field,
                                   "moveNotifier": opponent_move_notifier}
                        socketio.emit("update opponent state", updater)

                        return response
                elif game.player2_username == request_username:
                    if (hand_index < 0) or (hand_index >= len(game.player2.hand)):
                        abort(Response(json.dumps({"Message": "Card Index Out Of Range"}), 422))
                    else:
                        cardPlayed = game.player2.hand.pop(hand_index)["name"]

                        if cardPlayed == "communitysupport":
                            game.player2.field.append("communitysupport")
                            your_move_notifier = "You played Community Support.\nOpponent's turn."
                            opponent_move_notifier = "Opponent played Community Support."
                            next_turn = True
                        elif cardPlayed in ("military-1", "economic-1", "economic-2", "civil-1"):  # draw 1 card
                            game.player2.field.append(cardPlayed)

                            poppedCard = game.player2.popDeck()
                            game.player2.addHandCard(poppedCard)  # add the popped card to the hand
                            your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}.\nOpponent's turn."
                            opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card."
                            next_turn = True
                        elif cardPlayed in ("psychological-2", "social-2", "digital-2"):  # draw 1 card, 1 extra if have community support
                            game.player2.field.append(cardPlayed)

                            poppedCard = game.player2.popDeck()
                            game.player2.addHandCard(poppedCard)  # add the popped card to the hand

                            if game.player2.field.count("communitysupport") >= 1:
                                if len(game.player2.deck) > 0:
                                    poppedCard2 = game.player2.popDeck()
                                    game.player2.addHandCard(poppedCard2)  # add the popped card to the hand
                                    your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}, {lookup[poppedCard2]}.\nOpponent's turn."
                                    opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 2 cards."
                                else:
                                    your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]} as you only had 1 card in your deck.\nOpponent's turn."
                                    opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card as they had only 1 card in their deck."
                            else:
                                your_move_notifier = f"You played {lookup[cardPlayed]} and drew {lookup[poppedCard]}.\nOpponent's turn."
                                opponent_move_notifier = f"Opponent played {lookup[cardPlayed]} and drew 1 card."
                            next_turn = True
                        else:  # todo every other card
                            game.player2.discard = [cardPlayed] + game.player2.discard
                            your_move_notifier = f"You discarded {lookup[cardPlayed]}."
                            opponent_move_notifier = f"Opponent discarded {lookup[cardPlayed]}."
                            next_turn = False

                        if next_turn:
                            # todo do winning checks

                            poppedCard = game.player1.popDeck()
                            game.player1.addHandCard(poppedCard)  # add the popped card to the hand

                            game.player1.setHandEnablePlayStatus(True)
                            game.player2.setHandEnablePlayStatus(False)
                            game.recomputeBlockAndDialogStatus()

                            updater = {"uuid": game_id, "username": game.player1_username,
                                       "hand": game.player1.hand, "discard": game.player1.discard,
                                       "cardsLeft": len(game.player1.deck), "field": game.player1.field}
                            opponent_move_notifier += f"\nYour turn. You drew {lookup[poppedCard]}."
                            socketio.emit("update your state", updater)

                        response["hand"] = game.player2.hand
                        response["discard"] = game.player2.discard
                        response["cardsLeft"] = len(game.player2.deck)
                        response["cardPlayed"] = cardPlayed
                        response["field"] = game.player2.field
                        response["moveNotifier"] = your_move_notifier

                        updater = {"uuid": game_id, "username": game.player1_username,
                                   "hand": game.player2.hand, "discard": game.player2.discard,
                                   "cardsLeft": len(game.player2.deck), "field": game.player2.field,
                                   "moveNotifier": opponent_move_notifier}
                        socketio.emit("update opponent state", updater)

                        return response
        # else
        abort(Response(json.dumps({"Message": "Cannot Play Hand"}), 404))


@app.route('/get_discard', methods=["POST"])
@cross_origin()
def get_discard():
    # make a new shuffled deck for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    response = {
        "discard": []
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    response["discard"] = game.player1.discard
                elif game.player2_username == request_username:
                    response["discard"] = game.player2.discard
                return response
        # else
        abort(Response(json.dumps({"Message": "Discard Unavailable"}), 404))


@app.route('/game_init', methods=["POST"])
@cross_origin()
def game_init():
    # Initialises the game for the user whose LSK and username fit. 1 person per call, called 2 times.
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    game_id = request.json['game_id']
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                try:
                    game: Game = games[game_id]
                except KeyError:
                    return "Not Found"
                if game.player1_username == your_username or game.player2_username == your_username:
                    notifier = ""
                    if game.player1.crisis > game.player2.crisis and game.player1_username == your_username:
                        if len(game.player1.deck) == 46:  # fresh game, should initialise
                            for q in range(5):
                                game.player1.addHandCard(game.player1.popDeck())
                            game.player1.setHandEnablePlayStatus(True)
                            game.recomputeBlockAndDialogStatus()
                            notifier = f"Your crisis has the higher number. You are going first. Drew {lookup[game.player1.hand[-1]['name']]}."
                        returned = {"username": your_username,
                                    "hand": game.player1.hand,
                                    "cardsLeft": len(game.player1.deck),
                                    "field": game.player1.field,
                                    "discard": game.player1.discard,
                                    "crisis": game.player1.crisis,
                                    "moveNotifier": notifier,
                                    "uuid": game.internal_id}
                        # todo keep track of turn phase (eg playing time/discard cards at end of hand time etc)
                        socketio.emit("update your state", returned)
                        socketio.emit("update opponent state", {"username": game.player2_username,
                                                                "cardsLeft": len(game.player1.deck),
                                                                "field": game.player1.field,
                                                                "discard": game.player1.discard,
                                                                "crisis": game.player1.crisis,
                                                                "uuid": game.internal_id})
                        return "First"
                    elif game.player1.crisis < game.player2.crisis and game.player1_username == your_username:
                        if len(game.player1.deck) == 46:  # fresh game, should initialise
                            for q in range(5):
                                game.player1.addHandCard(game.player1.popDeck())
                            game.player1.setHandEnablePlayStatus(False)
                            game.recomputeBlockAndDialogStatus()
                            notifier = f"Your crisis has the lower number.  You are going second."
                        returned = {"username": your_username,
                                    "hand": game.player1.hand,
                                    "cardsLeft": len(game.player1.deck),
                                    "field": game.player1.field,
                                    "discard": game.player1.discard,
                                    "crisis": game.player1.crisis,
                                    "moveNotifier": notifier,
                                    "uuid": game.internal_id}
                        socketio.emit("update your state", returned)
                        socketio.emit("update opponent state", {"username": game.player2_username,
                                                                "cardsLeft": len(game.player1.deck),
                                                                "field": game.player1.field,
                                                                "discard": game.player1.discard,
                                                                "crisis": game.player1.crisis,
                                                                "uuid": game.internal_id})
                        return "Second"
                    elif game.player1.crisis > game.player2.crisis and game.player2_username == your_username:
                        if len(game.player2.deck) == 46:  # fresh game, should initialise
                            for q in range(5):
                                game.player2.addHandCard(game.player2.popDeck())
                            game.player2.setHandEnablePlayStatus(False)
                            game.recomputeBlockAndDialogStatus()
                            notifier = f"Your crisis has the lower number.  You are going second."
                        socketio.emit("update your state", {"username": your_username,
                                                            "hand": game.player2.hand,
                                                            "cardsLeft": len(game.player2.deck),
                                                            "field": game.player2.field,
                                                            "discard": game.player2.discard,
                                                            "crisis": game.player2.crisis,
                                                            "moveNotifier": notifier,
                                                            "uuid": game.internal_id})
                        socketio.emit("update opponent state", {"username": game.player1_username,
                                                                "cardsLeft": len(game.player2.deck),
                                                                "field": game.player2.field,
                                                                "discard": game.player2.discard,
                                                                "crisis": game.player2.crisis,
                                                                "uuid": game.internal_id})
                        return "Second"
                    else:  # player 2 crisis bigger and you are player 2
                        if len(game.player2.deck) == 46:  # fresh game, should initialise
                            for q in range(5):
                                game.player2.addHandCard(game.player2.popDeck())
                            game.player2.setHandEnablePlayStatus(True)
                            game.recomputeBlockAndDialogStatus()
                            notifier = f"Your crisis has the higher number. You are going first. Drew {lookup[game.player2.hand[-1]['name']]}."
                        socketio.emit("update your state", {"username": your_username,
                                                            "hand": game.player2.hand,
                                                            "cardsLeft": len(game.player2.deck),
                                                            "field": game.player2.field,
                                                            "discard": game.player2.discard,
                                                            "crisis": game.player2.crisis,
                                                            "moveNotifier": notifier,
                                                            "uuid": game.internal_id})
                        socketio.emit("update opponent state", {"username": game.player1_username,
                                                                "cardsLeft": len(game.player2.deck),
                                                                "field": game.player2.field,
                                                                "discard": game.player2.discard,
                                                                "crisis": game.player2.crisis,
                                                                "uuid": game.internal_id})
                        return "First"
                else:
                    # todo: spectator mode
                    return "Not Playing"
        # else
        abort(Response(json.dumps({"Message": "Checking Unavailable"}), 404))


# todo add pass turn

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
