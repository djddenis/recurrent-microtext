from __future__ import unicode_literals
import socket
import string
import codecs
from datetime import datetime
import os

# some user data, change as per your taste
SERVER = 'irc.chat.twitch.tv'
PORT = 6667
NICKNAME = 'djdenis_chat_filter_bot'
OAUTH = 'oauth:tzhqfe6tfarfis8hbk4ppcv05ttmsz'
CHANNEL = '#imaqtpie'

# open a socket to handle the connection
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# open a connection with the server
def irc_conn():
    IRC.connect((SERVER, PORT))


# simple function to send data through the socket
def send_data(command):
    IRC.send(command + '\n')


# join the channel
def join(channel):
    send_data("JOIN %s" % channel)


# send login data (customizable)
def login():
    send_data("PASS " + OAUTH)
    send_data("NICK " + NICKNAME)

irc_conn()
login()
join(CHANNEL)

channel_path = '{0}\\messages\\{1}\\'.format(os.getcwd(), CHANNEL.lstrip('#'))
filename = datetime.now().strftime('%d_%m_%H%M')

if not os.path.exists(channel_path):
    os.makedirs(channel_path)

decode_error_count = 0
while True:
    try:
        buff = IRC.recv(4092).decode('utf-8')
        msg = string.split(buff)
        if msg and msg[0] == "PING":  # check if server have sent ping command
            send_data("PONG %s" % msg[1])  # answer with pong as per RFC 1459
    except UnicodeDecodeError:
        decode_error_count += 1
        buff = 'DECODE ERROR ' + decode_error_count
    with codecs.open(channel_path + filename, 'a', 'utf-8') as f:
        formatted_with_timestamp = ':{1} {0}'.format(buff, datetime.now().strftime('%H%M'))
        f.write(formatted_with_timestamp)
        print formatted_with_timestamp

