# -*- coding: utf-8 -*-


"""
Anarchy Online markup language
"""


def color(text, color):
    return '<font color="%s">%s</font>' % (color, text,)

def u(text):
    return '<u>%s</u>' % text

def center(text):
    return '<div align="center">%s</div>' % text

def right(text):
    return '<div align="right">%s</div>' % text

def br(count = 1):
    return '<br>' ** count

def text(text, link):
    return '<a href="text://%s">%s</a>' % (text.replace('"', '\\"'), link,)

def command(command, link):
    if not command.startswith("/"):
        command = "/%s" % command
    
    return '<a href="chatcmd://%s">%s</a>' % (command, link,)

def gui(id):
    return '<img src="tdb://id:%s">' % id.upper()

def icon(id):
    return '<img src="rdb://%d>"' % id

