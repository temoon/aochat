# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: packets.
"""


import struct

from AOChat.Types import Integer, String, IntegerTuple, StringTuple, ChannelID
from AOChat.Characters import Character


class _Packet(tuple):
    
    def __new__(Class, type, args):
        """
        Constructor of packet.
        """
        
        return tuple.__new__(Class, args)
    
    def __init__(self, type, args):
        """
        Packet.
        """
        
        tuple.__init__(self, args)
        
        self.type = type
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        data = "".join(map(lambda arg: arg.pack(), self))
        data = struct.pack(">2H", self.type, len(data)) + data
        
        return data


class _ServerPacket(_Packet):
    
    def __new__(Class, packet_type, types, data):
        """
        Constructor of server packet.
        """
        
        args = []
        
        for item_type in types:
            arg, data = item_type.unpack(data)
            args.append(arg)
        
        return _Packet.__new__(Class, packet_type, args)
    
    def __init__(self, packet_type, types, data):
        """
        Packet from server.
        """
        
        _Packet.__init__(self, packet_type, self)


class _ClientPacket(_Packet):
    
    def __new__(Class, type, args):
        """
        Constructor of client packet.
        """
        
        return tuple.__new__(Class, args)
    
    def __init__(self, type, args):
        """
        Packet from client.
        """
        
        _Packet.__init__(self, type, args)


class AOSP_LOGIN_SEED(_ServerPacket):
    
    type = 0
    
    def __new__(Class, data):
        """
        Constructor of LOGIN_SEED packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_LOGIN_SEED.type, (String,), data)
    
    def __init__(self, data):
        """
        LOGIN_SEED packet (server_key of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_LOGIN_SEED.type, map(type, self), data)
        
        self.server_key = self[0]


class AOSP_LOGIN_OK(_ServerPacket):
    
    type = 5
    
    def __new__(Class, data):
        """
        Constructor of LOGIN_OK packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_LOGIN_OK.type, (), data)
    
    def __init__(self, data):
        """
        LOGIN_OK packet (no data).
        """
        
        _ServerPacket.__init__(self, AOSP_LOGIN_OK.type, map(type, self), data)


class AOSP_LOGIN_ERROR(_ServerPacket):
    
    type = 6
    
    def __new__(Class, data):
        """
        Constructor of LOGIN_ERROR packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_LOGIN_ERROR.type, (String,), data)
    
    def __init__(self, data):
        """
        LOGIN_ERROR packet (message of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_LOGIN_ERROR.type, map(type, self), data)
        
        self.message = self[0]


class AOSP_LOGIN_CHARACTER_LIST(_ServerPacket):
    
    type = 7
    
    def __new__(Class, data):
        """
        Constructor of LOGIN_CHARACTER_LIST packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_LOGIN_CHARACTER_LIST.type, (IntegerTuple, StringTuple, IntegerTuple, IntegerTuple,), data)
    
    def __init__(self, data):
        """
        LOGIN_CHARACTER_LIST packet (characters of <Character>).
        """
        
        _ServerPacket.__init__(self, AOSP_LOGIN_CHARACTER_LIST.type, map(type, self), data)
        
        characters = []
        
        for i in range(len(self[0])):
            character = Character(self[0][i], self[1][i], self[2][i], self[3][i])
            characters.append(character)
        
        self.characters = tuple(characters)


#class AOSP_CLIENT_UNKNOWN(ServerPacket):
#    """
#    Anarchy Online chat protocol: CLIENT_UNKNOWN packet.
#    """
#    
#    type = 10
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_CLIENT_NAME(ServerPacket):
#    """
#    Anarchy Online chat protocol: CLIENT_NAME packet.
#    """
#    
#    type = 20
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, String,))
#        
#        self.user_id = self.args[0]
#        self.name = self.args[1]
#
#
#class AOSP_LOOKUP_RESULT(ServerPacket):
#    """
#    Anarchy Online chat protocol: LOOKUP_RESULT packet.
#    """
#    
#    type = 21
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, String,))
#        
#        self.user_id = self.args[0]
#        self.name = self.args[1]
#
#
#class AOSP_MSG_PRIVATE(ServerPacket):
#    """
#    Anarchy Online chat protocol: MSG_PRIVATE packet.
#    """
#    
#    type = 30
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, String, String,))
#        
#        self.user_id = self.args[0]
#        self.text = self.args[1]
#        self.blob = self.args[2]
#
#
#class AOSP_MSG_VICINITY(ServerPacket):
#    """
#    Anarchy Online chat protocol: MSG_VICINITY packet.
#    """
#    
#    type = 34
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, String, String,))
#        
#        self.user_id = self.args[0]
#        self.text = self.args[1]
#        self.blob = self.args[2]
#
#
#class AOSP_MSG_ANONVICINITY(ServerPacket):
#    """
#    Anarchy Online chat protocol: MSG_ANONVICINITY packet.
#    """
#    
#    type = 35
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (String, String, String,))
#        
#        self.user = self.args[0]
#        self.text = self.args[1]
#        self.blob = self.args[2]
#
#
#class AOSP_MSG_SYSTEM(ServerPacket):
#    """
#    Anarchy Online chat protocol: MSG_SYSTEM packet.
#    """
#    
#    type = 36
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (String,))
#        
#        self.text = self.args[0]
#
#
#class AOSP_MESSAGE_SYSTEM(ServerPacket):
#    """
#    Anarchy Online chat protocol: MESSAGE_SYSTEM packet.
#    """
#    
#    type = 37
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, Integer, Integer, String,))
#        
#        self.client_id = self.args[0]
#        self.window_id = self.args[1]
#        self.message_id = self.args[2]
#        self.message_args = self.args[3]
#
#
#class AOSP_BUDDY_STATUS(ServerPacket):
#    """
#    Anarchy Online chat protocol: BUDDY_STATUS packet.
#    """
#    
#    type = 40
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, Integer, String,))
#        
#        self.user_id = self.args[0]
#        self.online = self.args[1]
#        self.status = self.args[2]
#
#
#class AOSP_BUDDY_REMOVED(ServerPacket):
#    """
#    Anarchy Online chat protocol: BUDDY_REMOVED packet.
#    """
#    
#    type = 41
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_PRIVGRP_INVITE(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_INVITE packet.
#    """
#    
#    type = 50
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_PRIVGRP_KICK(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_KICK packet.
#    """
#    
#    type = 51
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_PRIVGRP_JOIN(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_JOIN packet.
#    """
#    
#    type = 52
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_PRIVGRP_PART(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_PART packet.
#    """
#    
#    type = 53
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer,))
#        
#        self.user_id = self.args[0]
#
#
#class AOSP_PRIVGRP_KICKALL(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_KICKALL packet.
#    """
#    
#    type = 54
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, ())
#
#
#class AOSP_PRIVGRP_CLIJOIN(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_CLIJOIN packet.
#    """
#    
#    type = 55
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, Integer,))
#        
#        self.user_a_id = self.args[0]
#        self.user_b_id = self.args[1]
#
#
#class AOSP_PRIVGRP_CLIPART(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_CLIPART packet.
#    """
#    
#    type = 56
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, Integer,))
#        
#        self.user_a_id = self.args[0]
#        self.user_b_id = self.args[1]
#
#
#class AOSP_PRIVGRP_MSG(ServerPacket):
#    """
#    Anarchy Online chat protocol: PRIVGRP_MSG packet.
#    """
#    
#    type = 57
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, Integer, String, String,))
#        
#        self.user_a_id = self.args[0]
#        self.user_b_id = self.args[1]
#        self.text = self.args[2]
#        self.blob = self.args[3]
#
#
#class AOSP_GROUP_JOIN(ServerPacket):
#    """
#    Anarchy Online chat protocol: GROUP_JOIN packet.
#    """
#    
#    type = 60
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (GroupID, String, Integer, String,))
#        
#        self.group_id = self.args[0]
#        self.group_name = self.args[1]
#        self.mute = self.args[2]
#        self.status = self.args[3]
#
#
#class AOSP_GROUP_PART(ServerPacket):
#    """
#    Anarchy Online chat protocol: GROUP_PART packet.
#    """
#    
#    type = 61
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (GroupID,))
#        
#        self.group_id = self.args[0]
#
#
#class AOSP_GROUP_MSG(ServerPacket):
#    """
#    Anarchy Online chat protocol: GROUP_MSG packet.
#    """
#    
#    type = 65
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (GroupID, Integer, String, String,))
#        
#        self.group_id = self.args[0]
#        self.user_id = self.args[1]
#        self.text = self.args[2]
#        self.blob = self.args[3]
#
#
#class AOSP_PONG(ServerPacket):
#    """
#    Anarchy Online chat protocol: PONG packet.
#    """
#    
#    type = 100
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (String,))
#        
#        self.string = self.args[0]
#
#
#class AOSP_FORWARD(ServerPacket):
#    """
#    Anarchy Online chat protocol: FORWARD packet.
#    """
#    
#    type = 110
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integer, String,))
#        
#        # TODO: ...
#
#
#class AOSP_AMD_MUX_INFO(ServerPacket):
#    """
#    Anarchy Online chat protocol: AMD_MUX_INFO packet.
#    """
#    
#    type = 1100
#    
#    def __init__(self, data):
#        ServerPacket.__init__(self, data, (Integers, Integers, Integers,))
#        
#        # TODO: ...



### PACKETS TO SERVER ##########################################################


class AOCP_LOGIN_REQUEST(_ClientPacket):
    
    type = 2
    
    def __new__(Class, version, username, login_key):
        """
        Constructor of LOGIN_REQUEST packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_LOGIN_REQUEST.type, (Integer(version), String(username), String(login_key),))
    
    def __init__(self, version, username, login_key):
        """
        LOGIN_REQUEST packet (version of <Integer>, username of <String>, login_key of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_LOGIN_REQUEST.type, self)
        
        self.version = version
        self.username = username
        self.login_key = login_key


class AOCP_LOGIN_SELECT_CHARACTER(_ClientPacket):
    
    type = 3
    
    def __new__(Class, character_id):
        """
        Constructor of LOGIN_SELECT_CHARACTER packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_LOGIN_SELECT_CHARACTER.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        """
        LOGIN_SELECT_CHARACTER packet (character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_LOGIN_SELECT_CHARACTER.type, self)


#class AOCP_CHARACTER_LOOKUP_REQUEST(ClientPacket):
#    """
#    Anarchy Online chat protocol: CHARACTER_LOOKUP_REQUEST packet.
#    """
#    
#    type = 21
#    
#    def __init__(self, char_name):
#        ClientPacket.__init__(self, String(char_name))
#
#
#class AOCP_PRIVATE_MESSAGE(ClientPacket):
#    """
#    Anarchy Online chat protocol: PRIVATE_MESSAGE packet.
#    """
#    
#    type = 30
#    
#    def __init__(self, char_id, text, blob):
#        ClientPacket.__init__(self, Integer(char_id), String(text), String(blob))
#
#
#class AOCP_FRIEND_UPDATE(ClientPacket):
#    """
#    Anarchy Online chat protocol: FRIEND_UPDATE packet.
#    
#    flags = 0 means temporary, anything else means permanent.
#    """
#    
#    type = 40
#    
#    def __init__(self, char_id, flags):
#        ClientPacket.__init__(self, Integer(char_id), String(flags))
#
#
#class AOCP_FRIEND_REMOVE(ClientPacket):
#    """
#    Anarchy Online chat protocol: FRIEND_REMOVE packet.
#    """
#    
#    type = 41
#    
#    def __init__(self, char_id):
#        ClientPacket.__init__(self, Integer(char_id))
#
#
#class AOCP_ONLINE_STATUS(ClientPacket):
#    """
#    Anarchy Online chat protocol: ONLINE_STATUS packet.
#    """
#    
#    type = 42
#    
#    def __init__(self, online):
#        ClientPacket.__init__(self, Integer(online))
#
#
#class AOCP_PRIVATE_CHANNEL_ACCEPT(ClientPacket):
#    """
#    Anarchy Online chat protocol: PRIVATE_CHANNEL_ACCEPT packet.
#    """
#    
#    type = 52
#    
#    def __init__(self, owner_char_id):
#        ClientPacket.__init__(self, Integer(owner_char_id))
#
#
#class AOCP_PRIVATE_CHANNEL_LEAVE(ClientPacket):
#    """
#    Anarchy Online chat protocol: PRIVATE_CHANNEL_LEAVE packet.
#    """
#    
#    type = 53
#    
#    def __init__(self, owner_char_id):
#        ClientPacket.__init__(self, Integer(owner_char_id))
#
#
#class AOCP_PRIVATE_CHANNEL_KICK_ALL(ClientPacket):
#    """
#    Anarchy Online chat protocol: PRIVATE_CHANNEL_KICK_ALL packet.
#    """
#    
#    type = 54
#    
#    def __init__(self):
#        ClientPacket.__init__(self)
#
#
#class AOCP_GROUP_DATASET(ClientPacket):
#    """
#    Anarchy Online chat protocol: GROUP_DATASET packet.
#    """
#    
#    type = 64
#    
#    def __init__(self, group_id, mute):
#        ClientPacket.__init__(self, GroupID(group_id), Integer(mute), String(""))
#        
#        # TODO: ...
#
#
#class AOCP_GROUP_MESSAGE(ClientPacket):
#    """
#    Anarchy Online chat protocol: GROUP_MESSAGE packet.
#    """
#    
#    type = 65
#    
#    def __init__(self, group_id, text, blob):
#        ClientPacket.__init__(self, GroupID(group_id), String(text), String(blob))
#
#
#class AOCP_GROUP_CLIMODE(ClientPacket):
#    """
#    Anarchy Online chat protocol: GROUP_CLIMODE packet.
#    """
#    
#    type = 66
#    
#    def __init__(self, group_id):
#        ClientPacket.__init__(self, GroupID(group_id), Integer(0), Integer(0), Integer(0), Integer(0))
#        
#        # TODO: ...
#
#
#class AOCP_CLIMODE_GET(ClientPacket):
#    """
#    Anarchy Online chat protocol: CLIMODE_GET packet.
#    """
#    
#    type = 70
#    
#    def __init__(self, group_id):
#        ClientPacket.__init__(self, Integer(0), GroupID(group_id))
#        
#        # TODO: ...
#
#
#class AOCP_CLIMODE_SET(ClientPacket):
#    """
#    Anarchy Online chat protocol: CLIMODE_SET packet.
#    """
#    
#    type = 71
#    
#    def __init__(self):
#        ClientPacket.__init__(self, Integer(0), Integer(0), Integer(0), Integer(0))
#        
#        # TODO: ...
#
#
#class AOCP_PING(ClientPacket):
#    """
#    Anarchy Online chat protocol: PING packet.
#    """
#    
#    type = 100
#    
#    def __init__(self, string):
#        ClientPacket.__init__(self, String(string))
#
#
#class AOCP_CHAT_COMMAND(ClientPacket):
#    """
#    Anarchy Online chat protocol: CHAT_COMMAND packet.
#    """
#    
#    type = 120
#    
#    def __init__(self, command, value):
#        ClientPacket.__init__(self, String(command), String(value))
