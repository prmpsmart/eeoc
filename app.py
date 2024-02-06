from bottle import Bottle
import threading

app = Bottle()


def t():
    import scrape


@app.route("/")
def index():
    threading.Thread(target=t).start()
    return "Hello, this is your Bottle app!"
