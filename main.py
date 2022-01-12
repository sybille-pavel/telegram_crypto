import RSATelegram
import eel
import TelegramManager
import pprint as pp


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
    res = TelegramManager.get_messages(int(id), limit=5)

    for info in res:
        if info is None: continue

        if info["type"] == "document":
            name = info["value"]
            name = name.replace(" ", ".")
            name = name.split("\\")[1]
            name = name.split(".")

            if name[0] == "receiver" and name[-1] == "pem":
                crypto = RSATelegram.RSAMessages(id)
                cryptov = crypto.setCompanionPublicKey(open(info['value'].replace("\\", "/")).read())

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
