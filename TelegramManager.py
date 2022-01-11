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


def parse_message(msg):
    try:
        e = {
            'msg_id': msg.id,
            'type': '',
            'value': '',
            'date': str(msg.date)
        }

        if msg.media is not None:
            try:
                e['type'] = 'document'
            except:
                e['type'] = 'photo'

            e['value'] = client.download_media(message=msg, file="media/")

        else:
            e['type'] = 'text'
            e['value'] = msg.message

        try:
            e['from'] = msg.from_id.user_id
        except:
            e['from']: False

        return e
    except:
        return None


# @client.on(events.NewMessage())
# async def normal_handler(event):
#     print(parse_message(event.message))
#
# client.run_until_disconnected()


def get_messages(id, limit=10):
    messages = client.get_messages(id, limit=limit)
    res = []

    for msg in messages:
        res.append(parse_message(msg))

    return res


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


def send_file(id, file):
    client.send_file(id, file)
