import rethinkdb as r
from nltk.stem import WordNetLemmatizer

from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

wnl = WordNetLemmatizer()


def register_intent(name, engine, *keywords, **kwargs):

    for keyword in keywords:
        engine.register_entity(keyword, name.title() + "Keyword")

    for index, values in kwargs.items():
        for value in values:
            engine.register_entity(value, name.title() + index.title())

    intent = IntentBuilder(name.title() + "Intent")\
        .require("RecycleKeyword")\
        .require(name.title() + "Keyword")

    for index in kwargs:
        intent = intent.optionally(name.title() + index.title())

    intent = intent.build()

    engine.register_intent_parser(intent)


def build_engine(rdb_conn):
    """Build a recycling intent determination engine."""

    engine = IntentDeterminationEngine()

    recycle_keywords = ["recycle", "recyclable"]

    for rk in recycle_keywords:
        engine.register_entity(rk, "RecycleKeyword")

    plastic_keywords = [item["name"] for item in r.table(
        "items").filter({"type": "plastic"}).run(rdb_conn)]

    register_intent(
        "plastic", engine,
        *plastic_keywords,
        descriptor=["number"],
        numbers=["1", "2", "3", "4", "5", "6", "7"]
    )

    glass_keywords = [item["name"] for item in r.table(
        "items").filter({"type": "glass"}).run(rdb_conn)]

    register_intent(
        "glass", engine,
        *glass_keywords
    )

    paper_keywords = [item["name"] for item in r.table(
        "items").filter({"type": "paper"}).run(rdb_conn)]

    register_intent(
        "paper", engine,
        *paper_keywords
    )

    return engine


def parse(input_text, *, engine):
    """
    Takes in input text and parses it to determine whether it is talking
    about plastic, glass, or paper, and then to find any refining things
    like the number of plastic or the type of glass.
    """

    lemmatized = ' '.join(wnl.lemmatize(word) for word in input_text.split())

    for intent in engine.determine_intent(input_text):
        if intent is not None and intent.get('confidence') > 0:
            yield intent


if __name__ == "__main__":

    tests = [
        "Can I recycle this glass bottle?",
        "Is a number 6 bottle recyclable?",
        "Can I recycle this box?"
    ]

    _engine = build_engine(r.connect(host="localhost", port=28015, db="swish"))

    for test in tests:
        print(test)
        print(list(parse(test, engine=_engine)))
        print()
