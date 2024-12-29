import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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
        # Временно отключил
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]").click()
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "gvStudyPlan_tccell1_1"))
            )
        except:
            pass
        table = driver.find_element(By.ID, "gvStudyPlan_DXMainTable").get_attribute("outerHTML")
        table = BeautifulSoup(table, "html.parser")

        raws = table.find_all("tr")[3:]

        for i in raws:
            tds = i.find_all("td")
            if "семестр" in tds[1].text.lower():
                i['class'] = i.get('class', []) + ['clickable']
                i['onclick'] = "toggleDetails(this)"
            else:
                i['class'] = i.get('class', []) + ['details']

        # ЗАдед для будущей логики
        '''links = table.find_elements(By.TAG_NAME, "a")
        journal_links = []
        for i in links:
            if "Журнал" in i.get_attribute("innerHTML"):
                journal_links.append(i)'''
    finally:
        driver.quit()
    return table.prettify()

eel.init("./other/gui")
eel.start("login.html", mode="geckodriver", host="localhost", port=2700, block=True)