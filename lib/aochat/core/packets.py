# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
Network packets.

AOSP_* - Server to client Anarchy Online chat packets
AOCP_* - Client to server packets
AOFL_* - Flags
"""


import struct

from aochat.core.types import Integer, String, ChannelID, TupleOfIntegers, TupleOfStrings
from aochat.data import get_text
from aochat.characters import Character


### FLAGS ######################################################################


# Auth
AOFL_AUTH                    = Integer(0x00000000)

# Character lookup result
AOFL_CHARACTER_UNKNOWN       = Integer(0xFFFFFFFF)

# Broadcast message
AOFL_BROADCAST_NOTICE        = String("")
AOFL_BROADCAST_ALL           = String("\x03")
AOFL_BROADCAST_PET           = String("\x05")

# Provate message
AOFL_PRIVATE_MESSAGE         = String("\x00")

# Vicinity message
AOFL_VICINITY_SAY            = String("\x00")
AOFL_VICINITY_WHISPER        = String("\x01")
AOFL_VICINITY_SHOUT          = String("\x02")
AOFL_VICINITY_SELF           = String("\x03")

# Friend status
AOFL_FRIEND_RECENT           = String("\x00")
AOFL_FRIEND_BUDDY            = String("\x01")

# Private channel message
AOFL_PRIVATE_CHANNEL_MESSAGE = String("")

# Channel message
AOFL_CHANNEL_MESSAGE         = String("")

# Ping
AOFL_PING                    = String("\x02")

# Chat command
AOFL_CHAT_COMMAND            = Integer(0x00000001)


### BASE PACKET CLASSES ########################################################


class Packet(tuple):
    """
    Anarchy Online chat packet.
    """
    
    def __new__(Class, packet_type, args):
        self = tuple.__new__(Class, args)
        
        self.type = packet_type
        
        return self
    
    def pack(self):
        """
        Pack to binary data.
        """
        
        data = "".join(map(lambda arg: arg.pack(), self))
        data = struct.pack(">2H", self.type, len(data)) + data
        
        return data
    
    def __repr__(self):
        return "<Packet %d [%s]>" % (self.type, ", ".join(map(repr, self)) or "no data")


class ServerPacket(Packet):
    """
    Server to client Anarchy Online chat packet.
    """
    
    def __new__(Class, packet_type, types, data):
        args = []
        
        for item_type in types:
            arg, data = item_type.unpack(data)
            args.append(arg)
        
        return Packet.__new__(Class, packet_type, args)


class ClientPacket(Packet):
    """
    Client to server packet.
    """
    
    def __new__(Class, packet_type, args):
        return Packet.__new__(Class, packet_type, args)


### PACKETS FROM SERVER ########################################################


class AOSP_SEED(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Seed
    
    server_key of <String>
    """
    
    type = 0
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_SEED.type, (String,), data)
    
    def __init__(self, data):
        self.server_key = self[0]


class AOSP_LOGIN_OK(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Login OK
    
    no data
    """
    
    type = 5
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_LOGIN_OK.type, (), data)


class AOSP_AUTH_ERROR(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Auth Error
    
    message of <String>
    """
    
    type = 6
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_AUTH_ERROR.type, (String,), data)
    
    def __init__(self, data):
        self.message = self[0]


class AOSP_CHARACTERS_LIST(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Characters List
    
    characters_id of <TupleOfIntegers>
    characters_name of <TupleOfStrings>
    characters_level of <TupleOfIntegers>
    characters_online of <TupleOfIntegers>
    
    characters of tuple of <Character>
    """
    
    type = 7
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHARACTERS_LIST.type, (TupleOfIntegers, TupleOfStrings, TupleOfIntegers, TupleOfIntegers,), data)
    
    def __init__(self, data):
        self.characters_id = self[0]
        self.characters_name = self[1]
        self.characters_level = self[2]
        self.characters_online = self[3]
        
        characters = []
        
        for i in range(len(self[0])):
            character = Character(self[0][i], self[1][i], self[2][i], self[3][i])
            characters.append(character)
        
        self.characters = tuple(characters)


class AOSP_CHARACTER_NAME(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Character Name
    
    character_id of <Integer>
    character_name of <String>
    """
    
    type = 20
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHARACTER_NAME.type, (Integer, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.character_name = self[1]


class AOSP_CHARACTER_LOOKUP(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Character Lookup
    
    character_id of <Integer>
    character_name of <String>
    """
    
    type = 21
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHARACTER_LOOKUP.type, (Integer, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.character_name = self[1]


class AOSP_PRIVATE_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Message
    
    character_id of <Integer>
    message of <String>
    unknown of <String>
    """
    
    type = 30
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_MESSAGE.type, (Integer, String, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.message = self[1]
        self.unknown = self[2]


class AOSP_VICINITY_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Vicinity Message
    
    character_id of <Integer>
    message of <String>
    flags of <String>
    """
    
    type = 34
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_VICINITY_MESSAGE.type, (Integer, String, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.message = self[1]
        self.flags = self[2]


class AOSP_BROADCAST_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Broadcast Message
    
    character_name of <String>
    message of <String>
    flags of <String>
    """
    
    type = 35
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_BROADCAST_MESSAGE.type, (String, String, String,), data)
    
    def __init__(self, data):
        self.character_name = self[0]
        self.message = self[1]
        self.flags = self[2]


class AOSP_SYSTEM_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: System Message
    
    message of <String>
    """
    
    type = 36
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_SYSTEM_MESSAGE.type, (String,), data)
    
    def __init__(self, data):
        self.message = self[0]


class AOSP_CHAT_NOTICE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Chat Notice
    
    character_id of <Integer>
    unknown of <Integer>
    instance of <Integer>
    message of <String>
    """
    
    type = 37
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHAT_NOTICE.type, (Integer, Integer, Integer, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.unknown = self[1]
        self.categoty = 20000
        self.instance = self[2]
        self.message = self[3]
        
        # Extended message
        self.args = []
        self.mask = get_text(self.categoty, self.instance)
        
        data = self.message
        
        while data:
            arg_type, data = data[0], data[1:]
            
            if arg_type == "S":
                string, data = String.unpack(data)
                args.append(string)
            elif arg_type == "I":
                number, data = Integer.unpack(data)
                args.append(number)


class AOSP_FRIEND_UPDATE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Friend Update
    
    character_id of <Integer>
    online of <Integer>
    flags of <String>
    """
    
    type = 40
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_FRIEND_UPDATE.type, (Integer, Integer, String,), data)
    
    def __init__(self, data):
        self.character_id = self[0]
        self.online = self[1]
        self.flags = self[2]


class AOSP_FRIEND_REMOVE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Friend Remove
    
    character_id of <Integer>
    """
    
    type = 41
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_FRIEND_REMOVE.type, (Integer,), data)
    
    def __init__(self, data):
        self.character_id = self[0]


class AOSP_PRIVATE_CHANNEL_INVITE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Channel Invite
    
    channel_id of <Integer>
    """
    
    type = 50
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_INVITE.type, (Integer,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]


class AOSP_PRIVATE_CHANNEL_KICK(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Channel Kick
    
    channel_id of <Integer>
    """
    
    type = 51
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_KICK.type, (Integer,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]


class AOSP_PRIVATE_CHANNEL_CHARACTER_JOIN(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Channel Character Join
    
    channel_id of <Integer>
    character_id of <Integer>
    """
    
    type = 55
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_CHARACTER_JOIN.type, (Integer, Integer,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]
        self.character_id = self[1]


class AOSP_PRIVATE_CHANNEL_CHARACTER_LEAVE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Channel Character Leave
    
    channel_id of <Integer>
    character_id of <Integer>
    """
    
    type = 56
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_CHARACTER_LEAVE.type, (Integer, Integer,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]
        self.character_id = self[1]


class AOSP_PRIVATE_CHANNEL_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Private Channel Message
    
    channel_id of <Integer>
    character_id of <Integer>
    message of <String>
    unknown of <String>
    """
    
    type = 57
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PRIVATE_CHANNEL_MESSAGE.type, (Integer, Integer, String, String,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]
        self.character_id = self[1]
        self.message = self[2]
        self.unknown = self[3]


class AOSP_CHANNEL_JOIN(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Channel Join
    
    channel_id of <ChannelID>
    channel_name of <String>
    channel_status of <Integer>
    unknown of <String>
    """
    
    type = 60
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHANNEL_JOIN.type, (ChannelID, String, Integer, String,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]
        self.channel_name = self[1]
        self.channel_status = self[2]
        self.unknown = self[3]


class AOSP_CHANNEL_LEAVE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Channel Leave
    
    channel_id of <ChannelID>
    """
    
    type = 61
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHANNEL_LEAVE.type, (ChannelID,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]


class AOSP_CHANNEL_MESSAGE(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Channel Message
    
    channel_id of <ChannelID>
    character_id of <Integer>
    message of <String>
    unknown of <String>
    """
    
    type = 65
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_CHANNEL_MESSAGE.type, (ChannelID, Integer, String, String,), data)
    
    def __init__(self, data):
        self.channel_id = self[0]
        self.character_id = self[1]
        self.message = self[2]
        self.unknown = self[3]
        self.category = None
        self.instance = None
        
        # Extended message
        if self.character_id == 0L and self.message.startswith("~&"):
            def b85g(string):
                number = 0
                
                for i in range(5):
                    number = number * 85 + ord(string[i]) - 33
                
                return number, string[5:]
            
            # Parse arguments
            data = self.message[2:-1]
            
            self.category, data = b85g(data)
            self.instance, data = b85g(data)
            
            self.args = []
            self.mask = get_text(category, instance)
            
            while data:
                arg_type, data = data[0], data[1:]
                
                if arg_type == "s":
                    length = ord(data[0])
                    string, data = data[1:length], data[length:]
                    
                    args.append(string)
                elif arg_type in "iu":
                    number, data = b85g(data)
                    
                    args.append(number)
                elif arg_type == "R":
                    category, data = b85g(data)
                    instance, data = b85g(data)
                    
                    args.append(get_text(category, instance))


class AOSP_PING(ServerPacket):
    """
    Server to client Anarchy Online chat packet: Ping
    
    unknown of <String>
    """
    
    type = 100
    
    def __new__(Class, data):
        return ServerPacket.__new__(Class, AOSP_PING.type, (String,), data)
    
    def __init__(self, data):
        self.unknown = self[0]


### PACKETS TO SERVER ##########################################################


class AOCP_SEED(ClientPacket):
    """
    Client to server packet: Seed
    
    unknown of <Integer>
    character_id of <Integer>
    username of <String>
    login_key of <String>
    """
    
    type = 0
    
    def __new__(Class, character_id, username, login_key, unknown = AOFL_AUTH):
        return ClientPacket.__new__(Class, AOCP_SEED.type, (Integer(unknown), Integer(character_id), String(username), String(login_key),))
    
    def __init__(self, character_id, username, login_key, unknown = AOFL_AUTH):
        self.unknown = self[0]
        self.character_id = self[1]
        self.username = self[2]
        self.login_key = self[3]


class AOCP_AUTH(ClientPacket):
    """
    Client to server packet: Auth
    
    unknown of <Integer>
    username of <String>
    login_key of <String>
    """
    
    type = 2
    
    def __new__(Class, username, login_key, unknown = AOFL_AUTH):
        return ClientPacket.__new__(Class, AOCP_AUTH.type, (Integer(unknown), String(username), String(login_key),))
    
    def __init__(self, username, login_key, unknown = AOFL_AUTH):
        self.unknown = self[0]
        self.username = self[1]
        self.login_key = self[2]


class AOCP_LOGIN(ClientPacket):
    """
    Client to server packet: Login
    
    character_id of <Integer>
    """
    
    type = 3
    
    def __new__(Class, character_id):
        return ClientPacket.__new__(Class, AOCP_LOGIN.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        self.character_id = self[0]


class AOCP_CHARACTER_LOOKUP(ClientPacket):
    """
    Client to server packet: Character Lookup
    
    character_name of <String>
    """
    
    type = 21
    
    def __new__(Class, character_name):
        return ClientPacket.__new__(Class, AOCP_CHARACTER_LOOKUP.type, (String(character_name),))
    
    def __init__(self, character_name):
        self.character_name = self[0]


class AOCP_PRIVATE_MESSAGE(ClientPacket):
    """
    Client to server packet: Private Message
    
    character_id of <Integer>
    message of <String>
    unknown of <String>
    """
    
    type = 30
    
    def __new__(Class, character_id, message, unknown):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_MESSAGE.type, (Integer(character_id), String(message), String(unknown),))
    
    def __init__(self, character_id, message, unknown):
        self.character_id = self[0]
        self.message = self[1]
        self.unknown = self[2]


class AOCP_FRIEND_UPDATE(ClientPacket):
    """
    Client to server packet: Friend Update
    
    character_id of <Integer>
    flags of <String>
    """
    
    type = 40
    
    def __new__(Class, character_id, flags):
        return ClientPacket.__new__(Class, AOCP_FRIEND_UPDATE.type, (Integer(character_id), String(flags),))
    
    def __init__(self, character_id, flags):
        self.character_id = self[0]
        self.flags = self[1]


class AOCP_FRIEND_REMOVE(ClientPacket):
    """
    Client to server packet: Friend Remove
    
    character_id of <Integer>
    """
    
    type = 41
    
    def __new__(Class, character_id):
        return ClientPacket.__new__(Class, AOCP_FRIEND_REMOVE.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_INVITE(ClientPacket):
    """
    Client to server packet: Private Channel Invite
    
    character_id of <Integer>
    """
    
    type = 50
    
    def __new__(Class, character_id):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_INVITE.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_KICK(ClientPacket):
    """
    Client to server packet: Private Channel Kick
    
    character_id of <Integer>
    """
    
    type = 51
    
    def __new__(Class, character_id):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_KICK.type, (Integer(character_id),))
    
    def __init__(self, character_id):
        self.character_id = self[0]


class AOCP_PRIVATE_CHANNEL_JOIN(ClientPacket):
    """
    Client to server packet: Private Channel Join
    
    channel_id of <Integer>
    """
    
    type = 52
    
    def __new__(Class, owner_character_id):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_JOIN.type, (Integer(channel_id),))
    
    def __init__(self, owner_character_id):
        self.channel_id = self[0]


class AOCP_PRIVATE_CHANNEL_LEAVE(ClientPacket):
    """
    Client to server packet: Private Channel Leave
    
    channel_id of <Integer>
    """
    
    type = 53
    
    def __new__(Class, channel_id):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_LEAVE.type, (Integer(channel_id),))
    
    def __init__(self, channel_id):
        self.channel_id = self[0]


#class AOCP_PRIVATE_CHANNEL_KICKALL(ClientPacket):
#    """
#    Client to server packet: Private Channel Kick All
#    
#    no data
#    """
#    
#    type = 54
#    
#    def __new__(Class):
#        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_KICKALL.type, ())
#    
#    def __init__(self):
#        ClientPacket.__init__(self, AOCP_PRIVATE_CHANNEL_KICKALL.type, self)


class AOCP_PRIVATE_CHANNEL_MESSAGE(ClientPacket):
    """
    Client to server packet: Private Channel Message
    
    channel_id of <Integer>
    message of <String>
    unknown of <String>
    """
    
    type = 57
    
    def __new__(Class, channel_id, message, unknown = AOFL_PRIVATE_CHANNEL_MESSAGE):
        return ClientPacket.__new__(Class, AOCP_PRIVATE_CHANNEL_MESSAGE.type, (Integer(channel_id), String(message), String(unknown),))
    
    def __init__(self, channel_id, message, unknown = AOFL_PRIVATE_CHANNEL_MESSAGE):
        self.channel_id = self[0]
        self.message = self[1]
        self.unknown = self[2]


class AOCP_CHANNEL_MESSAGE(ClientPacket):
    """
    Client to server packet: Channel Message
    
    channel_id of <ChannelID>
    message of <String>
    unknown of <String>
    """
    
    type = 65
    
    def __new__(Class, channel_id, message, unknown = AOFL_CHANNEL_MESSAGE):
        return ClientPacket.__new__(Class, AOCP_CHANNEL_MESSAGE.type, (ChannelID(channel_id), String(message), String(unknown),))
    
    def __init__(self, channel_id, message, unknown = AOFL_CHANNEL_MESSAGE):
        self.channel_id = self[0]
        self.message = self[1]
        self.unknown = self[2]


class AOCP_PING(ClientPacket):
    """
    Client to server packet: Ping
    
    unknown of <String>
    """
    
    type = 100
    
    def __new__(Class, unknown = AOFL_PING):
        return ClientPacket.__new__(Class, AOCP_PING.type, (String(unknown),))
    
    def __init__(self, unknown = AOFL_PING):
        self.unknown = self[0]


class AOCP_CHAT_COMMAND(ClientPacket):
    """
    Client to server packet: Chat Command
    
    command of <TupleOfStrings>
    unknown of <Integer>
    """
    
    type = 120
    
    def __new__(Class, command, unknown = AOFL_CHAT_COMMAND):
        return ClientPacket.__new__(Class, AOCP_CHAT_COMMAND.type, (TupleOfStrings(command), Integer(unknown),))
    
    def __init__(self, command, unknown = AOFL_CHAT_COMMAND):
        self.command = self[0]
        self.unknown = self[1]


################################################################################


SERVER_PACKETS = {
    AOSP_SEED.type:                            AOSP_SEED,
    AOSP_LOGIN_OK.type:                        AOSP_LOGIN_OK,
    AOSP_AUTH_ERROR.type:                      AOSP_AUTH_ERROR,
    AOSP_CHARACTERS_LIST.type:                 AOSP_CHARACTERS_LIST,
    AOSP_CHARACTER_NAME.type:                  AOSP_CHARACTER_NAME,
    AOSP_CHARACTER_LOOKUP.type:                AOSP_CHARACTER_LOOKUP,
    AOSP_PRIVATE_MESSAGE.type:                 AOSP_PRIVATE_MESSAGE,
    AOSP_VICINITY_MESSAGE.type:                AOSP_VICINITY_MESSAGE,
    AOSP_BROADCAST_MESSAGE.type:               AOSP_BROADCAST_MESSAGE,
    AOSP_SYSTEM_MESSAGE.type:                  AOSP_SYSTEM_MESSAGE,
    AOSP_CHAT_NOTICE.type:                     AOSP_CHAT_NOTICE,
    AOSP_FRIEND_UPDATE.type:                   AOSP_FRIEND_UPDATE,
    AOSP_FRIEND_REMOVE.type:                   AOSP_FRIEND_REMOVE,
    AOSP_PRIVATE_CHANNEL_INVITE.type:          AOSP_PRIVATE_CHANNEL_INVITE,
    AOSP_PRIVATE_CHANNEL_KICK.type:            AOSP_PRIVATE_CHANNEL_KICK,
    AOSP_PRIVATE_CHANNEL_CHARACTER_JOIN.type:  AOSP_PRIVATE_CHANNEL_CHARACTER_JOIN,
    AOSP_PRIVATE_CHANNEL_CHARACTER_LEAVE.type: AOSP_PRIVATE_CHANNEL_CHARACTER_LEAVE,
    AOSP_PRIVATE_CHANNEL_MESSAGE.type:         AOSP_PRIVATE_CHANNEL_MESSAGE,
    AOSP_CHANNEL_JOIN.type:                    AOSP_CHANNEL_JOIN,
    AOSP_CHANNEL_LEAVE.type:                   AOSP_CHANNEL_LEAVE,
    AOSP_CHANNEL_MESSAGE.type:                 AOSP_CHANNEL_MESSAGE,
    AOSP_PING.type:                            AOSP_PING,
}

CLIENT_PACKETS = {
    AOCP_SEED.type:                            AOCP_SEED,
    AOCP_AUTH.type:                            AOCP_AUTH,
    AOCP_LOGIN.type:                           AOCP_LOGIN,
    AOCP_CHARACTER_LOOKUP.type:                AOCP_CHARACTER_LOOKUP,
    AOCP_PRIVATE_MESSAGE.type:                 AOCP_PRIVATE_MESSAGE,
    AOCP_FRIEND_UPDATE.type:                   AOCP_FRIEND_UPDATE,
    AOCP_FRIEND_REMOVE.type:                   AOCP_FRIEND_REMOVE,
    AOCP_PRIVATE_CHANNEL_INVITE.type:          AOCP_PRIVATE_CHANNEL_INVITE,
    AOCP_PRIVATE_CHANNEL_KICK.type:            AOCP_PRIVATE_CHANNEL_KICK,
    AOCP_PRIVATE_CHANNEL_JOIN.type:            AOCP_PRIVATE_CHANNEL_JOIN,
    AOCP_PRIVATE_CHANNEL_LEAVE.type:           AOCP_PRIVATE_CHANNEL_LEAVE,
    #AOCP_PRIVATE_CHANNEL_KICKALL.type:         AOCP_PRIVATE_CHANNEL_KICKALL,
    AOCP_PRIVATE_CHANNEL_MESSAGE.type:         AOCP_PRIVATE_CHANNEL_MESSAGE,
    AOCP_CHANNEL_MESSAGE.type:                 AOCP_CHANNEL_MESSAGE,
    AOCP_PING.type:                            AOCP_PING,
    AOCP_CHAT_COMMAND.type:                    AOCP_CHAT_COMMAND,
}
