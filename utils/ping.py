from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return """
Isobot lazer is online. Redirecting to homepage...
<script>window.location.replace("https://PyBotDevs.github.io/isobot-lazer")</script>
""", 200

def run():
    app.run(host="0.0.0.0", port="8080")

def host():
    server = Thread(target=run)
    server.start()
