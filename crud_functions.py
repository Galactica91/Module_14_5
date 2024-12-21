import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
)
''')
    connection.commit()

def get_all_products():
  cursor.execute('SELECT * FROM Products')
  return cursor.fetchall()

def insert_products():
  connection = sqlite3.connect('products.db')
  cursor = connection.cursor()

  products = [
    ('Продукт 1', 'Описание 1', 100),
    ('Продукт 2', 'Описание 2', 200),
    ('Продукт 3', 'Описание 3', 300),
    ('Продукт 4', 'Описание 4', 400)
  ]

  cursor.execute('INSERT OR IGNORE INTO Products(title, description, price) VALUES(?, ?, ?)', products)

  connection.commit()
  connection.close()

def add_user(username, email, age, balance=1000):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',(username, email, age, balance))
    connection.commit()
    connection.close()

def is_included(username):
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone() is None:
        return True
    return False


#initiate_db()
#connection.commit()
#connection.close()
