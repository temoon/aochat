# -*- coding: utf-8 -*-



"""
Anarchy Online chat protocol: packets.
"""



from AOChat.Types import Integer, Integers, String, Strings, GroupID
from AOChat.Characters import Character



### BASE CLASSES ###############################################################


class Packet(object):
    """
    Anarchy Online chat protocol: base packet.
    """
    
    type = None
    
    @staticmethod
    def pack(args):
        """
        Pack to binary data.
        """
        
        return "".join(map(lambda arg: arg.pack(arg), args))
    
    @staticmethod
    def unpack(data, types):
        """
        Unpack binary data.
        """
        
        args = []
        
        for arg_type in types:
            arg, data = arg_type.unpack(data)
            args.append(arg)
        
        return args


class ServerPacket(Packet):
    """
    Anarchy Online chat protocol: packet from server.
    """
    
    def __init__(self, data, types):
        self.args = Packet.unpack(data, types)


class ClientPacket(Packet):
    """
    Anarchy Online chat protocol: packet to server.
    """
    
    def __init__(self, *args):
        self.args = args[:]



### PACKETS FROM SERVER ########################################################


class AOSP_LOGIN_SEED(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_SEED packet.
    """
    
    type = 0
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (String,))
        
        self.seed = self.args[0]


class AOSP_LOGIN_OK(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_OK packet.
    """
    
    type = 5
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, ())


class AOSP_LOGIN_ERROR(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_ERROR packet.
    """
    
    type = 6
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (String,))
        
        self.message = self.args[0]


class AOSP_LOGIN_CHARLIST(ServerPacket):
    """
    Anarchy Online chat protocol: LOGIN_CHARLIST packet.
    """
    
    type = 7
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integers, Strings, Integers, Integers,))
        
        self.characters = []
        
        for i in range(len(self.args[0])):
            self.characters.append(Character(self.args[0][i], self.args[1][i], self.args[2][i], self.args[3][i]))


class AOSP_CLIENT_UNKNOWN(ServerPacket):
    """
    Anarchy Online chat protocol: CLIENT_UNKNOWN packet.
    """
    
    type = 10
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_CLIENT_NAME(ServerPacket):
    """
    Anarchy Online chat protocol: CLIENT_NAME packet.
    """
    
    type = 20
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, String,))
        
        self.user_id = self.args[0]
        self.name = self.args[1]


class AOSP_LOOKUP_RESULT(ServerPacket):
    """
    Anarchy Online chat protocol: LOOKUP_RESULT packet.
    """
    
    type = 21
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, String,))
        
        self.user_id = self.args[0]
        self.name = self.args[1]


class AOSP_MSG_PRIVATE(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_PRIVATE packet.
    """
    
    type = 30
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, String, String,))
        
        self.user_id = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_VICINITY(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_VICINITY packet.
    """
    
    type = 34
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, String, String,))
        
        self.user_id = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_ANONVICINITY(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_ANONVICINITY packet.
    """
    
    type = 35
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (String, String, String,))
        
        self.user = self.args[0]
        self.text = self.args[1]
        self.blob = self.args[2]


class AOSP_MSG_SYSTEM(ServerPacket):
    """
    Anarchy Online chat protocol: MSG_SYSTEM packet.
    """
    
    type = 36
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (String,))
        
        self.text = self.args[0]


class AOSP_MESSAGE_SYSTEM(ServerPacket):
    """
    Anarchy Online chat protocol: MESSAGE_SYSTEM packet.
    """
    
    type = 37
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, Integer, Integer, String,))
        
        self.client_id = self.args[0]
        self.window_id = self.args[1]
        self.message_id = self.args[2]
        self.message_args = self.args[3]


class AOSP_BUDDY_STATUS(ServerPacket):
    """
    Anarchy Online chat protocol: BUDDY_STATUS packet.
    """
    
    type = 40
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, Integer, String,))
        
        self.user_id = self.args[0]
        self.online = self.args[1]
        self.status = self.args[2]


class AOSP_BUDDY_REMOVED(ServerPacket):
    """
    Anarchy Online chat protocol: BUDDY_REMOVED packet.
    """
    
    type = 41
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_INVITE(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_INVITE packet.
    """
    
    type = 50
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_KICK(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_KICK packet.
    """
    
    type = 51
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_JOIN(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_JOIN packet.
    """
    
    type = 52
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_PART(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_PART packet.
    """
    
    type = 53
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer,))
        
        self.user_id = self.args[0]


class AOSP_PRIVGRP_KICKALL(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_KICKALL packet.
    """
    
    type = 54
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, ())


class AOSP_PRIVGRP_CLIJOIN(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_CLIJOIN packet.
    """
    
    type = 55
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, Integer,))
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]


class AOSP_PRIVGRP_CLIPART(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_CLIPART packet.
    """
    
    type = 56
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, Integer,))
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]


class AOSP_PRIVGRP_MSG(ServerPacket):
    """
    Anarchy Online chat protocol: PRIVGRP_MSG packet.
    """
    
    type = 57
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, Integer, String, String,))
        
        self.user_a_id = self.args[0]
        self.user_b_id = self.args[1]
        self.text = self.args[2]
        self.blob = self.args[3]


class AOSP_GROUP_JOIN(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_JOIN packet.
    """
    
    type = 60
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (GroupID, String, Integer, String,))
        
        self.group_id = self.args[0]
        self.group_name = self.args[1]
        self.mute = self.args[2]
        self.status = self.args[3]


class AOSP_GROUP_PART(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_PART packet.
    """
    
    type = 61
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (GroupID,))
        
        self.group_id = self.args[0]


class AOSP_GROUP_MSG(ServerPacket):
    """
    Anarchy Online chat protocol: GROUP_MSG packet.
    """
    
    type = 65
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (GroupID, Integer, String, String,))
        
        self.group_id = self.args[0]
        self.user_id = self.args[1]
        self.text = self.args[2]
        self.blob = self.args[3]


class AOSP_PONG(ServerPacket):
    """
    Anarchy Online chat protocol: PONG packet.
    """
    
    type = 100
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (String,))
        
        self.string = self.args[0]


class AOSP_FORWARD(ServerPacket):
    """
    Anarchy Online chat protocol: FORWARD packet.
    """
    
    type = 110
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integer, String,))
        
        # TODO: ...


class AOSP_AMD_MUX_INFO(ServerPacket):
    """
    Anarchy Online chat protocol: AMD_MUX_INFO packet.
    """
    
    type = 1100
    
    def __init__(self, data):
        ServerPacket.__init__(self, data, (Integers, Integers, Integers,))
        
        # TODO: ...



### PACKETS TO SERVER ##########################################################


class AOCP_LOGIN_RESPONSE(ClientPacket):
    """
    Anarchy Online chat protocol: LOGIN_RESPONSE packet.
    """
    
    type = 2
    
    def __init__(self, username, login_key):
        ClientPacket.__init__(self, Integer(0), String(username), String(login_key))


class AOCP_LOGIN_SELCHAR(ClientPacket):
    """
    Anarchy Online chat protocol: LOGIN_SELCHAR packet.
    """
    
    type = 3
    
    def __init__(self, user_id):
        ClientPacket.__init__(self, Integer(user_id))


class AOCP_NAME_LOOKUP(ClientPacket):
    """
    Anarchy Online chat protocol: NAME_LOOKUP packet.
    """
    
    type = 21
    
    def __init__(self, name):
        ClientPacket.__init__(self, String(name))


class AOCP_MSG_PRIVATE(ClientPacket):
    """
    Anarchy Online chat protocol: MSG_PRIVATE packet.
    """
    
    type = 30
    
    def __init__(self, user_id, text, blob):
        ClientPacket.__init__(self, Integer(user_id), String(text), String(blob))


class AOCP_BUDDY_ADD(ClientPacket):
    """
    Anarchy Online chat protocol: BUDDY_ADD packet.
    """
    
    type = 40
    
    def __init__(self, user_id, status):
        ClientPacket.__init__(self, Integer(user_id), String(status))


class AOCP_BUDDY_REMOVE(ClientPacket):
    """
    Anarchy Online chat protocol: BUDDY_REMOVE packet.
    """
    
    type = 41
    
    def __init__(self, user_id):
        ClientPacket.__init__(self, Integer(user_id))


class AOCP_ONLINE_STATUS(ClientPacket):
    """
    Anarchy Online chat protocol: ONLINE_STATUS packet.
    """
    
    type = 42
    
    def __init__(self, online):
        ClientPacket.__init__(self, Integer(online))


class AOCP_GROUP_DATASET(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_DATASET packet.
    """
    
    type = 64
    
    def __init__(self, group_id, mute):
        ClientPacket.__init__(self, GroupID(group_id), Integer(mute), String(""))
        
        # TODO: ...


class AOCP_GROUP_MESSAGE(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_MESSAGE packet.
    """
    
    type = 65
    
    def __init__(self, group_id, text, blob):
        ClientPacket.__init__(self, GroupID(group_id), String(text), String(blob))


class AOCP_GROUP_CLIMODE(ClientPacket):
    """
    Anarchy Online chat protocol: GROUP_CLIMODE packet.
    """
    
    type = 66
    
    def __init__(self, group_id):
        ClientPacket.__init__(self, GroupID(group_id), Integer(0), Integer(0), Integer(0), Integer(0))
        
        # TODO: ...


class AOCP_CLIMODE_GET(ClientPacket):
    """
    Anarchy Online chat protocol: CLIMODE_GET packet.
    """
    
    type = 70
    
    def __init__(self, group_id):
        ClientPacket.__init__(self, Integer(0), GroupID(group_id))
        
        # TODO: ...


class AOCP_CLIMODE_SET(ClientPacket):
    """
    Anarchy Online chat protocol: CLIMODE_SET packet.
    """
    
    type = 71
    
    def __init__(self):
        ClientPacket.__init__(self, Integer(0), Integer(0), Integer(0), Integer(0))
        
        # TODO: ...


class AOCP_PING(ClientPacket):
    """
    Anarchy Online chat protocol: PING packet.
    """
    
    type = 100
    
    def __init__(self, string):
        ClientPacket.__init__(self, String(string))


class AOCP_CHAT_COMMAND(ClientPacket):
    """
    Anarchy Online chat protocol: CHAT_COMMAND packet.
    """
    
    type = 120
    
    def __init__(self, command, value):
        ClientPacket.__init__(self, String(command), String(value))
