import sqlite3
import requests
import hashlib


def registration():
    '''Получение логина и пароля для дальнейшего добавления в базу данных'''
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    '''Подключение к базе данных'''
    conn = sqlite3.connect("Weather_program_base.db")
    cursor = conn.cursor()

    '''Проверка на отсуствие такого же(одинакового) логина'''
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    existing_user = cursor.fetchone()

    '''Цикл добавления пользователя при уникальности логина'''
    '''Так же при добавление пользователя пароль будет хэширован'''
    if existing_user:
        print("Пользователь с таким логином уже существует.")
    else:
        # Хэшируем пароль пользователя с помощью hashlib
        # sha512 - Это количество символов который создасть библеотека hashlib
        # encode('utf-8') - преобразование в байтовую строку
        # hexdigest() - возвращает строку в шестнадцатеричном формате.
        hashlib_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        # Добавляем нового пользователя
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)",
                       (login, hashlib_password))
        print("Пользователь успешно зарегистрирован.")
        # сохраняем результат и закрываем базу данных
        conn.commit()
        conn.close()


def authenticate():
    '''Функция проверки и аутификацией пользователя учетом возможных ошибок'''
    try:
        '''Получаем данные для прооверки'''
        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        '''Подключение к базе данных'''
        conn = sqlite3.connect("Weather_program_base.db")
        cursor = conn.cursor()

        '''Проверка на наличего логина в базе данных'''
        cursor.execute("SELECT * FROM users WHERE login=?", (login,))
        user = cursor.fetchone()

        '''Цикл аутификацией'''
        if user:
            # Получаем хэш пароля из базы данных
            hashed_password_db = user[2]
            # Хэшируем введенный пароль для сравнения
            h_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

            # Сравниваем хэшированные символы для аутификацией
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


def entrance_handler(entrance_choice: int):
    '''Простоя функция выбора между регистрацией и аутентификацией'''
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


def name_city_weather(city_name: str):
    '''Функция получения данных о погоде по названию города'''

    '''Задаем ссылку и ключ'''
    # ссылка на наш API сайт
    url = "https://api.openweathermap.org/data/2.5/weather"
    # Наш API ключ
    api_key = "9fc2e3a3520007f0d5650f5f800de13e"

    '''Задаем словарь с  который содержит параметры запроса'''
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    '''Подключение к базе данных'''
    conn = sqlite3.connect("Weather_program_base.db")
    cursor = conn.cursor()

    '''Взаймоствие с пользователем для дальнейшей указаний'''
    print("Вы хотите продолжить в режиме инкогнито?")
    print("1. Да")
    print("2. Нет")
    choice = int(input("Введите пожалуйста 1 или 2: "))

    '''Цикл функции для получений результата с сохранением и без'''
    if choice == 1:
        '''Отправляем запрос без сохранения истории'''
        response = requests.get(url, params=params)
        # Проверяем статус запроса
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
            print("Ошибка при получении данных о погоде")
    elif choice == 2:
        '''Отправляем запрос с сохранением истории'''
        response = requests.get(url, params=params)
        # Проверяем статус запроса
        if response.status_code == 200:
            data = response.json()
            print("Погода в", city_name)
            print("Температура:", data["main"]["temp"], "°C")
            print("Ощущается как:", data["main"]["feels_like"], "°C")
            print("Минимальная температура:", data["main"]["temp_min"], "°C")
            print("Максимальная температура:", data["main"]["temp_max"], "°C")
            print("Влажность:", data["main"]["humidity"], "%")
            print("Атмосферное давление:", data["main"]["pressure"], "hPa")

            '''Опция сохранения в таблице search_history'''
            try:
                # Вставляем запись в таблицу search_history
                cursor.execute('''INSERT INTO search_history (login,
                               search_query, search_type) VALUES (?, ?, ?)''',
                               ("", city_name, "Название"))
                # Подтверждаем изменения
                conn.commit()
                print("История поиска сохранена.")
            except sqlite3.Error as e:
                # Обработка ошибки при выполнении запроса
                print("Ошибка при сохранении истории поиска:", e)
        else:
            # Отработка ошибок
            print("Ошибка при получении данных о погоде")
    else:
        # Отработка ошибок
        print("Неверный выбор. Пожалуйста, введите 1 или 2.")


def get_weather_by_coordinates(lat: float, lon: float):
    '''Функция получения данных о погоде по координатам города'''

    '''Задаем ссылку и ключ'''
    # ссылка на наш API сайт
    url = "https://api.openweathermap.org/data/2.5/weather"
    # Наш API ключ
    api_key = "9fc2e3a3520007f0d5650f5f800de13e"

    '''Задаем словарь с  который содержит параметры запроса'''
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    '''Подключение к базе данных'''
    conn = sqlite3.connect("Weather_program_base.db")
    cursor = conn.cursor()

    '''Взаймоствие с пользователем для дальнейшей указаний'''
    print("Вы хотите продолжить в режиме инкогнито?")
    print("1. Да")
    print("2. Нет")
    choice = int(input("Введите пожалуйста 1 или 2: "))

    '''Цикл функции для получений результата с сохранением и без'''
    # проверка выбора пользователя
    if choice == 1 or choice == 2:
        response = requests.get(url, params=params)
        response.raise_for_status()
        '''Получение погоды по координатам'''
        if response.status_code == 200:
            weather_data = response.json()
            print("Погода в указанных координатах:")
            print("Температура:", weather_data["main"]["temp"], "°C")
            print("Ощущается как:", weather_data["main"]["feels_like"], "°C")
            print("Влажность:", weather_data["main"]["humidity"], "%")
            print("Скорость ветра:", weather_data["wind"]["speed"], "м/с")
            try:
                coordinates = (lat, lon)
                str_coordinates = f"{coordinates}"
                cursor.execute('''INSERT INTO search_history
                            (login, search_query, search_type)
                            VALUES (?, ?, ?)''', ("", str_coordinates,
                                                  "Координаты"))
                # Подтверждаем изменения
                conn.commit()
                print("История поиска сохранена.")
            except sqlite3.Error as e:
                # Обработка ошибки при выполнении запроса
                print("Ошибка при сохранении истории поиска:", e)
        else:
            print("Не удалось получить данные о погоде.")
    else:
        print("Неверный выбор. Пожалуйста, введите 1 или 2.")


def select_action_handler():
    '''Простая функция выбора поиска по названию или координатам'''
    print("Что вы хотите выполнить?")
    print("1. Поиск погоды по названию")
    print("2. Поиск погоды по координатам")
    action_selection = int(input("Напишите только 1 или 2: "))
    if action_selection == 1:
        city_name = input("Введите название города на английском: ")
        name_city_weather(city_name)
    elif action_selection == 2:
        lat = float(input("Введите широту: "))
        lon = float(input("Введите долготу: "))
        get_weather_by_coordinates(lat, lon)
    else:
        print("Неправильный выбор. Пожалуйста, выберите 1 или 2.")
