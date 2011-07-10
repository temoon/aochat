# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
Game data.
"""


TEXTS = {}


def load_texts(filename):
    """
    Load extended messages and references from data file.
    """
    
    global TEXTS
    
    TEXTS = {}
    
    data = file(filename, "rb")
    
    for entry in data:
        category, instance, message = entry.rstrip("\r\n").split("\t", 2)
        
        category = int(category)
        instance = int(instance)
        
        if category in TEXTS:
            TEXTS[category][instance] = message
        else:
            TEXTS[category] = {instance: message}


def get_text(category, instance):
    """
    Get text with category and instance.
    """
    
    if category not in TEXTS or instance not in TEXTS[category]:
        raise ValueError("unknown text category=%d instance=%d" % (category, instance,))
    else:
        return TEXTS[category][instance]

