import hashlib
import json
import os
import secrets
import threading
import time
import uuid
from datetime import datetime

from flask import Flask, request, send_file, abort, Response, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO

import lists
from Game import Game
from classes import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "runtime.log"

logged_in: list[User] = []
queue: list[User] = []
games: dict[str, Game] = {}

# create account files if not present
try:
    os.mkdir("./local_data_files")
except FileExistsError:
    pass
try:
    with open("local_data_files/accounts.json", "x"):
        pass
    with open("local_data_files/accounts.json", "w") as w:
        w.write("{}")
except FileExistsError:
    pass
try:
    with open("local_data_files/data.json", "x"):
        pass
    with open("local_data_files/data.json", "w") as w:
        w.write("{}")
except FileExistsError:
    pass


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
            with open("local_data_files/data.json", "r") as data_file:
                data = json.load(data_file)
            with open("local_data_files/data.json", "w") as data_file:
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
        with open("local_data_files/data.json", "r") as data_file:
            data = json.load(data_file)
            if username in data:
                return str(data[username])
            else:
                return "0"
    return "end of function"  # every method should return something


@app.route('/create_account', methods=['POST'])
@cross_origin()
def create_account():
    proposed_username = request.json['proposed_username']
    proposed_password = request.json['proposed_password']
    response = {
        "text": "PLACEHOLDER",
        "confirmed_username": "",
        "account_creation_success": False
    }
    if request.method == "POST":

        if proposed_username == "":
            response["text"] = "Blank usernames are not allowed. Account not created."
            return response
        if proposed_password == "":
            response["text"] = "Blank passwords are not allowed. Account not created."
            return response

        with open("local_data_files/accounts.json", "r") as accs_file:
            accounts = json.load(accs_file)
            for a in accounts:
                if a == proposed_username:
                    response["text"] = "Account already exists. Account not created."
                    response["confirmed_username"] = proposed_username
                    return response
        # if the account doesn't exist
        with open("local_data_files/accounts.json", "w") as accs_file:
            accounts[proposed_username] = {
                "username": proposed_username,
                "password": hashlib.sha256(bytes(proposed_password, 'utf-8')).hexdigest(),
                "losseschallenge": 0,
                "drawschallenge": 0,
                "winschallenge": 0,
                "lossesrandom": 0,
                "drawsrandom": 0,
                "winsrandom": 0,
            }
            json.dump(accounts, accs_file)
            response["text"] = "Account successfully created"
            response["account_creation_success"] = True
        return response


@app.route('/delete_account', methods=['POST'])
@cross_origin()
def delete_account():
    username = request.json['username']
    password = request.json['password']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text": "PLACEHOLDER",
        "wrong_password": False,
        "account_deletion_success": False
    }
    if request.method == "POST":
        account_to_delete = None
        user_to_delete = None
        with open("local_data_files/accounts.json", "r") as accs_file:
            accounts = json.load(accs_file)
            if username in accounts:
                a = accounts[username]
                # account exists
                # check if account signed in
                for u in logged_in:
                    keys_equal = False if (type(sent_login_sesh_key) is not str) else secrets.compare_digest(
                        u.login_session_key, sent_login_sesh_key)
                    if u.name == a["username"] and keys_equal:
                        if a["password"] == hashlib.sha256(bytes(password, 'utf-8')).hexdigest():
                            # password is correct
                            account_to_delete = a
                            user_to_delete = u
                            break
                        response["text"] = "Wrong password. Account not deleted."
                        response["wrong_password"] = True
                        return response
            else:
                # else, User is not logged in
                response["text"] = "User is not logged in. Account not deleted."
                return response
        # if account to delete exists
        if account_to_delete is not None:
            with open("local_data_files/accounts.json", "w") as accs_file:
                # all checks out, start deletion process
                # first sign out
                if user_to_delete in queue:
                    queue.remove(user_to_delete)
                logged_in.remove(user_to_delete)
                # then erase from accounts
                accounts.pop(user_to_delete.name)
                # then delete from accounts file
                json.dump(accounts, accs_file)
                # return success
                response["text"] = "Account successfully deleted."
                response["account_deletion_success"] = True
                return response
        # if the account doesn't exist (& other errors)
        response["text"] = "Account does not exist. Account not deleted."
        response["account_deletion_success"] = False
        return response


@app.route('/sign_in', methods=['POST'])
# we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_in():
    proposed_username = request.json['proposed_username']
    proposed_password = request.json['proposed_password']
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

        # check if user exists
        with open("local_data_files/accounts.json", "r") as accs_file:
            account_exists = False
            accounts = json.load(accs_file)
            if proposed_username in accounts:
                a = accounts[proposed_username]
                # check if password is wrong
                if a["password"] != hashlib.sha256(bytes(proposed_password, 'utf-8')).hexdigest():
                    response["text"] = "Password is incorrect."
                    return response
                # else go on
                account_exists = True
                losseschallenge = a["losseschallenge"]
                drawschallenge = a["drawschallenge"]
                winschallenge = a["winschallenge"]
                lossesrandom = a["lossesrandom"]
                drawsrandom = a["drawsrandom"]
                winsrandom = a["winsrandom"]
            if not account_exists:
                response["text"] = "There is no account with this username. Please create an account first."
                return response

        for i in logged_in:

            keys_equal = False if (type(sent_login_sesh_key) is not str) else secrets.compare_digest(
                i.login_session_key, sent_login_sesh_key)

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
        logged_in.append(User(proposed_username, int(datetime.now().timestamp()), login_session_key,
                              winsrandom, drawsrandom, lossesrandom, winschallenge, drawschallenge, losseschallenge))
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
                    games[random_uuid] = Game(opponent.name, username, random_uuid, "challenge")
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
                games[random_uuid] = Game(opponent.name, username, random_uuid, "random")
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
    # response = {"cardPlayed": "", "hand": [], "discard": [], "cardsLeft": 0, "needDiscard": False, "winThisTurn": False}
    # response is constructed in the game play hand function
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
                # add and save winners and losers (or drawers)
                ret = game.play_hand(socketio, 1 if game.player1_username == request_username else 2, hand_index,
                                     request)
                if ret["winThisTurn"]:
                    with open("local_data_files/accounts.json", "r") as accs_file:
                        accounts = json.load(accs_file)
                    with open("local_data_files/accounts.json", "w") as accs_file:
                        if game.winner == "":
                            accounts[game.player1_username]["draws" + game.gametype] += 1
                            accounts[game.player2_username]["draws" + game.gametype] += 1
                        else:
                            accounts[game.winner]["wins" + game.gametype] += 1
                            accounts[
                                game.player1_username if game.winner == game.player2_username else game.player2_username
                            ]["losses" + game.gametype] += 1
                        json.dump(accounts, accs_file)
                return ret
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
    # response = {"cardPlayed": "", "hand": [], "discard": [], "cardsLeft": 0, "nextTurn": False, "winThisTurn": False}
    # response is constructed in the game discard hand function
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
                # add and save winners and losers (or drawers)
                ret = game.discard_hand(socketio, 1 if game.player1_username == request_username else 2, hand_index)
                if ret["winThisTurn"]:
                    with open("local_data_files/accounts.json", "r") as accs_file:
                        accounts = json.load(accs_file)
                    with open("local_data_files/accounts.json", "w") as accs_file:
                        if game.winner == "":
                            accounts[game.player1_username]["draws" + game.gametype] += 1
                            accounts[game.player2_username]["draws" + game.gametype] += 1
                        else:
                            accounts[game.winner]["wins" + game.gametype] += 1
                            accounts[
                                game.player1_username if game.winner == game.player2_username else game.player2_username
                            ]["losses" + game.gametype] += 1
                        json.dump(accounts, accs_file)
                return ret

        # else
        abort(Response(json.dumps({"Message": "Cannot Discard Hand"}), 404))


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
                # add and save winners and losers (or drawers)
                ret = game.pass_turn(socketio, 1 if game.player1_username == request_username else 2)
                if ret["winThisTurn"]:
                    with open("local_data_files/accounts.json", "r") as accs_file:
                        accounts = json.load(accs_file)
                    with open("local_data_files/accounts.json", "w") as accs_file:
                        if game.winner == "":
                            accounts[game.player1_username]["draws" + game.gametype] += 1
                            accounts[game.player2_username]["draws" + game.gametype] += 1
                        else:
                            accounts[game.winner]["wins" + game.gametype] += 1
                            accounts[
                                game.player1_username if game.winner == game.player2_username else game.player2_username
                            ]["losses" + game.gametype] += 1
                        json.dump(accounts, accs_file)
                return ret
        # else
        abort(Response(json.dumps({"Message": "Cannot Pass Turn"}), 404))


@app.route('/forfeit', methods=["POST"])
@cross_origin()
def forfeit():
    # forfeit game for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    # response = {"hand": [], "discard": [], "cardsLeft": 0, "nextTurn": False, "winThisTurn": False}
    # response is constructed in the game forfeit function
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                # add and save winners and losers (guaranteed, since this is forfeit)
                ret = game.forfeit(socketio, 1 if game.player1_username == request_username else 2)
                if ret["winThisTurn"]:
                    with open("local_data_files/accounts.json", "r") as accs_file:
                        accounts = json.load(accs_file)
                    with open("local_data_files/accounts.json", "w") as accs_file:
                        accounts[game.winner]["wins" + game.gametype] += 1
                        accounts[
                            game.player1_username if game.winner == game.player2_username else game.player2_username
                        ]["losses" + game.gametype] += 1
                        json.dump(accounts, accs_file)
                return ret
        # else
        abort(Response(json.dumps({"Message": "Cannot Forfeit"}), 404))


@app.route('/timeout', methods=["POST"])
@cross_origin()
def timeout():
    # for the user whose LSK and username fit, they lose by timeout
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json["request_username"]
    game_id = request.json['game_id']
    # response = {"hand": [], "discard": [], "cardsLeft": 0, "nextTurn": False, "winThisTurn": False}
    # response is constructed in the game timeout function
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                # add and save winners and losers (guaranteed, since this is timeout)
                ret = game.timeout(socketio, 1 if game.player1_username == request_username else 2)
                if ret["winThisTurn"]:
                    with open("local_data_files/accounts.json", "r") as accs_file:
                        accounts = json.load(accs_file)
                    with open("local_data_files/accounts.json", "w") as accs_file:
                        accounts[game.winner]["wins" + game.gametype] += 1
                        accounts[
                            game.player1_username if game.winner == game.player2_username else game.player2_username
                        ]["losses" + game.gametype] += 1
                        json.dump(accounts, accs_file)
                return ret
        # else
        abort(Response(json.dumps({"Message": "Cannot Forfeit"}), 404))


@app.route('/get_discard', methods=["POST"])
@cross_origin()
def get_discard():
    # gets discard for the user whose LSK and username fit
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
    # saves data to game storage for the user whose LSK and username fit
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


@app.route('/update_timer', methods=["POST"])
@cross_origin()
def update_timer():
    # update timer (on specified side) for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    request_username = request.json['request_username']
    game_id = request.json['game_id']
    response = {}
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                game: Game = games[game_id]
                if game.player1_username == request_username:
                    socketio.emit("update opponent state", {
                        "username": game.player2_username,
                        "uuid": game_id,
                        "timer": game.player1.timer-request.json["delta"]
                    })
                    if "store" in request.json and request.json["store"]:
                        game.player1.timer -= request.json["delta"]
                elif game.player2_username == request_username:
                    socketio.emit("update opponent state", {
                        "username": game.player1_username,
                        "uuid": game_id,
                        "timer": game.player2.timer-request.json["delta"]
                    })
                    if "store" in request.json and request.json["store"]:
                        game.player2.timer -= request.json["delta"]
                return response
        # else
        abort(Response(json.dumps({"Message": "Updating Storage Unavailable"}), 404))


@app.route('/get_my_running_games', methods=["POST"])
@cross_origin()
def get_my_running_games():
    # Gets all running games for the user whose LSK and username fit
    sent_login_sesh_key = request.json['login_session_key']
    your_username = request.json['username']
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == your_username) and keys_equal:
                list_of_my_games: list[[str, str]] = []
                for g in games.values():
                    if g.winner is None and ((i.name == g.player1.name) or (i.name == g.player2.name)):
                        list_of_my_games.append([g.internal_id,
                                                 g.player1.name if i.name != g.player1.name else g.player2.name,
                                                 g.init_time.isoformat(timespec="seconds")])
                # currently: only unfinished games are returned
                # finished games are kept in games but not deleted, this behaviour is to be changed
                return {"games": list_of_my_games}  # todo: create a separate section for won games

        # else
        abort(Response(json.dumps({"Message": "Checking Unavailable"}), 404))


@app.route('/get_ladder', methods=["GET"])
def get_ladder():
    with open("local_data_files/accounts.json", "r") as accs_file:
        accounts = json.load(accs_file)
    for a in accounts:
        accounts[a].pop("password")  # do not send password hashes

    # arbitrary sort order of highest percentage of wins, tiebreak by earliest created account
    # todo better sort order, more stats like created date, include computer
    def sortorder(element):
        if element["winschallenge"] + element["drawschallenge"] + element["losseschallenge"] \
                + element["winsrandom"] + element["drawsrandom"] + element["lossesrandom"] == 0:
            return 0
        else:
            return (element["winschallenge"] + element["winsrandom"]) / \
                (element["winschallenge"] + element["drawschallenge"] + element["losseschallenge"]
                 + element["winsrandom"] + element["drawsrandom"] + element["lossesrandom"])

    return list(sorted(accounts.values(), key=sortorder, reverse=True))


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
