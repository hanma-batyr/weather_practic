import sqlite3

'''Создание подключения к базе данных'''
conn = sqlite3.connect("Weather_program_base.db")
cursor = conn.cursor()

'''Создание таблицы users'''
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT,
    password TEXT
)''')

'''Создание таблицы search_history'''
cursor.execute('''CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    search_query TEXT NOT NULL,
    search_type TEXT NOT NULL,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
