import sqlite3

def initiate_db():
    connection = sqlite3.connect('products5.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER
    )
    ''')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def add_user(username, email, age): # 14_5
    connection = sqlite3.connect('users.db')  # Подключаемся к базе данных
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, 1000)'
                   , (username, email, age))
    connection.commit()
    connection.close()


def is_included(username): # 14_5
    connection = sqlite3.connect('users.db')  # Подключаемся к базе данных
    cursor = connection.cursor()
    check_name = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    try:
        if check_name.fetchone()[1] == username:
            return True
    except TypeError:
        return False
    finally:
        connection.close()


def get_all_products(db_name='products5.db'):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()

    return products

def add_product(title, description, price, db_name='products5.db'):
    connection = sqlite3.connect(db_name) # Подключаемся к базе данных
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Products (title, description, price) VALUES (?, ?, ?)
    ''', (title, description, price))  # Вставляем новую запись в таблицу Products
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initiate_db()
    add_product('Продукт 1', 'Описание продукта 1', 100)
    add_product('Продукт 2', 'Описание продукта 2', 200)
    add_product('Продукт 3', 'Описание продукта 3', 300)
    add_product('Продукт 4', 'Описание продукта 4', 400)



