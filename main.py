import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

log, passw, main_table = ['']*3

@eel.expose
def get_lessons(login, password):
    global log, passw, main_table
    log, passw = login, password
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
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

        links = table.find_all("a")
        for i in links:
            if "журнал" in i.text.lower():
                p = table.new_tag('p', **{'class': 'link-like'})  # Создаем новый <p> с классом
                p.string = i.string  # Копируем текст из <a>
                p['onclick'] = f'calculate("{i['href']}",{1 if "да" in i.parent.parent.find_all("td")[12].text.lower() else 0})'
                i.replace_with(p) 
                
    finally:
        driver.quit()
    main_table = table.prettify()
    return main_table

@eel.expose
def calculate(link, flag):
    global log, passw
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    table = None
    try:
        driver.get("https://studlk.susu.ru")
        driver.find_element(By.ID, "UserName_I").send_keys(log)
        driver.find_element(By.ID, "dxPassword_I").send_keys(passw)
        driver.find_element(By.ID, "LoginBtn").click()

        driver.get("https://studlk.susu.ru"+link)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "gvStudyPlan_tccell1_1"))
            )
        except:
            pass
        table = driver.find_element(By.ID, "MarkJournalPivotGrid_PT").get_attribute("outerHTML")
        table = BeautifulSoup(table, "html.parser")
        table1 = table.find(id="MarkJournalPivotGrid_CVSCell_SCDTable").find_all("tr")
        points = table.find(id="MarkJournalPivotGrid_DCSCell_SCDTable").find_all("tr")
        table = BeautifulSoup("", "html.parser")
        table.insert(0, table.new_tag("table"))

        weight_str, points_str = ['']*2

        for raw in range(len(points)):
            for i in range(len(points[raw].find_all("td"))):
                if raw % 2:
                    if i % 2 and all(char in "1234567890," for char in points[raw].find_all("td")[i].decode_contents()):
                        points_str += f"{points[raw].find_all("td")[i].decode_contents()} "
                else:
                    if points[raw].find_all("td")[i].decode_contents() != '':
                        weight_str += f"{points[raw].find_all("td")[i].decode_contents()} "

        for i in table1:
            table.find("table").append(i)
        for i in points:
            table.find("table").append(i)
        back_button = table.new_tag('button', **{'class': 'back-button', "onclick":"backToMain()"})
        back_button.string = 'Возврат'
        table.insert(0, back_button)
    finally:
        driver.quit()
    return table.prettify()

@eel.expose
def backToMain():
    global main_table
    return main_table

eel.init("./other/gui")
eel.start("login.html", mode="chrome", host="localhost", port=2700, block=True)