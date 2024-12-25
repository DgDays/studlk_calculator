import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

geckodriver_path = "./geckodriver"

def get_lessons(login, password):
    driver = webdriver.Firefox(executable_path = geckodriver_path)
    try:
        driver.get("https://studlk.susu.ru")
    finally:
        driver.quit()
    return True

eel.init("./other/gui")

eel.start("login.html", mode="edge", host="localhost", port=2700, block=True, size=(1080, 720), position=(800, 250))