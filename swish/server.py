import rethinkdb as r
from flask import Flask, abort, g, jsonify, request

from .parse import parse_intent

app = Flask(__name__)


@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host="localhost", port=28015)
    except r.RqlDriverError:
        abort(503, "Database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error": 404
    }), 404


@app.route("/response")
def response():

    data = request.get_json()
    tables = r.db("items").table_list().run(g.rdb_conn)

    for intent in parse_intent(data["text"]):
        if intent.get("confidence") > 0:
            if intent.get("RecyclableMaterials") in tables:
                return jsonify(list(r.db("items").table("plastic").run(g.rdb_conn)))

    abort(404)
