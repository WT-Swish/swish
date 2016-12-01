import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine


def parse(input_text):
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
        engine.regiester_entity(gk, "GlassKeyword")

        glass_descriptor = [ "bottle", "light bulb", "broken", "mirror", "window", "ceramic" ]

    for gd in glass_descriptor:
        engine.register_entity(gd, "GlassDescriptor")

###########
## Paper ##
###########

    paper_keywords = [ "paper", "sheets", "carton" , "cardboard", "box" ]

    for pk in cardboard_keywords:
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

    glass_intent = IntentBuilder("GlassIntent")\
                   .require("RecycleKeyword")\
                   .require("GlassKeyword")\
                   .optionally("GlassDescriptor")\
                   .build()

    paper_intent = IntentBuilder("PaperIntent")\
                   .require("RecycleKeyword")\
                   .require("PaperKeyword")\
                   .build()


##############################
##############################
#### Parsing For Keywords ####
##############################
##############################
