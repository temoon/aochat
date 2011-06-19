# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: data types.
"""


import struct


class Integer(long):
    
    def __init__(self, x = 0L, base = 10):
        """
        Unsigned integer.
        """
        
        long.__init__(self, x, base)
        
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
    
    def __init__(self, x = ""):
        """
        String.
        """
        
        str.__init__(self, x)
        
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
    
    def __init__(self, x = 0L, base = 10):
        """
        Channel ID.
        """
        
        long.__init__(self, x, base)
        
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


class _Tuple(tuple):
    
    def __new__(Class, Type, sequence = ()):
        """
        Constructor of tuple of <Type>s.
        """
        
        return tuple.__new__(Class, map(Type, sequence))
    
    def __init__(self, Type, sequence = ()):
        """
        Tuple of <Type>s.
        """
        
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


class IntegerTuple(_Tuple):
    
    def __new__(Class, sequence = ()):
        """
        Constructor of tuple of <Integer>s.
        """
        
        return _Tuple.__new__(Class, Integer, sequence)
    
    def __init__(self, sequence = ()):
        """
        Tuple of <Integer>s.
        """
        
        _Tuple.__init__(self, Integer, sequence)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        items, data = _Tuple.unpack(Integer, data)
        
        return Class(items), data


class StringTuple(_Tuple):
    
    def __new__(Class, sequence = ()):
        """
        Constructor of tuple of <String>s.
        """
        
        return _Tuple.__new__(Class, String, sequence)
    
    def __init__(self, sequence = ()):
        """
        Tuple of <String>s.
        """
        
        _Tuple.__init__(self, String, sequence)
    
    @classmethod
    def unpack(Class, data):
        """
        Unpack from binary data.
        """
        
        items, data = _Tuple.unpack(String, data)
        
        return Class(items), data
