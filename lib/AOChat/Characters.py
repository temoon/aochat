# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: characters.
"""



### CLASSES ####################################################################


class Character(object):
    """
    Anarchy Online chat protocol: character.
    """
    
    def __init__(self, id, name, level, online = False, ai_level = None, org_id = None, org_name = None, org_rank = None):
        # Main attributes
        self.id = id
        self.name = name
        self.level = level
        self.online = online
        
        # Extended attributes
        self.ai_level = ai_level;
        self.org_id = org_id;
        self.org_name = org_name;
        self.org_rank = org_rank;
    
    def __str__(self):
        return "<AO character ID=%s Name=%s Level=%s [%s]>" (self.id, self.name, self.level, "Online" if self.online else "Offline")
