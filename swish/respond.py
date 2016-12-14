import rethinkdb as r

RECYCLABLE_PLASTICS = (1, 2, 3, 4, 5, 7)


def respond_plastic(intent, rdb_conn, *, keyword="PlasticKeyword"):

    item = next(r.table("items").filter({
        "name": intent[keyword]
    }).run(rdb_conn))

    return r.table("responses").filter({
        "is_recyclable": item["number"] in RECYCLABLE_PLASTICS
    }).sample(1).run(rdb_conn)[0]["response"].format(
        item=item["name"]
    ) + " Number {n} plastic is {r}recyclable.".format(
        n=item["number"],
        r="" if item["number"] in RECYCLABLE_PLASTICS else "not "
    )


def respond(intent, rdb_conn, *, keyword):

    item = next(r.table("items").filter({
        "name": intent[keyword]
    }).run(rdb_conn))

    return r.table("responses").filter({
        "is_recyclable": item["recyclable"]
    }).sample(1).run(rdb_conn)[0]["response"].format(item=item["name"])
