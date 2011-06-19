# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: characters.
"""


class Character(object):
    
    def __init__(self, id, name, level, online = False):
        """
        Game character.
        """
        
        self.id = long(id)
        self.name = str(name)
        self.level = long(level)
        self.online = long(online)
    
    def __repr__(self):
        return "<Character [%s] %s (%d), level %d>" % ("Online" if self.online else "Offline", self.name, self.id, self.level,)
