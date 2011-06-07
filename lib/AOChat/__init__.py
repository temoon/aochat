# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
"""



import socket
import time


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



class ChatError(Exception): pass

class Chat(object):
    """
    Core Anarchy Online chat protocol implementation.
    """
    
    def __init__(self, username, password, dimension, character = None, timeout = 10):
        self.username = username
        self.password = password
        self.dimension = dimension
        self.character = character
        
        # Initialize connection
        try:
            self.socket = socket.create_connection((dimension.host, dimension.port,), timeout)
            self.ping_time = time.time()
        except socket.error, error:
            raise ChatError("Connection failed: %s" % str(error), error)
        else:
            try:
                packet = self.wait_packet(AOCP_LOGIN_SEED)
            except TypeError, packet:
                raise ChatError("Invalid greeting packet.", packet)
        
        # Athenticate
        try:
            login_key = generate_login_key(packet.args[0], username, password)
            
            packet = self.send_packet(
                send = AOCP_LOGIN_REQUEST,
                expect = AOCP_LOGIN_CHARLIST,
                data = [0, username, login_key],
            )
        except TypeError, packet:
            raise ChatError("Authentication failed.", packet)
        else:
            if packet.args[0].startswith("No characters found"):
                raise ChatError("No characters found.")
        
        # Login
        if self.character:
            self.login(self.character)
    
    def wait_packet(self, expect):
        try:
            pass
        except socket.timeout:
            raise ChatError("Connection timed out.")
    
    def send_packet(self, send, data, expect = None):
        try:
            pass
        except socket.timeout:
            raise ChatError("Connection timed out.")
        
        if expect is not None:
            return self.wait_packet(expect)

