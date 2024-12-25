const welcome = document.getElementById('welcome');
const login = document.getElementById('loginDiv');

        // Функция для переключения между welcome и login
function showLogin() {
    welcome.classList.remove('active'); // Убираем активный класс у welcome
    setTimeout(() => {
        login.classList.add('active'); // Добавляем активный класс к login
    }, 500); // Задержка для плавного исчезновения welcome
}

        // Показываем welcome и переключаем на login через 5 секунд
setTimeout(() => {
    welcome.classList.add('active'); // Убедимся, что welcome активен
    setTimeout(showLogin, 5000); // Через 5 секунд вызываем функцию showLogin
}, 0);