# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: dimensions.
"""



### CONSTANTS ##################################################################


DIMENSIONS = {
    0: {
        "name": "Test-Live (Test Server)",
        "host": "chat.dt.funcom.com",
        "port": 7109,
    },
    
    1: {
        "name": "Atlantean (Rubi-Ka 1)",
        "host": "chat.d1.funcom.com",
        "port": 7101,
    },
    
    2: {
        "name": "Rimor (Rubi-Ka 2)",
        "host": "chat.d2.funcom.com",
        "port": 7102,
    },
}



### CLASSES ####################################################################


class Dimension(object):
    """
    Anarchy Online chat protocol: dimension.
    """
    
    @staticmethod
    def get_by_id(id):
        """
        Get dimension by ID.
        """
        
        if id in DIMENSIONS:
            name = DIMENSIONS[id]["name"]
            host = DIMENSIONS[id]["host"]
            port = DIMENSIONS[id]["port"]
        else:
            raise KeyError("Invalid dimension: %s" % id)
        
        return Dimension(id, name, host, port)
    
    def __init__(self, id, name, host, port):
        self.id = id
        self.name = name
        self.host = host
        self.port = port
