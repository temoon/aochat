# -*- coding: utf-8 -*-



"""
Anarchy Online chat protocol: packets.
"""



from AOChat.Types import Integer, Integers, String, Strings, GroupID, AOTypeError
from AOChat.Characters import Character



### BASE CLASSES ###############################################################


class PacketError(IOError):
    pass

class ServerPacketError(PacketError):
    pass

class ClientPacketError(PacketError):
    pass


class Packet(object):
    """
    Anarchy Online chat protocol: base packet.
    """
    
    @staticmethod
    def pack(args):
        """
        Pack args to binary data.
        """
        
        try:
            data = "".join(map(lambda arg: arg.pack(arg), args))
        except AOTypeError, error:
            raise PacketError(error)
        
        return data
    
    @staticmethod
    def unpack(data, types):
        """
        Unpack args by type from binary data.
        """
        
        args = []
        
        for aotype in types:
            try:
                arg, data = aotype.unpack(data)
            except AOTypeError, error:
                raise PacketError(error)
            
            args.append(arg)
        
        return args
    
    def __init__(self, id):
        self.id = id
    
    def __repr__(self):
        return self.id


class ServerPacket(Packet):
    """
    Anarchy Online chat protocol: packet from server.
    """
    
    def __init__(self, id, data, types):
        Packet.__init__(self, id)
        
        self.args = Packet.unpack(data, types)


class ClientPacket(Packet):
    """
    Anarchy Online chat protocol: packet to server.
    """
    
    def __init__(self, id, *args):
        Packet.__init__(self, id)
        
        self.args = args[:]



### PACKETS FROM SERVER ########################################################


class AOSP_LOGIN_SEED(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_SEED packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 0, data, [String])
        
        self.seed = self.args[0]


class AOSP_LOGIN_OK(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_OK packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 5, data, [])


class AOSP_LOGIN_ERROR(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_ERROR packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 6, data, [String])
        
        self.message = self.args[0]


class AOSP_LOGIN_CHARLIST(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_CHARLIST packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 7, data, [Integers, Strings, Integers, Integers])
        
        self.chars = []
        
        for i in range(len(self.args[0])):
            self.chars.append(Character(self.args[0][i], self.args[1][i], self.args[2][i], self.args[3][i]))


class AOSP_CLIENT_UNKNOWN(ServerPacket):
    """
    Anarchy Online chat protocol: CLIENT_UNKNOWN packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 10, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_CLIENT_NAME(ServerPacket):
    """
    Anarchy Online chat protocol: CLIENT_NAME packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 20, data, [Integer, String])
        
        self.user_id = self.args[0]
        self.name = self.args[1]


class AOSP_LOOKUP_RESULT(ServerPacket):
    """
    Anarchy Online chat protocol: LOOKUP_RESULT packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 21, data, [Integer, String])
        
        self.user_id = self.args[0]
        self.name = self.args[1]


class AOSP_MSG_PRIVATE(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_PRIVATE packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 30, data, [Integer, String, String])
        
        self.user_id = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_VICINITY(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_VICINITY packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 34, data, [Integer, String, String])
        
        self.user_id = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_ANONVICINITY(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_ANONVICINITY packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 35, data, [String, String, String])
        
        self.user = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_SYSTEM(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_SYSTEM packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 36, data, [String])
        
        self.text = self.args[0]


class AOSP_MESSAGE_SYSTEM(ServerPacket):
    """
    Anarchy Online chat protocol: MESSAGE_SYSTEM packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 37, data, [Integer, Integer, Integer, String])
        
        self.client_id = self.args[0]
        self.window_id = self.args[1]
        self.message_id = self.args[2]
        self.message_args = self.args[3]


class AOSP_BUDDY_STATUS(ServerPacket):
    """
    Anarchy Online chat protocol: BUDDY_STATUS packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 40, data, [Integer, Integer, String])
        
        self.user_id = self.args[0]
        self.online = self.args[1]
        self.status = self.args[2]


class AOSP_BUDDY_REMOVED(ServerPacket):
    """
    Anarchy Online chat protocol: BUDDY_REMOVED packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 41, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_INVITE(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_INVITE packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 50, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_KICK(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_KICK packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 51, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_JOIN(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_JOIN packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 52, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_PART(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_PART packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 53, data, [Integer])
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_KICKALL(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_KICKALL packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 54, data, [])


class AOSP_PRIVGRP_CLIJOIN(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_CLIJOIN packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 55, data, [Integer, Integer])
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]


class AOSP_PRIVGRP_CLIPART(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_CLIPART packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 56, data, [Integer, Integer])
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]


class AOSP_PRIVGRP_MSG(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_MSG packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 57, data, [Integer, Integer, String, String])
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]
        self.text = self.args[2]
        self.blob = self.args[3]


class AOSP_GROUP_JOIN(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_JOIN packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 60, data, [GroupID, String, Integer, String])
        
        self.group_id = self.args[0]
        self.group_name = self.args[1]
        self.mute = self.args[2]
        self.status = self.args[3]


class AOSP_GROUP_PART(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_PART packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 61, data, [GroupID])
        
        self.group_id = self.args[0]


class AOSP_GROUP_MSG(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_MSG packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 65, data, [GroupID, Integer, String, String])
        
        self.group_id = self.args[0]
        self.user_id = self.args[1]
        self.text = self.args[2]
        self.blob = self.args[3]


class AOSP_PONG(ServerPacket):
    """
    Anarchy Online chat protocol: PONG packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 100, data, [String])
        
        self.string = self.args[0]


class AOSP_FORWARD(ServerPacket):
    """
    Anarchy Online chat protocol: FORWARD packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 110, data, [Integer, String])
        
        # TODO: ...


class AOSP_AMD_MUX_INFO(ServerPacket):
    """
    Anarchy Online chat protocol: AMD_MUX_INFO packet.
    """
    
    def __init__(self, data):
        ServerPacket.__init__(self, 1100, data, [Integers, Integers, Integers])
        
        # TODO: ...



### PACKETS TO SERVER ##########################################################


class AOCP_LOGIN_RESPONSE(ClientPacket):
    """
    Anarchy Online chat protocol: LOGIN_RESPONSE packet.
    """
    
    def __init__(self, username, login_key):
        ClientPacket.__init__(self, 2, Integer(0), String(username), String(login_key))


class AOCP_LOGIN_SELCHAR(ClientPacket):
    """
    Anarchy Online chat protocol: LOGIN_SELCHAR packet.
    """
    
    def __init__(self, user_id):
        ClientPacket.__init__(self, 3, Integer(user_id))


class AOCP_NAME_LOOKUP(ClientPacket):
    """
    Anarchy Online chat protocol: NAME_LOOKUP packet.
    """
    
    def __init__(self, name):
        ClientPacket.__init__(self, 21, String(name))


class AOCP_MSG_PRIVATE(ClientPacket):
    """
    Anarchy Online chat protocol: MSG_PRIVATE packet.
    """
    
    def __init__(self, user_id, text, blob):
        ClientPacket.__init__(self, 30, Integer(user_id), String(text), String(blob))


class AOCP_BUDDY_ADD(ClientPacket):
    """
    Anarchy Online chat protocol: BUDDY_ADD packet.
    """
    
    def __init__(self, user_id, status):
        ClientPacket.__init__(self, 40, Integer(user_id), String(status))


class AOCP_BUDDY_REMOVE(ClientPacket):
    """
    Anarchy Online chat protocol: BUDDY_REMOVE packet.
    """
    
    def __init__(self, user_id):
        ClientPacket.__init__(self, 41, Integer(user_id))


class AOCP_ONLINE_STATUS(ClientPacket):
    """
    Anarchy Online chat protocol: ONLINE_STATUS packet.
    """
    
    def __init__(self, online):
        ClientPacket.__init__(self, 42, Integer(online))


class AOCP_GROUP_DATASET(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_DATASET packet.
    """
    
    def __init__(self, group_id, mute):
        ClientPacket.__init__(self, 64, GroupID(group_id), Integer(mute), String(""))
        
        # TODO: ...


class AOCP_GROUP_MESSAGE(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_MESSAGE packet.
    """
    
    def __init__(self, group_id, text, blob):
        ClientPacket.__init__(self, 65, GroupID(group_id), String(text), String(blob))


class AOCP_GROUP_CLIMODE(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_CLIMODE packet.
    """
    
    def __init__(self, group_id):
        ClientPacket.__init__(self, 66, GroupID(group_id), Integer(0), Integer(0), Integer(0), Integer(0))
        
        # TODO: ...


class AOCP_CLIMODE_GET(ClientPacket):
    """
    Anarchy Online chat protocol: CLIMODE_GET packet.
    """
    
    def __init__(self, group_id):
        ClientPacket.__init__(self, 70, Integer(0), GroupID(group_id))
        
        # TODO: ...


class AOCP_CLIMODE_SET(ClientPacket):
    """
    Anarchy Online chat protocol: CLIMODE_SET packet.
    """
    
    def __init__(self):
        ClientPacket.__init__(self, 71, Integer(0), Integer(0), Integer(0), Integer(0))
        
        # TODO: ...


class AOCP_PING(ClientPacket):
    """
    Anarchy Online chat protocol: PING packet.
    """
    
    def __init__(self, string):
        ClientPacket.__init__(self, 100, String(string))


class AOCP_CHAT_COMMAND(ClientPacket):
    """
    Anarchy Online chat protocol: CHAT_COMMAND packet.
    """
    
    def __init__(self, command, value):
        ClientPacket.__init__(self, 120, String(command), String(value))
