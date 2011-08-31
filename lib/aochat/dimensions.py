# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
Dimensions.
"""


class Dimension(object):
    
    def __init__(self, id, name, host, port):
        """
        Dimension.
        """
        
        self.id = id
        self.name = name
        self.host = host
        self.port = port
    
    def __repr__(self):
        return "<Dimension '%s' at '%s:%d'>" % (self.name, self.host, self.port)


DIMENSIONS = {
    0: Dimension(0, "Test-Live (Test Server)", "chat.dt.funcom.com", 7109),
    1: Dimension(1, "Atlantean (Rubi-Ka 1)", "chat.d1.funcom.com", 7101),
    2: Dimension(2, "Rimor (Rubi-Ka 2)", "chat.d2.funcom.com", 7102),
}
