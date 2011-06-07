# -*- coding: utf-8 -*-



"""
Anarchy Online chat protocol: data types.
"""



import struct



### EXCEPTIONS #################################################################


class AOTypeError(TypeError):
    pass

class IntegersTypeError(AOTypeError):
    pass

class IntegerTypeError(IntegersTypeError):
    pass

class StringsTypeError(AOTypeError):
    pass

class StringTypeError(StringsTypeError):
    pass

class GroupIDTypeError(AOTypeError):
    pass



### DATA TYPES #################################################################


class Integer(long):
    """
    Anarchy Online chat protocol: 32-bit unsigned integer data type.
    """
    
    @staticmethod
    def pack(integer):
        """
        Pack Integer to binary data.
        """
        
        try:
            data = struct.pack(">I", integer)
        except struct.error, error:
            raise IntegerTypeError(error, integer)
        
        return data
    
    @staticmethod
    def unpack(data):
        """
        Unpack first Integer from binary data.
        """
        
        try:
            integer, data = Integer(struct.unpack(">I", data[:4])[0]), data[4:]
        except struct.error, error:
            raise IntegerTypeError(error, data)
        
        return integer, data


class Integers(list):
    """
    Anarchy Online chat protocol: 16-bit length array of Integer data type.
    """
    
    @staticmethod
    def pack(integers):
        """
        Pack Integers (list of Integer) to binary data.
        """
        
        try:
            data = struct.pack(">H", len(integers)) + "".join(map(lambda item: Integer.pack(item), integers))
        except struct.error, error:
            raise IntegersTypeError(error, integers)
        
        return data
    
    @staticmethod
    def unpack(data):
        """
        Unpack first Integers (list of Integer) from binary data.
        """
        
        integers = Integers()
        
        try:
            count, data = struct.unpack(">H", data[:2])[0], data[2:]
        except struct.error, error:
            raise IntegersTypeError(error, data)
        
        for i in range(count):
            integer, data = Integer.unpack(data)
            integers.append(integer)
        
        return integers, data


class String(str):
    """
    Anarchy Online chat protocol: 16-bit length string data type.
    """
    
    @staticmethod
    def pack(string):
        """
        Pack String to binary data.
        """
        
        try:
            data = struct.pack(">H", len(string)) + string
        except struct.error, error:
            raise StringTypeError(error, string)
        
        return data
    
    @staticmethod
    def unpack(data):
        """
        Unpack first String from binary data.
        """
        
        try:
            length, data = struct.unpack(">H", data[:2])[0], data[2:]
        except struct.error, error:
            raise StringTypeError(error, data)
        
        return data[:length], data[length:]


class Strings(list):
    """
    Anarchy Online chat protocol: 16-bit length array of String data type.
    """
    
    @staticmethod
    def pack(strings):
        """
        Pack Strings (list of String) to binary data.
        """
        
        try:
            data = struct.pack(">H", len(strings)) + "".join(map(lambda item: String.pack(item), strings))
        except struct.error, error:
            raise StringsTypeError(error, strings)
        
        return data
    
    @staticmethod
    def unpack(data):
        """
        Unpack first Strings (list of String) from binary data.
        """
        
        strings = Strings()
        
        try:
            count, data = struct.unpack(">H", data[:2])[0], data[2:]
        except struct.error, error:
            raise StringsTypeError(error, data)
        
        for i in range(count):
            string, data = String.unpack(data)
            strings.append(string)
        
        return strings, data


class GroupID(long):
    """
    Anarchy Online chat protocol: 40-bit binary data type.
    """
    
    @staticmethod
    def pack(id):
        """
        Pack GroupID to binary data.
        """
        
        try:
            data = struct.pack(">BI", id >> 32, id & 0xffffffffL)
        except struct.error, error:
            raise GroupIDTypeError(error, id)
        
        return data
    
    @staticmethod
    def unpack(data):
        """
        Unpack first GroupID from binary data.
        """
        
        try:
            a, b = struct.unpack(">BI", data[:5])
        except struct.error, error:
            raise GroupIDTypeError(error, data)
        
        return a << 32 + b, data[5:]
