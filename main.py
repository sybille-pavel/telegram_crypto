import eel
import TelegramManager


@eel.expose
def get_chats():
    return TelegramManager.get_chats()


@eel.expose
def send_message(id, text):
    print(id, text)


@eel.expose
def get_messages(id):
    return TelegramManager.get_messages(id)


eel.init("web")
eel.start("main.html", size=(1200, 700))

