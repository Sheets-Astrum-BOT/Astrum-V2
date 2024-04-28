
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;">
    <iframe width="100%" height="100%" src="https://astrumbot.vercel.app/" frameborder="0" allowfullscreen></iframe>
  </body>'''


def run():
    app.run(host='0.0.0.0', port=10403)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()