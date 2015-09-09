import sqlite3,sha

try:
	a = open('data/pastebox.db','r')
	a.read(1)
	a.close()
	## the database already exixts of this succeeds.
except:
	## create database
	conn = sqlite3.connect('data/pastebox.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE pastes
	(hash text, data text)''')
	conn.commit()
	conn.close()


def addpaste(data):
	conn = sqlite3.connect('data/pastebox.db')
	hd = sha.new(data)
	dhash = str(hd.hexdigest())
	c = conn.cursor()
	c.execute('SELECT hash FROM pastes WHERE hash=?',(unicode(dhash),))
	temp = c.fetchone()
	if temp:
		return dhash
	else:
		c.execute("INSERT INTO pastes VALUES (?,?)",(dhash,data))
		conn.commit()
	conn.close()
	return dhash

def getpaste(dhash):
	conn = sqlite3.connect('data/pastebox.db')
	c = conn.cursor()
	c.execute('SELECT data FROM pastes WHERE hash=?',((dhash),))
	temp = c.fetchone()
	if not temp:
		return "Paste not found"
	else:
		return str(temp[0])
	conn.close()