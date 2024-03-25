import back

while True:
    print("Здравствуйте. Пройдите пожалуйста аутентификацию или регистрацию")
    print("1. Регистрация")
    print("2. Аутентификация")
    print("3. Выход")
    initial_choice = int(input("Напишите только 1, 2 или 3: "))

    if initial_choice == 1 or initial_choice == 2:
        back.entrance_handler(initial_choice)
        back.select_action_handler()
    elif initial_choice == 3:
        print("До свидания!")
        break
    else:
        print("Неправильный выбор. Пожалуйста, введите 1, 2 или 3.")
