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

        table = driver.find_element(By.XPATH, "/html/body/div[5]/div/table[2]/tbody/tr/td/table[1]").get_attribute("outerHTML")
        table = BeautifulSoup(table, "html.parser")

        new_body = BeautifulSoup('', "html.parser")

        new_div = new_body.new_tag("div")
        new_div['style'] = 'height: 450px; max-height:600px; width: 900px; overflow-y: auto;'
        new_body.append(new_div)

        new_table = new_body.new_tag("table")
        new_table['style'] = "width: 100%;"
        new_div.append(new_table)
        names = """<colgroup><col style="width: 450px" span="2"><col style="width: 450px"></colgroup><tr><td colspan="2">Дисциплина</td><td>Журнал</td></tr>"""
        names = BeautifulSoup(names, "html.parser")
        new_table.append(names)

        raws = table.find_all("tr")[3:]

        for i in raws:
            tds = i.find_all("td")
            if "семестр" in tds[1].text.lower():
                i['class'] = i.get('class', []) + ['clickable']
                i['onclick'] = "toggleDetails(this)"
            else:
                i['class'] = i.get('class', []) + ['details']
                i['style'] = "display: none;"
            new_table.append(i)

        links = new_table.find_all("a")
        for i in links:
            if "журнал" in i.text.lower():
                p = new_body.new_tag('p', **{'class': 'link-like'})  # Создаем новый <p> с классом
                p.string = i.string  # Копируем текст из <a>
                p['onclick'] = f'calculate("{i['href']}",{1 if "да" in i.parent.parent.find_all("td")[12].text.lower() else 0})'
                i.replace_with(p) 

        raws = new_table.find_all("tr")[1:]

        for i in raws:
            tds = i.find_all("td")[3:]
            for j in tds:
                j.decompose()
            tds = i.find_all("td")
            if "семестр" in tds[1].text.lower():
                tds[1]['colspan'] = "3"
                tds[0].decompose()
            else:
                a = tds[1].find('a')
                if a:
                    p = new_body.new_tag('p')
                    p.string = a.string  # Копируем текст из <a>
                    a.replace_with(p)
           
    
    finally:
        driver.quit()
    main_table = new_body.prettify()
    return main_table

@eel.expose
def calculate(link, flag):
    global log, passw, main_table
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
        name = driver.find_element(By.ID, "MainBody").find_elements(By.TAG_NAME, "span")[1].get_attribute("innerHTML")
        table = driver.find_element(By.ID, "MarkJournalPivotGrid_PT").get_attribute("outerHTML")
        table = BeautifulSoup(table, "html.parser")
        table1 = table.find(id="MarkJournalPivotGrid_CVSCell_SCDTable").find_all("tr")
        points = table.find(id="MarkJournalPivotGrid_DCSCell_SCDTable").find_all("tr")

        table = BeautifulSoup('', "html.parser")

        name_tag = table.new_tag("h1")
        name_tag.string = name

        # Создаем новый div с классом для стилей
        div_block = table.new_tag("div", **{'class': 'block-container'})

        # Добавляем стиль для div
        style = """
        <style>
            .block-container {
                display: flex; /* Используем flexbox для центрирования */
                flex-direction: column; /* Элементы внутри будут располагаться вертикально */
                align-items: center; /* Центрируем элементы по горизонтали */
                margin: 0 auto; /* Центрирование контейнера */
                max-width: 600px; /* Максимальная ширина контейнера (по желанию) */
                padding: 20px; /* Отступы внутри контейнера */
                border: none;
            }
            .table-container {
                overflow-x: auto; /* Горизонтальная прокрутка */
                width: 1000px; /* Ширина контейнера для таблицы */
                margin-top: 10px; /* Отступ сверху для контейнера таблицы */
                border: none;
                border-radius: 10px;
            }
            table {
                width: 100%; /* Таблица занимает всю ширину контейнера */
                border-collapse: collapse; /* Убираем двойные границы */
                margin-top: 10px; /* Отступ сверху для таблицы */
            }
            th, td {
                text-align: center; /* Центрируем текст в ячейках */
                padding: 8px; /* Отступы внутри ячеек */
                border: 1px solid #ccc; /* Граница ячеек (по желанию) */
            }
            .back-button {
                display: block; /* Кнопка будет отображаться как блок */
                margin-top: 10px; /* Отступ сверху */
            }
        </style>
        """

        # Вставляем стиль в начало таблицы
        table.insert(0, BeautifulSoup(style, "html.parser"))

        # Оборачиваем элементы в div
        div_block.append(name_tag)  # Добавляем заголовок
        table_container = table.new_tag("div", **{'class': 'table-container'})
        div_block.append(table_container)  # Добавляем контейнер для таблицы в div_block

        # Добавляем таблицу в контейнер
        table_tag = table.new_tag("table")
        table_container.append(table_tag)  # Добавляем таблицу в контейнер

        # Добавляем div в основную таблицу
        table.append(div_block)

        # Добавляем строки таблицы в новый div
        for i in table1:
            table_tag.append(i)  # Добавляем строки в таблицу
        for i in points:
            table_tag.append(i)

        # Создаем кнопку и добавляем ее в div
        back_button = table.new_tag('button', **{'class': 'back-button', "onclick": "backToMain()"})
        back_button.string = 'Возврат'
        div_block.insert(1, back_button)  # Добавляем кнопку в div
    except:
        return main_table
    finally:
        driver.quit()
    return table.prettify()

@eel.expose
def backToMain():
    global main_table
    return main_table

eel.init("./other/gui")
eel.start("login.html", mode="chrome", host="localhost", port=2700, block=True)