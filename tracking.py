import sqlite3,sha,time
from flask import render_template

try:
	a = open('data/trackbox.db','r')
	t=a.read(1)
	a.close()
	## the database already exists if this succeeds.
except:
	## create database
	conn = sqlite3.connect('data/trackbox.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE tracks
	(hash text, hits int)''')
	conn.commit()
	conn.close()


def addtrack():
	conn = sqlite3.connect('data/trackbox.db')
	hd = sha.new(str(time.time()))
	dhash = str(hd.hexdigest())
	c = conn.cursor()
	c.execute('SELECT * FROM tracks WHERE hash=?',(unicode(dhash),))
	if len(c.fetchall()) < 1:
		c.execute("INSERT INTO tracks VALUES (?,?)",(dhash,0))
		conn.commit()
	conn.close()
	return dhash

def trackhit(thash,request):
	conn = sqlite3.connect('data/trackbox.db')
	now = str(time.time())
	ip = request.remote_addr
	c = conn.cursor()
	c.execute("SELECT * FROM tracks WHERE hash=?",(thash,))
	_,hits = c.fetchone()
	c.execute("DELETE FROM tracks WHERE hash=?",(thash,))
	c.execute("INSERT INTO tracks VALUES (?,?)",(thash,hits+1))
	#print "hit!"
	conn.commit()
	conn.close()

def gettrackdata(thash):
	conn = sqlite3.connect('data/trackbox.db')
	c = conn.cursor()
	c.execute('SELECT * FROM tracks WHERE hash=?',(thash,))
	temp = c.fetchone()
	if not temp:
		return "tracker not found"
	else:
		hits=temp[1]
		return render_template('track_disp.html',tid=thash,hits=hits)
	conn.close()