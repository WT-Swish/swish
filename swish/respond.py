import random

import rethinkdb as r

RECYCLABLE_PLASTICS = (1, 2, 3, 4, 5, 7)


def respond_plastic(intent, rdb_conn, *, keyword="PlasticKeyword"):

    item, response = respond(
        intent, rdb_conn, keyword=keyword,
        function=lambda item: item["number"] in RECYCLABLE_PLASTICS
    )

    return response + " Number {n} plastic is {r}recyclable.".format(
        n=item["number"],
        r="" if item["number"] in RECYCLABLE_PLASTICS else "not "
    )


def respond(intent, rdb_conn, *, keyword, function=None):

    if function is None:
        function = lambda item: item["recyclable"]

    item = next(r.table("items").filter({
        "name": intent[keyword]
    }).run(rdb_conn))

    if "responses" in item:
        return item, random.choice(item["responses"])

    return item, r.table("responses").filter({
        "is_recyclable": function(item)
    }).sample(1).run(rdb_conn)[0]["response"].format(item=item["name"])
