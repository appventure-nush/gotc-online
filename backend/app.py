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

from classes import *
import lists
from Game import Game

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "runtime.log"


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

        # check for invalid usernames
        if proposed_username == "":
            response["text"] = "Blank usernames are not allowed. Not signed in."
            return response
        if proposed_username in ("NO GAME INITIATED",):
            # this username is the placeholder for invalid/uninitiated game boards
            response["text"] = "This username is not allowed. Not signed in."
            return response


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
    quality = request.args.get('quality')
    if quality == "png":
        return send_file(f"card_art/png/{cardname}.png", mimetype='image/png')
    else:
        return send_file(f"card_art/jpeg/{cardname}.jpg", mimetype='image/jpeg')


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
    return str(len(lists.STANDARD_DECK))


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
                game.recomputeBlockAndDialogStatus()
                if game.player1_username == request_username:
                    response["hand"] = game.player1.hand
                elif game.player2_username == request_username:
                    response["hand"] = game.player2.hand
                return response
        # else
        abort(Response(json.dumps({"Message": "Hand Unavailable"}), 404))


@app.route('/get_opponent_hand', methods=["POST"])
@cross_origin()
def get_opponent_hand():
    # return opponent's hand for the user whose LSK and username fit
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
                game.recomputeBlockAndDialogStatus()
                if game.player1_username == request_username:
                    response["hand"] = game.player2.hand
                elif game.player2_username == request_username:
                    response["hand"] = game.player1.hand
                return response
        # else
        abort(Response(json.dumps({"Message": "Hand Unavailable"}), 404))


@app.route('/play_hand', methods=["POST"])
@cross_origin()
def play_hand():
    # play a card from hand for the user whose LSK and username fit
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
        "needDiscard": False,
        "winThisTurn": False
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if (
                        (game.player1_username == request_username) and
                        ((hand_index < 0) or (hand_index >= len(game.player1.hand)))
                ) or (
                        (game.player2_username == request_username) and
                        ((hand_index < 0) or (hand_index >= len(game.player2.hand)))
                ):
                    abort(Response(json.dumps({"Message": "Card Index Out Of Range"}), 422))
                return game.play_hand(socketio, 1 if game.player1_username == request_username else 2, hand_index, request)
        # else
        abort(Response(json.dumps({"Message": "Cannot Play Hand"}), 404))


@app.route('/discard_hand', methods=["POST"])
@cross_origin()
def discard_hand():
    # discard a card from hand for the user whose LSK and username fit
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
        "nextTurn": False,
        "winThisTurn": False
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if (
                    (game.player1_username == request_username) and
                    ((hand_index < 0) or (hand_index >= len(game.player1.hand)))
                ) or (
                    (game.player2_username == request_username) and
                    ((hand_index < 0) or (hand_index >= len(game.player2.hand)))
                ):
                        abort(Response(json.dumps({"Message": "Card Index Out Of Range"}), 422))
                return game.discard_hand(socketio, 1 if game.player1_username == request_username else 2, hand_index)

        # else
        abort(Response(json.dumps({"Message": "Cannot Play Hand"}), 404))


@app.route('/pass_turn', methods=["POST"])
@cross_origin()
def pass_turn():
    # pass turn for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    # response = {"hand": [], "discard": [], "cardsLeft": 0, "nextTurn": False, "winThisTurn": False}
    # response is constructed in the game pass turn function
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                return game.pass_turn(socketio, 1 if game.player1_username == request_username else 2)
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


@app.route('/write_storage', methods=["POST"])
@cross_origin()
def write_storage():
    # make a new shuffled deck for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    game_id = request.json['game_id']
    response = {}
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == your_username:
                    game.player1.storage |= request.json["storage"]
                elif game.player2_username == your_username:
                    game.player2.storage |= request.json["storage"]
                return response
        # else
        abort(Response(json.dumps({"Message": "Updating Storage Unavailable"}), 404))


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
                return game.game_init(socketio, your_username)
        # else
        abort(Response(json.dumps({"Message": "Checking Unavailable"}), 404))


@app.route('/get_my_running_games', methods=["POST"])
@cross_origin()
def get_my_running_games():
    # Initialises the game for the user whose LSK and username fit. 1 person per call, called 2 times.
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                list_of_my_games : list[[str,str]] = []
                for g in games.values():
                    if (i.name == g.player1.name) or (i.name == g.player2.name):
                        list_of_my_games.append([g.internal_id, g.player1.name if i.name != g.player1.name else g.player2.name, g.init_time.isoformat(timespec="seconds")])
                return {"games":list_of_my_games}

        # else
        abort(Response(json.dumps({"Message": "Checking Unavailable"}), 404))


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
