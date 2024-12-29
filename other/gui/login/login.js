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

function toggleDetails(row) {
    let nextRow = row.nextElementSibling;
    let detailsVisible = false;

    // Перебираем все следующие строки
    while (nextRow && nextRow.classList.contains('details')) {
        // Если строка видима, скрываем её
        if (nextRow.style.display !== 'none') {
            nextRow.style.display = 'none';
            detailsVisible = true;
        } else {
            // Если строка скрыта, показываем её
            nextRow.style.display = 'table-row';
            detailsVisible = false;
        }
        nextRow = nextRow.nextElementSibling;
    }

    // Если строки были видимы, скрываем их, иначе показываем
    if (detailsVisible) {
        row.classList.remove('active');
    } else {
        row.classList.add('active');
    }
}