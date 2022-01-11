#import eel
import TelegramManager

TelegramManager.send_file("vitalyi_shpagin", "web/main.html")

exit()

eel.init("web")
eel.start("main.html", size=(1200, 700))

