import sqlite3

database = 'students.db'

def create_connection():
    conn = sqlite3.connect(database)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_student(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def verify_student(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE username = ? AND password = ?', (username, password))
    student = cursor.fetchone()
    conn.close()
    return student is not None