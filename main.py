import RSATelegram
import eel
import TelegramManager


@eel.expose
def get_chats():
    return TelegramManager.get_chats()


@eel.expose
def send_message(id, text):
    print(id, text)

@eel.expose
def send_public_key(id):
	crypto = RSATelegram.RSAMessages(id)
	TelegramManager.send_file(id, crypto.getPathPublicKey())



@eel.expose
def get_messages(id):
    print(id)
    res = TelegramManager.get_messages(int(id), limit=5)
    return res


eel.init("web")
eel.start("main.html", size=(1200, 700))

