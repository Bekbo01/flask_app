import sqlite3

connection = sqlite3.connect('todolist.db', check_same_thread=False)
cursor=connection.cursor()

cursor.execute(
    """CREATE TABLE admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_name VARCHAR(32) UNIQUE,
        password VARCHAR(64),
        reg_date VARCHAR(32)
    );"""
)
connection.commit()
cursor.close()
connection.close()