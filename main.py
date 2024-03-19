import sqlite3
import hashlib
import requests

# Создание подключения к базе данных
# conn = sqlite3.connect("user.db")
# cursor = conn.cursor()
# #   Создание таблицы
# cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY,
#     login TEXT,
#     password TEXT
# )''')


# функция регистраций
def registration():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    # Проверяем, есть ли уже пользователь с таким логином
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Пользователь с таким логином уже существует.")
    else:
        # Хэшируем пароль пользователя с помощью hashlib
        h_p = hashlib.sha512(password.encode('utf-8')).hexdigest()
        # Добавляем нового пользователя
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, h_p))
        print("Пользователь успешно зарегистрирован.")
        conn.commit()


# функция аутификацией
def authenticate():
    try:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        # Проверяем, есть ли пользователь с таким логином
        cursor.execute("SELECT * FROM users WHERE login=?", (login,))
        user = cursor.fetchone()

        if user:
            # Получаем хэш пароля из базы данных
            hashed_password_db = user[2]
            # Хэшируем введенный пароль для сравнения
            h_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

            if h_password == hashed_password_db:
                print("Вход выполнен успешно!")
                return True  # Возвращаем True, если аутентификация успешна
            else:
                print("Неправильный пароль.")
                return False  # Возвращаем False, если пароль неправильный
        else:
            print("Пользователя с таким логином не существует.")
            return False  # Возвращаем False, если пользователь не найден

        conn.close()
    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)
        return False  # Возвращаем False в случае ошибки работы с базой данных
    except Exception as e:
        print("Произошла ошибка:", e)
        return False  # Возвращаем False в случае другой ошибки


def entrance_handler(entrance_choice):
    if entrance_choice == 1:
        registration()
    elif entrance_choice == 2:
        authenticated = False
        while not authenticated:
            authenticated = authenticate()
            if authenticated:
                print("Вход выполнен успешно!")
            else:
                print("Неправильно. Пожалуйста, попробуйте еще раз.")
    else:
        print("Неправильный выбор. Пожалуйста, выберите 1 или 2.")


def name_city_weather(city_name, api_key="9fc2e3a3520007f0d5650f5f800de13e"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Погода в", city_name)
        print("Температура:", data["main"]["temp"], "°C")
        print("Ощущается как:", data["main"]["feels_like"], "°C")
        print("Минимальная температура:", data["main"]["temp_min"], "°C")
        print("Максимальная температура:", data["main"]["temp_max"], "°C")
        print("Влажность:", data["main"]["humidity"], "%")
        print("Атмосферное давление:", data["main"]["pressure"], "hPa")
    else:
        print("Неверные данные")