import RSATelegram
import eel
import TelegramManager

@eel.expose
def get_chats():
    return TelegramManager.get_chats()


@eel.expose
def send_message(id, text):
    crypto = RSATelegram.RSAMessages(id)
    if crypto.getCompanionPublicKey():
        TelegramManager.send_file(id, crypto.encryptData(text))
    else:
        print("Ошибка ебанный рот")


@eel.expose
def send_public_key(id):
    crypto = RSATelegram.RSAMessages(id)
    TelegramManager.send_file(int(id), crypto.getPathPublicKey())
    crypto.setChatInfo(1)


@eel.expose
def get_messages(id):
    return TelegramManager.get_messages(int(id), limit=5)

@eel.expose
def get_chat_info(id):
    crypto = RSATelegram.RSAMessages(id)
    return crypto.getChatInfo()

@eel.expose
def get_companion_public_key(id):
    crypto = RSATelegram.RSAMessages(id)
    return crypto.getCompanionPublicKey()

# @TelegramManager.client.on(TelegramManager.events.NewMessage())
# async def normal_handler(event):
#     print(parse_message(event.message))


# def function1():
#     TelegramManager.client.run_until_disconnected()


eel.init("web")
eel.start("main.html", size=(1200, 700))

