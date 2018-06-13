"""
1. if data not ready, api return blank state return False 
2. if data is ready return data and change the process state to True
3. set data and query request are supposed to be bounded together
4. the request after the latest valid request is supposed to be the sign of finishing
    otherwise the problem will be unsolvable 
"""

from flask import Flask

app = Flask(__name__)

rt = "hello"
ready = False
processing = False


def setReturn(r):
    global rt
    rt = r
    global ready
    ready = True


def getState():
    """
    general state
    """
    global ready
    global processing
    if not ready:
        return False
    if processing:
        return False
    return True


@app.route("/<server>")
def hello(server):
    global processing
    global ready
    processing = False
    if not ready:
        return ""
    processing = True
    ready = False
    return rt


def run():
    app.run(port=5000)
