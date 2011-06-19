# -*- coding: utf-8 -*-



"""
Anarchy Online chat protocol: login key generator.
"""



import random
import struct
import socket



def generate_login_key(server_key, username, password):
    """
    Generate login key by SEED, username and password.
    """
    
    dhY = 0x9c32cc23d559ca90fc31be72df817d0e124769e809f936bc14360ff4bed758f260a0d596584eacbbc2b88bdd410416163e11dbf62173393fbc0c6fefb2d855f1a03dec8e9f105bbad91b3437d8eb73fe2f44159597aa4053cf788d2f9d7012fb8d7c4ce3876f7d6cd5d0c31754f4cd96166708641958de54a6def5657b9f2e92L
    dhN = 0xeca2e8c85d863dcdc26a429a71a9815ad052f6139669dd659f98ae159d313d13c6bf2838e10a69b6478b64a24bd054ba8248e8fa778703b418408249440b2c1edd28853e240d8a7e49540b76d120d3b1ad2878b1b99490eb4a2a5e84caa8a91cecbdb1aa7c816e8be343246f80c637abc653b893fd91686cf8d32d6cfe5f2a6fL
    dhG = 0x5L
    dhx = random.randrange(0, 2 ** 256)
    
    dhX = pow(dhG, dhx, dhN)
    dhK = int(("%x" % pow(dhY, dhx, dhN))[:32], 16)
    
    challenge = "%s|%s|%s" % (username, server_key, password)
    prefix    = struct.pack(">Q", random.randrange(0, 2 ** 64))
    length    = 8 + 4 + len(challenge)
    pad       = " " * ((8 - length % 8) % 8)
    
    plain = prefix + struct.pack(">I", len(challenge)) + challenge + pad
    
    return "%0x-%s" % (dhX, crypt(dhK, plain))


def crypt(key, plain):
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
        
        result = tea_encrypt(cycle, keys)
        
        crypted += "%08x%08x" % (socket.htonl(result[0]) & 0xffffffffL, socket.htonl(result[1]) & 0xffffffffL)
        
        i += 2
    
    return crypted


def tea_encrypt(cycle, keys):
    """
    TEA encrypt.
    """
    
    a, b = cycle
    sum = 0
    delta = 0x9e3779b9L
    
    i = 32
    
    while i:
        sum = (sum + delta) & 0xffffffffL
        
        a += (((b << 4 & 0xfffffff0L) + keys[0]) ^ (b + sum) ^ ((b >> 5 & 0x7ffffffL) + keys[1])) & 0xffffffffL
        a &= 0xffffffffL
        
        b += (((a << 4 & 0xfffffff0L) + keys[2]) ^ (a + sum) ^ ((a >> 5 & 0x7ffffffL) + keys[3])) & 0xffffffffL
        b &= 0xffffffffL
        
        i -= 1
    
    return a, b
