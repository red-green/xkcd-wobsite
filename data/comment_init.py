import sqlite3

conn = sqlite3.connect('comments.db')
c = conn.cursor()

c.execute("""CREATE TABLE comments
			(num int, uname text, comment text)""")

conn.commit()
conn.close()