import time
import threading
from datetime import datetime
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


logged_in = []

class User:
    def __init__(self, name, last_checkin):
        self.name = name
        self.last_checkin = last_checkin

    def __str__(self):
        return self.name + " | " + str(self.last_checkin)

def printUsers():
    for i in logged_in:
        print(i)

def clear_inactive_users_from_login():
    while True:
        users_to_log_off = []
        curr_time = int(datetime.now().timestamp())
        for i in logged_in:
            if(curr_time - i.last_checkin > 60):  #if not checked in for more than 10*60 secs = 10 mins
                users_to_log_off.append(i)
        for i in users_to_log_off:
            logged_in.remove(i)
        print("after clearing cycle @" + str(curr_time) + ":")
        printUsers()
        print("===")
        time.sleep(30) # do the check ever 2 mins

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
    if request.method == "POST":
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        with open("data.json", "w") as data_file:
            data[request.json["username"]] = request.json["value"]
            json.dump(data, data_file)
        return "success"  # every method should return something

@app.route('/get_counter', methods=['POST'])
@cross_origin()
def get_counter():
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        if request.json["username"] in data:
            return str(data[request.json["username"]])
        else:
            return "0"



@app.route('/sign_in',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def sign_in():
    proposed_username = request.json['proposed_username']
    response = {
        "text" : "PLACEHOLDER",
        "confirmed_username" : "",
        "login_success" : False
    }
    if request.method == "POST":
        for i in logged_in:
            if i.name == proposed_username:
                response["text"] = "This username is already logged in"
                printUsers()
                return response
        #else
        logged_in.append(User(proposed_username, int(datetime.now().timestamp())))
        response["text"] = "Logged in as " + proposed_username
        response["confirmed_username"] = proposed_username
        response["login_success"] = True
        printUsers()
        return response

@app.route('/user_activity_ping',methods=['POST'])
#we need this cross-origin stuff for post requests since this is how people decided the internet would work
@cross_origin()
def user_activity_ping():
    pinger_username = request.json['username']
    response = {
        "text" : "PLACEHOLDER",
        "still_active" : False
    }
    if request.method == "POST":
        for i in logged_in:
            if i.name == pinger_username:
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
