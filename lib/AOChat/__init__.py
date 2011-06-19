# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
"""



import socket
import struct


from AOChat.LoginKey import generate_login_key

from AOChat.Packets import (
    # Server packets
    AOSP_LOGIN_SEED, AOSP_LOGIN_OK, AOSP_LOGIN_ERROR, AOSP_LOGIN_CHARACTER_LIST,
    
    # Client packets
    AOCP_LOGIN_REQUEST, AOCP_LOGIN_SELECT_CHARACTER,
)

from AOChat.Dimensions import Dimension
from AOChat.Characters import Character


class ChatError(Exception):
    pass

class UnexpectedPacket(ChatError):
    pass


class Chat(object):
    """
    Anarchy Online chat protocol implementation.
    """
    
    def __init__(self, username, password, dimension, character = None, timeout = 10):
        # Initialize connection
        try:
            self.socket = socket.create_connection((dimension.host, dimension.port,), timeout)
        except socket.error, error:
            raise ChatError("Socket error %d: %s" % tuple(error))
        
        # Wait server key and generate login key
        try:
            server_key = self.wait_packet(AOSP_LOGIN_SEED).server_key
            login_key  = generate_login_key(server_key, username, password)
        except UnexpectedPacket, (type, packet):
            raise ChatError("Invalid greeting packet: %s" % type)
        
        # Authenticate
        try:
            self.character  = None
            self.characters = self.send_packet(AOCP_LOGIN_REQUEST(0, username, login_key), AOSP_LOGIN_CHARACTER_LIST, AOSP_LOGIN_ERROR).characters
        except UnexpectedPacket, (type, packet):
            raise ChatError(packet.message)
        
        # Login
        if character:
            self.login(character)
    
    def __read_socket(self, bytes):
        data = ""
        
        while bytes > 0:
            try:
                chunk = self.socket.recv(bytes)
            except socket.error, error:
                raise ChatError("Socket error %d: %s" % tuple(error))
            except socket.timeout:
                raise ChatError("Connection timed out.")
            
            if chunk == "":
                raise ChatError("Connection broken.")
            
            bytes = bytes - len(chunk)
            data = data + chunk
        
        return data
    
    def __write_socket(self, data):
        bytes = len(data)
        
        while bytes > 0:
            try:
                sent = self.socket.send(data)
            except socket.error, error:
                raise ChatError("Socket error %d: %s" % tuple(error))
            except socket.timeout:
                raise ChatError("Connection timed out.")
            
            if sent == 0:
                raise ChatError("Connection broken.")
            
            data = data[sent:]
            bytes = bytes - sent
    
    def wait_packet(self, expect, error = None):
        """
        Wait packet from server.
        """
        
        # Read data from server
        head = self.__read_socket(4)
        type, length = struct.unpack(">2H", head)
        data = self.__read_socket(length)
        
        # Check packet type
        if type != expect.type:
            if error and type == error.type:
                # Make error packet
                packet = error(data)
                
                raise UnexpectedPacket(type, packet)
            else:
                raise ChatError("Unexpected error.")
        
        # Make expected packet
        packet = expect(data)
        
        return packet
    
    def send_packet(self, packet, expect = None, error = None):
        """
        Send packet to server.
        """
        
        # Pack
        data = packet.pack()
        
        # Send data to server
        self.__write_socket(data)
        
        if expect:
            return self.wait_packet(expect, error)
    
    def login(self, character):
        """
        Login to chat.
        """
        
        # Lookup character
        if character.id not in map(lambda char: char.id, self.characters):
            raise ChatError("no valid characters to login.")
        
        # Login with selected character
        try:
            self.send_packet(AOCP_LOGIN_SELECT_CHARACTER(character.id), AOSP_LOGIN_OK, AOSP_LOGIN_ERROR)
        except UnexpectedPacket, (type, packet):
            raise ChatError(packet.message)
        
        # Set current character
        self.character = character
    
    def logout(self):
        """
        Logout from chat.
        """
        
        # TODO: ...
        
        # Unset current character
        self.character = None
