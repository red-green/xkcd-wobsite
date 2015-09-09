import sqlite3,sha,time

try:
	a = open('data/ushort.db','r')
	a.read(1)
	a.close()
	## the database already exists of this succeeds.
except:
	## create database
	conn = sqlite3.connect('data/ushort.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE urls
	(id text, url text)''')
	conn.commit()
	conn.close()



def addurl(url):
	conn = sqlite3.connect('data/ushort.db')
	hd = sha.new(url)
	dhash = str(hd.hexdigest())[0:16]
	c = conn.cursor()
	c.execute('SELECT id FROM urls WHERE id=?',(dhash,))
	temp = c.fetchone()
	print temp
	if temp:
		return dhash
	else:
		c.execute("INSERT INTO urls VALUES (?,?)",(dhash,url))
		conn.commit()
	conn.close()
	return dhash

def geturl(uid):
	conn = sqlite3.connect('data/ushort.db')
	c = conn.cursor()
	c.execute('SELECT url FROM urls WHERE id=?',(uid,))
	temp = c.fetchone()
	print temp
	if not temp:
		return "/url"
	else:
		return str(temp[0])
	conn.close()