## Требования
- `python 3.10` и выше
- наличие Microsoft Egde(не обязательно. позже добавлю как исправить)
- прямые руки))) (опционально)

## Установка
1. Клонировать репозиторий
2. Добавить папку `./other/geckodriver` в перенную `PATH` среды
3. Скачать все библиотеки командой `pip install -r requirements.txt`
4. Запустить `main.py`

## Обход наличия Edge
Для адекватной работы на лини достаточно найти строку:  
```eel.start("login.html", mode="edge", host="localhost", port=2700, block=True)```  
и заменить ее на:  
```eel.start("login.html", mode="chrome", host="localhost", port=2700, block=True)```  
В дальнейшем добавлю автоопределение системы и адекватный запуск  
