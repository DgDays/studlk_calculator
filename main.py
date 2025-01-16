import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback

log, passw, main_table = ['']*3

#𝕊𝕖𝕣.𝔻𝕖𝕤𝕙𝕖𝕣 itk,ns yf[eq

def vesa(str):
    vesa = str.replace(',','.')
    vesa = vesa.split()  #строка с весами нужны только значения со слешами
    f_vesa = []
    #print(vesa[0])
    mark = 0
    for i in vesa:
        ves = ""
        mark = 0
        for j in i:
            #print(i,j,mark)
            if mark == 1:
                ves += j
            if j == '/':
                mark = 1
        #print(float(ves))
        f_vesa.append(float(ves))
    #print(f_vesa)
    return f_vesa

def bally(str):
    str = str.replace(',','.')
    bally = str.split() #такое же количество элементов как в весах все остальное считается
    #print(bally)
    ball = []
    for i in range(len(bally)):
        ball.append(float(bally[i]))
            #print(i,bally[i])
    #print(ball)
    return ball

def percent(vesa,bally):
    sum_v=0
    ves = 0
    sum_b=0
    blank = 0
    blank_v = 0
    vesa_blank = dict()
    output = []
    for i in range(len(vesa)):
        ves += vesa[i]
        if bally[i] == 0:
            blank += 1
            blank_v += vesa[i]
            vesa_blank[i] = vesa[i]
        sum_v += vesa[i]
        sum_b += vesa[i]*bally[i]/100
    #print(vesa_blank)
    vesa_blank = dict(sorted(vesa_blank.items(), reverse=1))
    points = 0
    points_b = 0
    for i in range(len(vesa)):
        if bally[i] != 0:
            points += 1
            points_b += bally[i]
    points_b = round(points_b / points,2)
    #print(sum_v,sum_b)
    sum_3 = sum_v*0.6
    sum_4 = sum_v*0.75
    sum_5 = sum_v*0.85

    ZACHET_MARK = round(sum_3 - sum_b, 2)
    output.append("Для зачета вам нужно " + str(ZACHET_MARK) + " баллов")
    output.append(f"Ваша средняя оценка составляет {points_b}% Если вы все еще получаете средние оценки, вам нужно завершить:")

    for i in vesa_blank.keys():
        if ZACHET_MARK > 0:
            output.append(f"Номер в таблице: {i+1:^4} Баллы: {round(vesa_blank[i]*points_b/100,2):^6}")
            ZACHET_MARK -= round(vesa_blank[i]*points_b/100,2)
    return output

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
        names = """<colgroup><col style="width: 100px"><col style="width: 600px"><col style="width: 200px"></colgroup><tr><td colspan="2">Дисциплина</td><td>Журнал</td></tr>"""
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
                p['onclick'] = f'calculate("{i["href"]}",{1 if "да" in i.parent.parent.find_all("td")[12].text.lower() else 0})'
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
    
    except:
        eel.eel_alert_login()
        return "<div id='loginDiv' class='active'><form action=''><input type='login' id='login' placeholder='Логин'><input type='password' id='password' placeholder='Пароль'><input type='button' value='Войти' onclick='get_lessons()'></form></div><script src='login/login.js'></script>"
    
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

        weights, points_a = [], []
        weight_str, points_str = ['']*2
        for raw in range(len(points)):
            for i in range(len(points[raw].find_all("td"))):
                if raw % 2:
                    if i % 2 and all(char in "1234567890," for char in points[raw].find_all("td")[i].decode_contents()):
                        points_str += f"{points[raw].find_all('td')[i].decode_contents()} "
                else:
                    if points[raw].find_all("td")[i].decode_contents() != '' and "/" in points[raw].find_all("td")[i].decode_contents():
                        weight_str += f"{points[raw].find_all('td')[i].decode_contents()} "

        weights = weight_str.split(" ")
        points_a = points_str.split(" ")
        weight_str = " ".join(weights) 
        points_str = " ".join(points_a[:len(weights)-1])

        points_a = bally(points_str)
        weights = vesa(weight_str)
        output = percent(weights, points_a)

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
                width: 90vw; /* Ширина контейнера для таблицы */
                margin-top: 10px; /* Отступ сверху для контейнера таблицы */
                border: none;
                border-radius: 30px;
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

        for line in output:
            p = table.new_tag("p", **{'class': 'p_out'})
            p.string = line
            div_block.append(p)
    except Exception as e:
        print(e)
        # Выводим трассировку стека
        traceback.print_exc()
        eel.eel_alert_table()
        return main_table
    finally:
        driver.quit()
    return table.prettify()

@eel.expose
def backToMain():
    global main_table
    return main_table

eel.init("./other/gui")
eel.start("login.html", mode="edge", host="localhost", port=2700, block=True)