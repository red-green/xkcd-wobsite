

import sqlite3

conn = sqlite3.connect('comics.db')
c = conn.cursor()

c.execute("SELECT * FROM comics WHERE num=400000")
print c.fetchone()
conn.close()
