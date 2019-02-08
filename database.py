import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Housing (name TEXT,address TEXT,price INTEGER)''')
