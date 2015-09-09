import sqlite3,requests,time,json,random

root = '/Users/jacksonservheen/Documents/Programming/xkcd-4-wobsite/data/'

start = int(open(root + 'lastcomic.txt','r').read())
end = int(json.loads(requests.get("http://xkcd.com/info.0.json").text)['num'])

newdb=True
try:
	a = open(root + 'comics.db','r')
	a.read(1)
	a.close()
	newdb = False
	start = start - 10
	if start<0: 
		start = 1
	print "Appending to old database..."
except:
	newdb = True
	start = 1
	print "Creating new database..."

print "Getting comics {} through {}\n".format(start,end)

conn = sqlite3.connect(root + 'comics.db')
c = conn.cursor()

if newdb:
	c.execute('''CREATE TABLE comics
			 (num int, year int, month int, day int, img text, alt text, news text, link text, trans text, title text)''')

def main():
	end2 = 0
	for i in range(start,end+1):
		print "Comic {}:".format(i),
		try:
			c.execute("DELETE FROM comics WHERE num=?",(i,))
			data = requests.get("http://xkcd.com/{0}/info.0.json".format(i)).text
			data = json.loads(data)
			tup = (data['num'],data['year'],data['month'],data['day'],data['img'],data['alt'],data['news'],data['link'],data['transcript'],data['title'])
			c.execute("INSERT INTO comics VALUES (?,?,?,?,?,?,?,?,?,?)",tup)
			print "Success"
			time.sleep(1)
			end2 = i
		except KeyboardInterrupt:
			break
		except:
			print "FAILED"
	conn.commit()
	conn.close()
	f = open(root + 'lastcomic.txt','w')
	f.write(str(end2))

if __name__ == '__main__':
	main()
