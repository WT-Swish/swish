import json
import sys

from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

engine = IntentDeterminationEngine()

recyclable_keyword = [
    "recyclable",
    "recycle",
    "recycling"
]

for keyword in recyclable_keyword:
    engine.register_entity(keyword, "RecyclableKeyword")

materials = [
    "plastic",
    "paper",
    "metal",
    "glass"
]

for keyword in materials:
    engine.register_entity(keyword, "RecyclableMaterials")

plastic_numbers = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7"
]

for number in plastic_numbers:
    engine.register_entity(number, "PlasticNumber")

weather_intent = IntentBuilder("RecyclableIntent")\
    .require("RecyclableKeyword")\
    .require("RecyclableMaterials")\
    .optionally("PlasticNumber")\
    .build()

engine.register_intent_parser(weather_intent)


def parse_intent(phrase):
    return engine.determine_intent(phrase)

if __name__ == "__main__":
    for intent in parse_intent(' '.join(sys.argv[1:])):
        if intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
