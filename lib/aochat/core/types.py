# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
Data types.
"""


import struct


class Integer(long):
    """
    Unsigned 32-bit integer.
    """
    
    def __new__(Class, x = 0L, base = 10):
        return long.__new__(Class, str(x), base)
    
    def __init__(self, x = 0L, base = 10):
        if self > 0xFFFFFFFFL:
            raise ValueError("out of range")
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        return struct.pack(">I", self)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        if len(data) < 4:
            raise ValueError("too short data")
        
        return Class(struct.unpack(">I", data[:4])[0]), data[4:]


class String(str):
    """
    16-bit length string.
    """
    
    def __new__(Class, x = ""):
        return str.__new__(Class, x or "")
    
    def __init__(self, x = ""):
        if len(self) > 0xFFFF:
            raise ValueError("too long string")
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        return struct.pack(">H", len(self)) + self
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        if len(data) < 2:
            raise ValueError("too short data")
        
        length, data = struct.unpack(">H", data[:2])[0], data[2:]
        
        return Class(data[:length]), data[length:]


class ChannelID(long):
    """
    Channel ID.
    """
    
    def __new__(Class, x = 0L, base = 10):
        return long.__new__(Class, str(x), base)
    
    def __init__(self, x = 0L, base = 10):
        if self > 0xFFFFFFFFFFL:
            raise ValueError("out of range")
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        return struct.pack(">BI", self >> 32, self & 0xFFFFFFFFL)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        if len(data) < 5:
            raise ValueError("too short data")
        
        a, b = struct.unpack(">BI", data[:5])
        
        return Class((a << 32) + b), data[5:]


class Tuple(tuple):
    """
    Tuple of <Type>s.
    """
    
    def __new__(Class, Type, sequence = ()):
        return tuple.__new__(Class, map(Type, sequence))
    
    def __init__(self, Type, sequence = ()):
        if len(self) > 0xFFFF:
            raise ValueError("too long sequence")
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        return struct.pack(">H", len(self)) + "".join(map(lambda item: item.pack(), self))
    
    @staticmethod
    def unpack(Type, data):
        """
        Unpack from binary data.
        """
        
        if len(data) < 2:
            raise ValueError("too short data")
        
        count, data = struct.unpack(">H", data[:2])[0], data[2:]
        
        items = []
        
        for i in range(count):
            item, data = Type.unpack(data)
            items.append(item)
        
        return items, data


class TupleOfIntegers(Tuple):
    """
    Tuple of <Integer>s.
    """
    
    def __new__(Class, sequence = ()):
        return Tuple.__new__(Class, Integer, sequence)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        items, data = Tuple.unpack(Integer, data)
        
        return Class(items), data


class TupleOfStrings(Tuple):
    """
    Tuple of <String>s.
    """
    
    def __new__(Class, sequence = ()):
        return Tuple.__new__(Class, String, sequence)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        items, data = Tuple.unpack(String, data)
        
        return Class(items), data
