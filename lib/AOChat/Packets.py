# -*- coding: utf-8 -*-


"""
Anarchy Online chat protocol: packets.
"""


import struct

from AOChat.Types import Integer, String, IntegerTuple, StringTuple, ChannelID
from AOChat.Characters import Character



### BASE PROTECTED CLASSES #####################################################


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



### PACKETS FROM SERVER ########################################################


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
        LOGIN_CHARACTER_LIST packet (characters of <Character>s, character_id of <Integer>s, character_name of <String>s, character_level of <Integer>s, character_online of <Integer>s).
        """
        
        _ServerPacket.__init__(self, AOSP_LOGIN_CHARACTER_LIST.type, map(type, self), data)
        
        characters = []
        
        for i in range(len(self[0])):
            character = Character(self[0][i], self[1][i], self[2][i], self[3][i])
            characters.append(character)
        
        self.characters = tuple(characters)
        
        self.character_id = self[0]
        self.character_name = self[1]
        self.character_level = self[2]
        self.character_online = self[3]


class AOSP_CHARACTER_UNKNOWN(_ServerPacket):
    
    type = 10
    
    def __new__(Class, data):
        """
        Constructor of CHARACTER_UNKNOWN packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHARACTER_UNKNOWN.type, (Integer,), data)
    
    def __init__(self, data):
        """
        CHARACTER_UNKNOWN packet (character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHARACTER_UNKNOWN.type, map(type, self), data)
        
        self.character_id = self[0]


class AOSP_CHARACTER_NAME(_ServerPacket):
    
    type = 20
    
    def __new__(Class, data):
        """
        Constructor of CHARACTER_NAME packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHARACTER_NAME.type, (Integer, String,), data)
    
    def __init__(self, data):
        """
        CHARACTER_NAME packet (character_id of <Integer>, character_name of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHARACTER_NAME.type, map(type, self), data)
        
        self.character_id = self[0]
        self.character_name = self[1]


class AOSP_CHARACTER_LOOKUP_RESULT(_ServerPacket):
    
    type = 21
    
    def __new__(Class, data):
        """
        Constructor of CHARACTER_LOOKUP_RESULT packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHARACTER_LOOKUP_RESULT.type, (Integer, String,), data)
    
    def __init__(self, data):
        """
        CHARACTER_LOOKUP_RESULT packet (character_id of <Integer>, character_name of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHARACTER_LOOKUP_RESULT.type, map(type, self), data)
        
        self.character_id = self[0]
        self.character_name = self[1]


class AOSP_PRIVATE_MESSAGE(_ServerPacket):
    
    type = 30
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_MESSAGE.type, (Integer, String, String,), data)
    
    def __init__(self, data):
        """
        PRIVATE_MESSAGE packet (character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_MESSAGE.type, map(type, self), data)
        
        self.character_id = self[0]
        self.message = self[1]
        self.blob = self[2]


class AOSP_VICINITY_MESSAGE(_ServerPacket):
    
    type = 34
    
    def __new__(Class, data):
        """
        Constructor of VICINITY_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_VICINITY_MESSAGE.type, (Integer, String, String,), data)
    
    def __init__(self, data):
        """
        VICINITY_MESSAGE packet (character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_VICINITY_MESSAGE.type, map(type, self), data)
        
        self.character_id = self[0]
        self.message = self[1]
        self.blob = self[2]


class AOSP_BROADCAST_MESSAGE(_ServerPacket):
    
    type = 35
    
    def __new__(Class, data):
        """
        Constructor of BROADCAST_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_BROADCAST_MESSAGE.type, (Integer, String, String,), data)
    
    def __init__(self, data):
        """
        BROADCAST_MESSAGE packet (character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_BROADCAST_MESSAGE.type, map(type, self), data)
        
        self.character_id = self[0]
        self.message = self[1]
        self.blob = self[2]


class AOSP_SIMPLE_SYSTEM_MESSAGE(_ServerPacket):
    
    type = 36
    
    def __new__(Class, data):
        """
        Constructor of SIMPLE_SYSTEM_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_SIMPLE_SYSTEM_MESSAGE.type, (String,), data)
    
    def __init__(self, data):
        """
        SIMPLE_SYSTEM_MESSAGE packet (message of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_SIMPLE_SYSTEM_MESSAGE.type, map(type, self), data)
        
        self.message = self[0]


class AOSP_SYSTEM_MESSAGE(_ServerPacket):
    
    type = 37
    
    def __new__(Class, data):
        """
        Constructor of SYSTEM_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_SYSTEM_MESSAGE.type, (Integer, Integer, Integer, String,), data)
    
    def __init__(self, data):
        """
        SYSTEM_MESSAGE packet (client_id of <Integer>, window_id of <Integer>, message_id of <Integer>, message of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_SYSTEM_MESSAGE.type, map(type, self), data)
        
        self.client_id = self[0]
        self.window_id = self[1]
        self.message_id = self[2]
        self.message = self[3]


class AOSP_FRIEND_UPDATE(_ServerPacket):
    
    type = 40
    
    def __new__(Class, data):
        """
        Constructor of FRIEND_UPDATE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_FRIEND_UPDATE.type, (Integer, Integer, String,), data)
    
    def __init__(self, data):
        """
        FRIEND_UPDATE packet (character_id of <Integer>, online of <Integer>, flags of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_FRIEND_UPDATE.type, map(type, self), data)
        
        self.character_id = self[0]
        self.online = self[1]
        self.flags = self[2]


class AOSP_FRIEND_REMOVE(_ServerPacket):
    
    type = 41
    
    def __new__(Class, data):
        """
        Constructor of FRIEND_REMOVE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_FRIEND_REMOVE.type, (Integer,), data)
    
    def __init__(self, data):
        """
        FRIEND_REMOVE packet (character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_FRIEND_REMOVE.type, map(type, self), data)
        
        self.character_id = self[0]


class AOSP_PRIVATE_CHANNEL_INVITE(_ServerPacket):
    
    type = 50
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_CHANNEL_INVITE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_INVITE.type, (Integer,), data)
    
    def __init__(self, data):
        """
        PRIVATE_CHANNEL_INVITE packet (character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_CHANNEL_INVITE.type, map(type, self), data)
        
        self.character_id = self[0]


class AOSP_PRIVATE_CHANNEL_KICK(_ServerPacket):
    
    type = 51
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_CHANNEL_KICK packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_KICK.type, (Integer,), data)
    
    def __init__(self, data):
        """
        PRIVATE_CHANNEL_KICK packet (character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_CHANNEL_KICK.type, map(type, self), data)
        
        self.character_id = self[0]


class AOSP_PRIVATE_CHANNEL_JOIN(_ServerPacket):
    
    type = 55
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_CHANNEL_JOIN packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_JOIN.type, (Integer, Integer,), data)
    
    def __init__(self, data):
        """
        PRIVATE_CHANNEL_JOIN packet (owner_character_id of <Integer>, character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_CHANNEL_JOIN.type, map(type, self), data)
        
        self.owner_character_id = self[0]
        self.character_id = self[1]


class AOSP_PRIVATE_CHANNEL_LEAVE(_ServerPacket):
    
    type = 56
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_CHANNEL_LEAVE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_LEAVE.type, (Integer, Integer,), data)
    
    def __init__(self, data):
        """
        PRIVATE_CHANNEL_LEAVE packet (owner_character_id of <Integer>, character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_CHANNEL_LEAVE.type, map(type, self), data)
        
        self.owner_character_id = self[0]
        self.character_id = self[1]


class AOSP_PRIVATE_CHANNEL_MESSAGE(_ServerPacket):
    
    type = 51
    
    def __new__(Class, data):
        """
        Constructor of PRIVATE_CHANNEL_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_MESSAGE.type, (Integer,), data)
    
    def __init__(self, data):
        """
        PRIVATE_CHANNEL_MESSAGE packet (character_id of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_PRIVATE_CHANNEL_MESSAGE.type, map(type, self), data)
        
        self.character_id = self[0]


class AOSP_CHANNEL_JOIN(_ServerPacket):
    
    type = 60
    
    def __new__(Class, data):
        """
        Constructor of CHANNEL_JOIN packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHANNEL_JOIN.type, (ChannelID, String, Integer,), data)
    
    def __init__(self, data):
        """
        CHANNEL_JOIN packet (channel_id of <ChannelID>, channel_name of <String>, channel_status of <Integer>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHANNEL_JOIN.type, map(type, self), data)
        
        self.channel_id = self[0]
        self.channel_name = self[1]
        self.channel_status = self[2]


class AOSP_CHANNEL_LEAVE(_ServerPacket):
    
    type = 61
    
    def __new__(Class, data):
        """
        Constructor of CHANNEL_LEAVE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHANNEL_LEAVE.type, (ChannelID,), data)
    
    def __init__(self, data):
        """
        CHANNEL_LEAVE packet (channel_id of <ChannelID>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHANNEL_LEAVE.type, map(type, self), data)
        
        self.channel_id = self[0]


class AOSP_CHANNEL_MESSAGE(_ServerPacket):
    
    type = 65
    
    def __new__(Class, data):
        """
        Constructor of CHANNEL_MESSAGE packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_CHANNEL_MESSAGE.type, (ChannelID, Integer, String, String,), data)
    
    def __init__(self, data):
        """
        CHANNEL_MESSAGE packet (channel_id of <ChannelID>, character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_CHANNEL_MESSAGE.type, map(type, self), data)
        
        self.channel_id = self[0]
        self.character_id = self[1]
        self.message = self[2]
        self.blob  = self[3]


class AOSP_PONG(_ServerPacket):
    
    type = 100
    
    def __new__(Class, data):
        """
        Constructor of PONG packet.
        """
        
        return _ServerPacket.__new__(Class, AOSP_PONG.type, (String,), data)
    
    def __init__(self, data):
        """
        PONG packet (message of <String>).
        """
        
        _ServerPacket.__init__(self, AOSP_PONG.type, map(type, self), data)
        
        self.message = self[0]



### PACKETS TO SERVER ##########################################################


class AOCP_LOGIN_REQUEST(_ClientPacket):
    
    type = 2
    
    def __new__(Class, username, login_key, version = 0):
        """
        Constructor of LOGIN_REQUEST packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_LOGIN_REQUEST.type, (Integer(version), String(username), String(login_key),))
    
    def __init__(self, username, login_key, version = 0):
        """
        LOGIN_REQUEST packet (username of <String>, login_key of <String>, version of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_LOGIN_REQUEST.type, self)
        
        self.version = self[0]
        self.username = self[1]
        self.login_key = self[2]


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
        
        self.character_id = self[0]


class AOCP_CHARACTER_LOOKUP_REQUEST(_ClientPacket):
    
    type = 21
    
    def __new__(Class, character_name):
        """
        Constructor of LOGIN_CHARACTER_LOOKUP_REQUEST packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_CHARACTER_LOOKUP_REQUEST.type, (String(character_name),))
    
    def __init__(self, character_name):
        """
        CHARACTER_LOOKUP_REQUEST packet (character_name of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_CHARACTER_LOOKUP_REQUEST.type, self)
        
        self.character_name = self[0]


class AOCP_PRIVATE_MESSAGE(_ClientPacket):
    
    type = 30
    
    def __new__(Class, character_id, message, blob):
        """
        Constructor of PRIVATE_MESSAGE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_MESSAGE.type, (Integer(character_id), String(message), String(blob),))
    
    def __init__(self, character_id, message, blob):
        """
        PRIVATE_MESSAGE packet (character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_MESSAGE.type, self)
        
        self.character_id = self[0]
        self.message = self[1]
        self.blob = self[2]


class AOCP_FRIEND_UPDATE(_ClientPacket):
    
    type = 40
    
    def __new__(Class, character_id, flags = 0):
        """
        Constructor of FRIEND_UPDATE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_FRIEND_UPDATE.type, (Integer(character_id), Integer(flags),))
    
    def __init__(self, character_id, flags = 0):
        """
        FRIEND_UPDATE packet (character_id of <Integer>, flags of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_FRIEND_UPDATE.type, self)
        
        self.character_id = self[0]
        self.flags = self[1]


class AOCP_FRIEND_REMOVE(_ClientPacket):
    
    type = 41
    
    def __new__(Class, character_id):
        """
        Constructor of FRIEND_REMOVE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_FRIEND_REMOVE.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        """
        FRIEND_REMOVE packet (character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_FRIEND_REMOVE.type, self)
        
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_INVITE(_ClientPacket):
    
    type = 50
    
    def __new__(Class, character_id):
        """
        Constructor of PRIVATE_CHANNEL_INVITE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_INVITE.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        """
        PRIVATE_CHANNEL_INVITE packet (character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_INVITE.type, self)
        
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_KICK(_ClientPacket):
    
    type = 51
    
    def __new__(Class, character_id):
        """
        Constructor of PRIVATE_CHANNEL_KICK packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_KICK.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        """
        PRIVATE_CHANNEL_KICK packet (character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_KICK.type, self)
        
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_JOIN(_ClientPacket):
    
    type = 52
    
    def __new__(Class, owner_character_id):
        """
        Constructor of PRIVATE_CHANNEL_JOIN packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_JOIN.type, (Integer(owner_character_id),))
    
    def __init__(self, owner_character_id):
        """
        PRIVATE_CHANNEL_JOIN packet (owner_character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_JOIN.type, self)
        
        self.owner_character_id = self[0]


class AOCP_PRIVATE_CHANNEL_LEAVE(_ClientPacket):
    
    type = 53
    
    def __new__(Class, owner_character_id):
        """
        Constructor of PRIVATE_CHANNEL_LEAVE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_LEAVE.type, (Integer(owner_character_id),))
    
    def __init__(self, owner_character_id):
        """
        PRIVATE_CHANNEL_LEAVE packet (owner_character_id of <Integer>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_LEAVE.type, self)
        
        self.owner_character_id = self[0]


class AOCP_PRIVATE_CHANNEL_KICKALL(_ClientPacket):
    
    type = 54
    
    def __new__(Class):
        """
        Constructor of PRIVATE_CHANNEL_KICKALL packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_KICKALL.type, ())
    
    def __init__(self):
        """
        PRIVATE_CHANNEL_KICKALL packet (no data).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_KICKALL.type, self)


class AOCP_PRIVATE_CHANNEL_MESSAGE(_ClientPacket):
    
    type = 57
    
    def __new__(Class, character_id, message, blob):
        """
        Constructor of PRIVATE_CHANNEL_MESSAGE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_MESSAGE.type, (Integer(character_id), String(message), String(blob),))
    
    def __init__(self, character_id, message, blob):
        """
        PRIVATE_CHANNEL_MESSAGE packet (character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_MESSAGE.type, self)
        
        self.character_id = self[0]
        self.message = self[1]
        self.blob = self[2]


class AOCP_CHANNEL_MESSAGE(_ClientPacket):
    
    type = 65
    
    def __new__(Class, channel_id, character_id, message, blob):
        """
        Constructor of CHANNEL_MESSAGE packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_CHANNEL_MESSAGE.type, (ChannelID(channel_id), Integer(character_id), String(message), String(blob),))
    
    def __init__(self, channel_id, character_id, message, blob):
        """
        CHANNEL_MESSAGE packet (channel_id of <ChannelID>, character_id of <Integer>, message of <String>, blob of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_CHANNEL_MESSAGE.type, self)
        
        self.channel_id = self[0]
        self.character_id = self[1]
        self.message = self[2]
        self.blob = self[3]


class AOCP_PING(_ClientPacket):
    
    type = 100
    
    def __new__(Class, message):
        """
        Constructor of PING packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_PING.type, (String(message),))
    
    def __init__(self, message):
        """
        PING packet (message of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_PING.type, self)
        
        self.message = self[0]


class AOCP_CHAT_COMMAND(_ClientPacket):
    
    type = 120
    
    def __new__(Class, command):
        """
        Constructor of CHAT_COMMAND packet.
        """
        
        return _ClientPacket.__new__(Class, AOCP_CHAT_COMMAND.type, (String(command),))
    
    def __init__(self, command):
        """
        CHAT_COMMAND packet (command of <String>).
        """
        
        _ClientPacket.__init__(self, AOCP_CHAT_COMMAND.type, self)
        
        self.command = self[0]
