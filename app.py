from bottle import Bottle, route, run
import threading

app = Bottle()


def t():
    import scrape


@app.route("/")
def index():
    threading.Thread(target=t)
    return "Hello, this is your Bottle app!"
