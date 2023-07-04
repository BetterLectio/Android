from threading import Thread
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "<p><strong>BetterLectio Mobile</strong></p><br/><p>Dette er en test for at se om Python med Flask virker på native Android.<p/>"

def thread():
    app.run(host="0.0.0.0")

def main():
    Thread(target=thread).start()
