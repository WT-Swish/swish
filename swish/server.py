from collections import defaultdict

import rethinkdb as r
from flask import Flask, abort, g, jsonify, request

from .parse import build_engine, parse
from .respond import respond, respond_plastic

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


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({
        "error": 405
    }), 405


engine = build_engine(r.connect(host="localhost", port=28015, db="swish"))

RESPOND = defaultdict(lambda: respond, {
    "PlasticKeyword": respond_plastic,
    "GlassKeyword": respond,
    "PaperKeyword": respond
})


@app.route("/response", methods=("GET",))
def response():

    data = request.get_json()
    print(data)

    for intent in parse(data["text"], engine=engine):
        if intent is not None and intent.get("confidence") > 0:
            for keyword, respond_function in RESPOND.items():
                if keyword in intent:
                    return jsonify({
                        "response": respond_function(
                            intent, g.rdb_conn, keyword=keyword
                        )[1]
                    })

    return jsonify({})
