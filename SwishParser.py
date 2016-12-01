import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine


def parse(input_text):
    """
    Takes in input text and parses it to determine whether it is talking
    about plastic, glass, or paper, and then to find any refining things
    like the number of plastic or the type of glass.

    """

    tokenizer = EnglishTokenizer()
    trie = Trie()
    tagger = EntityTagger(trie, tokenizer)
    parser = Parser

    engine = IntentDeterminationEngine()


################################
################################
#### Keyword Initialization ####
################################
################################

    recycle_keywords = ["recycle", "recycleable"]

    for rk in recycle_keywords:
        engine.register_entity(rk, "RecycleKeyword")
        
##############
## Plastics ##
##############

    plastic_keywords = [ "plastic", "bottle" ]

    for pk in plastic_keywords:
        engine.register_entity(pk, "PlasticKeyword")

    plastic_descriptor = [ "number" ]
        
    for pd in plastic_descriptor:
        engine.register_entity(pd, "PlasticDescriptor")

    plastic_numbers = [ "1", "2", "3", "4", "5", "6", "7" ]

    for pn in plastic_numbers:
        engine.register_entity(pn, "PlasticNumber")

###########
## Glass ##
###########

    glass_keywords = [ "glass" ]

    for gk in glass_keywords:
        engine.register_entity(gk, "GlassKeyword")

        glass_descriptor = [ "bottle", "light bulb", "broken", "mirror", "window", "ceramic" ]

    for gd in glass_descriptor:
        engine.register_entity(gd, "GlassDescriptor")

###########
## Paper ##
###########

    paper_keywords = [ "paper", "sheets", "carton" , "cardboard", "box" ]

    for pk in paper_keywords:
        engine.register_entity(pk, "PaperKeyword")

############################
############################
####  Creating Intents  ####
############################
############################

    plastic_intent = IntentBuilder("PlasticIntent")\
                     .require("RecycleKeyword")\
                     .require("PlasticKeyword")\
                     .optionally("PlasticDescriptor")\
                     .optionally("PlasticNumber")\
                     .build()

    engine.register_intent_parser(plastic_intent)

    glass_intent = IntentBuilder("GlassIntent")\
                   .require("RecycleKeyword")\
                   .require("GlassKeyword")\
                   .optionally("GlassDescriptor")\
                   .build()

    engine.register_intent_parser(glass_intent)

    paper_intent = IntentBuilder("PaperIntent")\
                   .require("RecycleKeyword")\
                   .require("PaperKeyword")\
                   .build()

    engine.register_intent_parser(paper_intent)
    

##############################
##############################
#### Parsing For Keywords ####
##############################
##############################
    intents = []

    for intent in engine.determine_intent(input_text):
        if intent.get('confidence') > 0:
            intents.append(intent)
            #print(json.dumps(intent, intent=4)) ATTN: Strange error here. I returned the dictionaries instead.

    return intents


## Examples: Not necessary for the rest of the code

print(parse("Can I recycle this glass bottle?"))

print(parse("Can I recycle this plastic bottle?"))

print(parse("Can I recycle this box?"))
