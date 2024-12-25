import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

@eel.expose
def get_lessons(login, password):
    driver = webdriver.Firefox()
    table = None
    try:
        driver.get("https://studlk.susu.ru")
        driver.find_element(By.ID, "UserName_I").send_keys(login)
        driver.find_element(By.ID, "dxPassword_I").send_keys(password)
        driver.find_element(By.ID, "LoginBtn").click()

        driver.get("https://studlk.susu.ru/ru/StudyPlan/StudyPlanView")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "gvStudyPlan_tccell1_1"))
            )
        except:
            pass
        table = driver.find_element(By.ID, "gvStudyPlan_DXMainTable").get_attribute("outerHTML")
    finally:
        driver.quit()
    return table

eel.init("./other/gui")

eel.start("login.html", mode="edge", host="localhost", port=2700, block=True, size=(1080, 720), position=(800, 250))