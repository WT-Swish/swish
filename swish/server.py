import json

import rethinkdb as r
from flask import Flask, request

from .recognize import get_result_response

app = Flask(__name__)


@app.route("/response")
def response():
    data = request.get_json()
    return json.dumps(list(r.db("items").table("plastic").run()))
