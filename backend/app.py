from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/')
def main():  # put application's code here
    return 'Hello World!'

@app.route('/hw')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/get_image')
def get_image():
    return send_file("Oran_Berry_Sprite.png", mimetype='image/png')

if __name__ == '__main__':
    app.run()
