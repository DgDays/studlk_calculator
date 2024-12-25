async function get_lessons() {
    let login = document.getElementById("login").value; // Получаем значение логина
    let password = document.getElementById("password").value; // Получаем значение пароля

    // Проверяем, что поля не пустые
    if (!login || !password) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    // Вызываем функцию Eel
    let res = await eel.get_lessons(login, password)(); // Убедитесь, что функция Eel возвращает результат
    document.body.innerHTML = res; // Обновляем содержимое страницы
}