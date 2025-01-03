async function get_lessons() {
    let login = document.getElementById("login").value; // Получаем значение логина
    let password = document.getElementById("password").value; // Получаем значение пароля

    // Проверяем, что поля не пустые
    if (!login || !password) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }
    document.body.innerHTML = "<div class='active' id='welcome'><h1>Ожидайте</h1>\n<h2>Идет загрузка учебного плана</h2></div>";
    // Вызываем функцию Eel
    let res = await eel.get_lessons(login, password)(); // Убедитесь, что функция Eel возвращает результат
    document.body.innerHTML = res; // Обновляем содержимое страницы
}

async function calculate(link, flag){
    document.body.innerHTML = "<div class='active' id='welcome'><h1>Ожидайте</h1>\n<h2>Идет рассчет баллов</h2></div>";
    let res = await eel.calculate(link, flag)();
    document.body.innerHTML = res;
}

async function backToMain() {
    let res = await eel.backToMain()();
    document.body.innerHTML = res;
}