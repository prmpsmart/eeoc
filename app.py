from bottle import Bottle
import threading

app = Bottle()


def t():
    # trunk-ignore(ruff/F401)
    import scrape


@app.route("/")
def index():
    threading.Thread(target=t).start()
    return "Hello, this is your Bottle app!"
