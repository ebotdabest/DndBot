from threading import Thread
from flask import Flask

app = Flask('')

@app.route("/")
def index():
  return "Hello there!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
