import rethinkdb as r
from flask import Flask, abort, g, jsonify, request

from .parse import build_engine, parse

app = Flask(__name__)


@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host="localhost", port=28015, db="swish")
    except r.RqlDriverError:
        abort(503, "Database connection could be established.")


@app.teardown_request
def teardown_request(_):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.errorhandler(404)
def page_not_found(_):
    return jsonify({
        "error": 404
    }), 404

INTENTS = {
    "PlasticIntent": "plastic",
    "PaperIntent": "paper",
    "GlassIntent": "glass"
}

engine = build_engine(r.connect(host="localhost", port=28015, db="swish"))


@app.route("/response")
def response():

    data = request.get_json()

    result = []

    for intent in parse(data["text"], engine=engine):
        if intent is not None and intent.get("confidence") > 0:
            result.append(intent)  # TODO

    return jsonify(result)
