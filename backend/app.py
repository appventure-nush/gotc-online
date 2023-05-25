from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route('/get_image')
def get_image():
    return send_file("Oran_Berry_Sprite.png", mimetype='image/png')

if __name__ == '__main__':
    app.run()
