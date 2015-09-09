import requests,random,time,json,re,sqlite3
from flask import render_template

def comments(num):
	conn = sqlite3.connect('data/comments.db')
	c = conn.cursor()
	c.execute("SELECT * FROM comments WHERE num=?",(num,))
	r = c.fetchall()
	conn.close()
	return r

def addcomment(num,name,comm):
	if name != "" and comm != "":
		conn = sqlite3.connect('data/comments.db')
		c = conn.cursor()
		c.execute("INSERT INTO comments VALUES (?,?,?)",(num,name,comm))
		conn.commit()
		conn.close()

def comicpage(num):
	conn = sqlite3.connect('data/comics.db')
	c = conn.cursor()
	# sql tuple format:
	# (num int, year int, month int, day int, img text, alt text, news text, link text, trans text, title text)
	last = int(open('data/lastcomic.txt','r').read())
	if num == -1:
		num = last
	if num < 1 or num > last:
		return render_template("errorpage.html",id='404',url='/{}'.format(num),reason='The requested comic does not exist.'),404
	try:
		c.execute("SELECT * FROM comics WHERE num=?",(num,))
		cdata = c.fetchone()
		conn.close()
		if cdata is None:
			return render_template("errorpage.html",id='404',url='/{}'.format(num),reason='The requested comic does not exist'),404
		transcript = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', cdata[8].encode('utf-8','ignore').replace('\n','<br/>').replace('[[','<i>').replace(']]','</i>').replace('<<','<b>').replace('>>','</b>').replace('((','<i>').replace('))','</i>'))
		if '{{' in transcript:
			transcript = transcript.split('{{',1)[0]
		return render_template("comicpage.html",id=cdata[0],img=cdata[4],title=cdata[9],alt=cdata[5],trans=transcript,date="%s/%s/%s"%(cdata[2],cdata[3],cdata[1]),news=cdata[6],imglink=cdata[7],comments=comments(num))
	except:
		return render_template("errorpage.html",id='500',url='/{}'.format(num),reason='The server has ancountered an internal error. Please notify the owners.'),500

def chunks(seq,n):
	while seq:
		yield seq[:n]
		seq = seq[n:]

def search(term,page):
	conn = sqlite3.connect('data/comics.db')
	c = conn.cursor()
	c.execute("SELECT * FROM comics WHERE title LIKE ?",('%'+term+'%',))
	results = c.fetchall()
	c.execute("SELECT * FROM comics WHERE alt LIKE ?",('%'+term+'%',))
	results += c.fetchall()
	c.execute("SELECT * FROM comics WHERE trans LIKE ?",('%'+term+'%',))
	results += c.fetchall()
	if len(results) == 0:
		return render_template('searchpage.html',term=term,results=[],page=int(page))
	unique = []
	d = [unique.append(item) for item in results if item not in unique]
	results = list(chunks(unique,20))
	results = results[int(page)-1]
	conn.close()
	return render_template('searchpage.html',term=term,results=results,page=int(page))

def randcomic():
	last = int(open('data/lastcomic.txt','r').read())
	return random.randint(1,last)