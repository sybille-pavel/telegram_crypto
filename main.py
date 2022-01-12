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
    TelegramManager.send_file(id, crypto.getPathPublicKey())
    crypto.setChatInfo(1)


@eel.expose
def get_messages(id):
    res = TelegramManager.get_messages(int(id), limit=5)
    return res

@eel.expose
def get_chat_info(id):
    crypto = RSATelegram.RSAMessages(id)
    return crypto.getChatInfo()

@eel.expose
def get_companion_public_key(id):
    crypto = RSATelegram.RSAMessages(id)
    return crypto.getCompanionPublicKey()

eel.init("web")
eel.start("main.html", size=(1200, 700))
