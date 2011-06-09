# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
"""



import socket
import time
import struct


from AOChat.LoginKey import generate_login_key

from AOChat.Packets import (
    # Server packets
    AOSP_LOGIN_SEED,        AOSP_LOGIN_OK,         AOSP_LOGIN_ERROR,
    AOSP_LOGIN_CHARLIST,    AOSP_CLIENT_UNKNOWN,   AOSP_CLIENT_NAME,
    AOSP_LOOKUP_RESULT,     AOSP_MSG_PRIVATE,      AOSP_MSG_VICINITY,
    AOSP_MSG_ANONVICINITY,  AOSP_MSG_SYSTEM,       AOSP_MESSAGE_SYSTEM,
    AOSP_BUDDY_STATUS,      AOSP_BUDDY_REMOVED,    AOSP_PRIVGRP_INVITE,
    AOSP_PRIVGRP_KICK,      AOSP_PRIVGRP_JOIN,     AOSP_PRIVGRP_PART,
    AOSP_PRIVGRP_KICKALL,   AOSP_PRIVGRP_CLIJOIN,  AOSP_PRIVGRP_CLIPART,
    AOSP_PRIVGRP_MSG,       AOSP_GROUP_JOIN,       AOSP_GROUP_PART,
    AOSP_GROUP_MSG,         AOSP_PONG,             AOSP_FORWARD,
    AOSP_AMD_MUX_INFO,
    
    # Client packets
    AOCP_LOGIN_RESPONSE,    AOCP_LOGIN_SELCHAR,    AOCP_NAME_LOOKUP,
    AOCP_MSG_PRIVATE,       AOCP_BUDDY_ADD,        AOCP_BUDDY_REMOVE,
    AOCP_ONLINE_STATUS,     AOCP_GROUP_DATASET,    AOCP_GROUP_MESSAGE,
    AOCP_GROUP_CLIMODE,     AOCP_CLIMODE_GET,      AOCP_CLIMODE_SET,
    AOCP_PING,              AOCP_CHAT_COMMAND,
)

from AOChat.Dimensions import Dimension
from AOChat.Characters import Character



class ChatError(Exception):
    pass

class ProtocolError(ChatError):
    pass

class NetworkError(ChatError):
    pass

class UnexpectedPacketError(NetworkError):
    pass


class Chat(object):
    """
    Core Anarchy Online chat protocol implementation.
    """
    
    def __init__(self, username, password, dimension, timeout = 10):
        self.username = username
        self.password = password
        self.dimension = dimension
        self.character = None
        
        # Initialize connection
        try:
            self.socket = socket.create_connection((self.dimension.host, self.dimension.port,), timeout)
            self.ping_time = time.time()
        except socket.error, error:
            raise NetworkError("Connection failed: %s" % error)
        
        try:
            p_login_seed = self.wait_packet(AOSP_LOGIN_SEED)
        except UnexpectedPacketError:
            raise ProtocolError("Invalid greeting packet.")
        
        # Athenticate
        login_key = generate_login_key(p_login_seed.seed, self.username, self.password)
        
        try:
            p_login_charlist = self.send_packet(AOCP_LOGIN_RESPONSE, (username, login_key,), AOSP_LOGIN_CHARLIST)
        except UnexpectedPacketError:
            raise ProtocolError("Authentication failed or no characters found.")
    
    def wait_packet(self, expect):
        """
        Wait packet from server.
        """
        
        def read_from_socket(bytes):
            data = ""
            
            while bytes > 0:
                buffer = self.socket.recv(bytes)
                data = data + buffer
                bytes = bytes - len(buffer)
            
            return data
        
        # Read data from socket
        try:
            head = read_from_socket(4)
            type, length = struct.unpack(">2H", head)
            data = read_from_socket(length)
        except socket.timeout:
            raise NetworkError("Connection timed out.")
        
        # Check packet type
        if expect.type != type:
            raise UnexpectedPacket()
        
        # Make packet
        packet = expect(data)
        
        return packet
    
    def send_packet(self, send, args, expect = None):
        """
        Send packet to server.
        """
        
        # Make packet
        packet = send(*args)
        
        # Make data
        data = packet.pack(packet.args)
        data = struct.pack(">2H", packet.type, len(data)) + data
        
        try:
            self.socket.send(data)
        except socket.timeout:
            raise NetworkError("Connection timed out.")
        
        if expect:
            return self.wait_packet(expect)
    
    def login(self, character):
        """
        Login to chat.
        """
        
        # Lookup character
        for exist_character in self.characters:
            if character.id == exist_character.id:
                break
        else:
            raise ProtocolError("No valid character to login.")
        
        try:
            self.send_packet(AOCP_LOGIN_SELCHAR, (character.id,), AOSP_LOGIN_OK)
        except UnexpectedPacketError:
            raise ProtocolError("Login failed.")
        
        self.character = character
    
    def logout(self):
        """
        Logout from chat.
        """
        
        self.character = None
