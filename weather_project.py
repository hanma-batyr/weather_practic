import main

print("Зарегистрируйтесь или пройдите аутентификацию")
print("1. Зарегистрироваться")
print("2. Пройти аутентификацию")
entrance_choice = int(input())
main.entrance_handler(entrance_choice)

print("Что вы хотите выполнить?")
print("1. Поиск погоды по названию")
print("2. Поиск погоды по координатам")
user_choice = int(input())
if user_choice == 1:
    city_name = input("Введите название города: ")
    main.name_city_weather(city_name)
elif user_choice == 2:
    # Код еще в разработке 
    pass
else:
    print("Неправильный выбор. Пожалуйста, выберите 1 или 2.")