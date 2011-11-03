# -*- coding: utf-8 -*-


"""
Python implementation of Anarchy Online chat protocol.
"""


import socket
import select
import struct
import random

from aochat.packets import *


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
#    AOCP_PRIVATE_CHANNEL_KICKALL.type:         AOCP_PRIVATE_CHANNEL_KICKALL,
    AOCP_PRIVATE_CHANNEL_MESSAGE.type:         AOCP_PRIVATE_CHANNEL_MESSAGE,
    AOCP_CHANNEL_MESSAGE.type:                 AOCP_CHANNEL_MESSAGE,
    AOCP_PING.type:                            AOCP_PING,
    AOCP_CHAT_COMMAND.type:                    AOCP_CHAT_COMMAND,
}



### LOGIN KEY GENERATOR ########################################################


def _generate_login_key(server_key, username, password):
    """
    Generate login key by server_key, username and password.
    """
    
    dhY = 0x9C32CC23D559CA90FC31BE72DF817D0E124769E809F936BC14360FF4BED758F260A0D596584EACBBC2B88BDD410416163E11DBF62173393FBC0C6FEFB2D855F1A03DEC8E9F105BBAD91B3437D8EB73FE2F44159597AA4053CF788D2F9D7012FB8D7C4CE3876F7D6CD5D0C31754F4CD96166708641958DE54A6DEF5657B9F2E92L
    dhN = 0xECA2E8C85D863DCDC26A429A71A9815AD052F6139669DD659F98AE159D313D13C6BF2838E10A69B6478B64A24BD054BA8248E8FA778703B418408249440B2C1EDD28853E240D8A7E49540B76D120D3B1AD2878B1B99490EB4A2A5E84CAA8A91CECBDB1AA7C816E8BE343246F80C637ABC653B893FD91686CF8D32D6CFE5F2A6FL
    dhG = 0x5L
    dhx = random.randrange(0, 2 ** 256)
    
    dhX = pow(dhG, dhx, dhN)
    dhK = int(("%x" % pow(dhY, dhx, dhN))[:32], 16)
    
    challenge = "%s|%s|%s" % (username, server_key, password)
    prefix    = struct.pack(">Q", random.randrange(0, 2 ** 64))
    length    = 8 + 4 + len(challenge)
    pad       = " " * ((8 - length % 8) % 8)
    
    plain = prefix + struct.pack(">I", len(challenge)) + challenge + pad
    
    return "%0x-%s" % (dhX, _crypt(dhK, plain))


def _crypt(key, plain):
    """
    Crypt plain text with key.
    """
    
    if len(plain) % 8 != 0:
        raise ValueError("Length of plain text must be multiple of 8.")
    
    crypted = ""
    
    cycle  = [0, 0]
    result = [0, 0]
    
    keys = [socket.ntohl(int(s, 16)) for s in struct.unpack("8s" * (len(str(key)) / 8), "%x" % key)]
    data = struct.unpack("I" * (len(plain) / 4), plain)
    
    i = 0
    
    while i < len(data):
        cycle[0] = data[i] ^ result[0]
        cycle[1] = data[i + 1] ^ result[1]
        
        result = _tea_encrypt(cycle, keys)
        
        crypted += "%08x%08x" % (socket.htonl(result[0]) & 0xFFFFFFFFL, socket.htonl(result[1]) & 0xFFFFFFFFL)
        
        i += 2
    
    return crypted


def _tea_encrypt(cycle, keys):
    """
    TEA encrypt.
    """
    
    a, b = cycle
    sum = 0
    delta = 0x9E3779B9L
    
    i = 32
    
    while i:
        sum = (sum + delta) & 0xFFFFFFFFL
        
        a += (((b << 4 & 0xFFFFFFF0L) + keys[0]) ^ (b + sum) ^ ((b >> 5 & 0x7FFFFFFL) + keys[1])) & 0xFFFFFFFFL
        a &= 0xFFFFFFFFL
        
        b += (((a << 4 & 0xFFFFFFF0L) + keys[2]) ^ (a + sum) ^ ((a >> 5 & 0x7FFFFFFL) + keys[3])) & 0xFFFFFFFFL
        b &= 0xFFFFFFFFL
        
        i -= 1
    
    return a, b



### ANARCHY ONLINE CHAT PROTOCOL ###############################################


class ChatError(Exception):
    pass

class UnexpectedPacket(ChatError):
    pass


class Chat(object):
    """
    Anarchy Online chat protocol implementation.
    """
    
    def __init__(self, username, password, host, port, timeout = 10):
        # Initialize connection
        try:
            self.socket = socket.create_connection((host, port,), timeout)
        except socket.error, error:
            raise ChatError("Socket error %s: %s" % tuple(error))
        
        # Wait server key and generate login key
        try:
            server_key = self.wait_packet(AOSP_SEED).server_key
            login_key  = _generate_login_key(server_key, username, password)
        except UnexpectedPacket, (type, packet):
            raise ChatError("Invalid greeting packet: %s" % type)
        
        # Authenticate
        try:
            self.character  = None
            self.characters = self.send_packet(AOCP_AUTH(username, login_key), AOSP_CHARACTERS_LIST, AOSP_AUTH_ERROR).characters
        except UnexpectedPacket, (type, packet):
            raise ChatError(packet.message)
    
    def __read_socket(self, bytes):
        data = ""
        
        while bytes > 0:
            try:
                chunk = self.socket.recv(bytes)
            except socket.error, error:
                raise ChatError("Socket error %s: %s" % tuple(error))
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
                raise ChatError("Socket error %s: %s" % tuple(error))
            except socket.timeout:
                raise ChatError("Connection timed out.")
            
            if sent == 0:
                raise ChatError("Connection broken.")
            
            data = data[sent:]
            bytes = bytes - sent
    
    def wait_packet(self, Expect = None, Error = None):
        """
        Wait packet from server.
        """
        
        # Read data from server
        head = self.__read_socket(4)
        packet_type, packet_length = struct.unpack(">2H", head)
        data = self.__read_socket(packet_length)
        
        if Expect:
            # Check packet type
            if packet_type != Expect.type:
                if Error and packet_type == Error.type:
                    # Make error packet
                    packet = Error(data)
                    
                    raise UnexpectedPacket(packet_type, packet)
                else:
                    raise ChatError("Unexpected error.")
            
            # Make expected packet
            packet = Expect(data)
        else:
            try:
                packet = SERVER_PACKETS[packet_type](data)
            except KeyError:
                raise UnexpectedPacket(packet_type, data)
        
        return packet
    
    def send_packet(self, packet, Expect = None, Error = None):
        """
        Send packet to server.
        """
        
        # Pack
        data = packet.pack()
        
        # Send data to server
        self.__write_socket(data)
        
        if Expect:
            return self.wait_packet(Expect, Error)
    
    def login(self, character_id):
        """
        Login to chat.
        """
        
        # Lookup character
        for character in self.characters:
            if character_id == character.id:
                break
        else:
            raise ChatError("no valid characters to login.")
        
        # Login with selected character
        try:
            self.send_packet(AOCP_LOGIN(character_id), AOSP_LOGIN_OK, AOSP_AUTH_ERROR)
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
    
    def send_private_message(self, character_id, message):
        """
        Send private message to player.
        """
        
        self.send_packet(AOCP_PRIVATE_MESSAGE(character_id, message, AOFL_PRIVATE_MESSAGE))
    
    def send_private_channel_message(self, channel_id, message):
        """
        Send message to private channel.
        """
        
        self.send_packet(AOCP_PRIVATE_CHANNEL_MESSAGE(channel_id, message, AOFL_PRIVATE_CHANNEL_MESSAGE))
    
    def send_channel_message(self, channel_id, message):
        """
        Send message to channel.
        """
        
        self.send_packet(AOCP_CHANNEL_MESSAGE(channel_id, message, AOFL_CHANNEL_MESSAGE))
    
    def private_channel_invite(self, character_id):
        """
        Invite to private channel.
        """
        
        self.send_packet(AOCP_PRIVATE_CHANNEL_INVITE(character_id))
    
    def private_channel_kick(self, character_id):
        """
        Kick from private channel.
        """
        
        self.send_packet(AOCP_PRIVATE_CHANNEL_KICK(character_id))
    
    def ping(self, message = "PING"):
        """
        Send ping to chat server.
        """
        
        self.send_packet(AOCP_PING())
    
    def start(self, callback, ping_interval = 60000):
        """
        Start chat.
        """
        
        poll = select.poll()
        poll.register(self.socket, select.POLLIN)
        
        while True:
            try:
                events = poll.poll(ping_interval)
                
                for socket, event in events:
                    if event == select.POLLIN:
                        try:
                            packet = self.wait_packet()
                        except UnexpectedPacket, (type, data):
                            print "Unexpected packet %s: %s" % (type, repr(data))
                            continue
                        
                        callback(self, packet)
                    elif event == select.POLLHUP:
                        return
                    elif event == select.POLLERR:
                        return
                
                if not events:
                    self.ping()
            except KeyboardInterrupt:
                break
