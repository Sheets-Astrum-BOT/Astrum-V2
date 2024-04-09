from flask import Flask
from threading import Thread
import logging 

logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR) 
app = Flask('')

@app.route('/')
def home():
    return "Bot Is Up And Running"

def run():
  app.run(port=8000)

def KeepAlive():
    t = Thread(target=run)
    t.start()