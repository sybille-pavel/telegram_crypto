from telethon import TelegramClient, events, utils, functions, types
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import datetime
import pprint as pp

api_id = '1522909'
api_hash = 'fc0e17812ae016a0345db633499a2d98'
name = 'session'


client = TelegramClient('session', api_id, api_hash, retry_delay=30, auto_reconnect=True).start()


def get_chats():
    chats = []
    result = client(GetDialogsRequest(
                 offset_date='',
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=10000,
                 hash=0
             ))

    for i in result.users:
        chats.append((i.id, i.username))

    return chats


def send_file():
    pass
