import random
import secrets
import time
import threading
from datetime import datetime
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

LOG_FILE = "runtime.log"


logged_in = []


class User:
    def __init__(self, name, last_checkin, login_session_key):
        self.name = name
        self.last_checkin = last_checkin
        self.login_session_key = login_session_key

    def __str__(self):
        return self.name + " | " + str(self.last_checkin)


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
            if(curr_time - i.last_checkin > 10*60):  #if not checked in for more than 10*60 secs = 10 mins
                users_to_log_off.append(i)
        for i in users_to_log_off:
            logged_in.remove(i)
        writeLog("after clearing cycle @" + str(curr_time) + ": {")
        writeLog(usersListString())
        writeLog("}")
        time.sleep(2*60) # do the check ever 2 mins


log_in_clearer_daemon = threading.Thread(target=clear_inactive_users_from_login, daemon=True)
log_in_clearer_daemon.start()


@app.route('/')
def main():  # put application's code here
    return 'Hello World!'


@app.route('/calculate',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
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
        if(i.name == username) and secrets.compare_digest(sent_login_sesh_key, i.login_session_key):
            target_user_logged_in = True
            break
    #if indeed logged in then do the get counter stuff
    if(target_user_logged_in):
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            if username in data:
                return str(data[username])
            else:
                return "0"
    return "end of function"  # every method should return something


@app.route('/sign_in',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_in():
    proposed_username = request.json['proposed_username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text" : "PLACEHOLDER",
        "confirmed_username" : "",
        "login_session_key": "0",
        "login_success" : False
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
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
        #else
        login_session_key = secrets.token_hex()
        logged_in.append(User(proposed_username, int(datetime.now().timestamp()), login_session_key))
        response["text"] = "Logged in as " + proposed_username
        response["confirmed_username"] = proposed_username
        response["login_session_key"] = login_session_key
        response["login_success"] = True
        writeLog(usersListString())
        return response


@app.route('/sign_out',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_out():
    username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text" : "PLACEHOLDER",
        "signout_success" : False
    }

    if request.method == "POST":
        users_to_remove = []
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == username) and keys_equal:
                users_to_remove.append(i)
        if(len(users_to_remove) > 0):
            for i in users_to_remove:
                logged_in.remove(i)
            response["text"] = "signed out successfully"
            response["signout_success"] = True
        else:
            response["text"] = "nobody was signed out"
            response["signout_success"] = False
        return response


@app.route('/user_activity_ping',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def user_activity_ping():
    pinger_username = request.json['username']
    sent_login_sesh_key = request.json['login_session_key']
    response = {
        "text" : "PLACEHOLDER",
        "still_active" : False
    }
    if request.method == "POST":
        for i in logged_in:
            keys_equal = secrets.compare_digest(i.login_session_key, sent_login_sesh_key)
            if (i.name == pinger_username) and keys_equal:
                i.last_checkin = int(datetime.now().timestamp())
                response["text"] = "activity sucessfully registered"
                response["still_active"] = True
                return response
        #else
        response["text"] = "You were signed out due to inactivity!"
        response["still_active"] = False
        return response


@app.route('/activity_status_request',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def activity_status_request():
    pinger_username = request.json['username']
    response = {
        "text" : "PLACEHOLDER",
        "still_active" : False
    }
    if request.method == "POST":
        for i in logged_in:
            if i.name == pinger_username:
                response["text"] = "account still logged in"
                response["still_active"] = True
                return response
        #else
        response["text"] = "You were signed out due to inactivity!"
        response["still_active"] = False
        return response


@app.route('/get_image')
def get_image():
    return send_file("Oran_Berry_Sprite.png", mimetype='image/png')


if __name__ == '__main__':
    app.run()
