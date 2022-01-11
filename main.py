#import eel
import TelegramManager

print(TelegramManager.get_chats())

exit()

eel.init("web")
eel.start("main.html", size=(1200, 700))

