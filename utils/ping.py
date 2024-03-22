from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  data = open("web/index.html", 'r', encoding="utf-8")
  return data, 200

def run():
    app.run(host="0.0.0.0", port="8080")

def host(*, no_thread: bool = False):
    if no_thread: run()
    else:
        server = Thread(target=run)
        server.daemon = True
        server.start()
