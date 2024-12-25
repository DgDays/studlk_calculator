import eel
import selenium



eel.init("./other/gui")

eel.start("login.html", mode="edge", host="localhost", port=2700, block=True, size=(1080, 720), position=(800, 250))