from flask import Flask,redirect,request,make_response
from comics import *
from tracking import *
from urlshort import *
from pastebox import *

app = Flask(__name__)

## comic web page serving
@app.route('/')
def homepage():
	return comicpage(-1)

@app.route('/<int:cid>/')
def comic(cid):
	return comicpage(cid)

@app.route('/random/')
def randomcomic():
	return redirect("/%i"%(randcomic(),), code=302)

@app.route('/search/')
def csearch():
	return search(request.args.get('q',''),request.args.get('p',1))

@app.route('/about/')
def aboutpage():
	return render_template('aboutpage.html')

@app.route('/stuff/')
def stuffpage():
	return render_template('otherstuff.html')

## dynamic post-based stuff for comics
@app.route('/addcomment',methods=['POST'])
def addcomment_():
	num = request.form['num']
	name = request.form['name']
	com = request.form['comm']
	addcomment(num,name,com)
	return redirect("/{}".format(num), code=302)

## tracking image handling

@app.route('/track', methods=['GET','POST'])
def tracking_creator():
	if request.method == 'GET':
		return render_template('track_create.html')
	elif request.method == 'POST':
		thash = addtrack()
		return render_template('track_create.html',thash=thash)
@app.route('/track/', methods=['GET'])
def tracking_creator_():
	return render_template('track_create.html')

pngdata = open('static/1x1.png').read()

@app.route('/track/<uid>.png')
def tracking_handler(uid):
	trackhit(uid,request)
	response = make_response(pngdata)
	response.headers['Content-Type'] = 'image/png'
	return response

@app.route('/track/<uid>')
def tracking_data(uid):
	return gettrackdata(uid)

## pastebox handling

@app.route('/paste',methods=['GET','POST'])
def pastebox_handler():
	if request.method == 'GET':
		return render_template('pastebox_create.html')
	elif request.method == 'POST':
		data = request.form['data']
		dhash = addpaste(data)
		return redirect('/paste/{}'.format(dhash),302)
@app.route('/paste/',methods=['GET'])
def pastebox_handler_():
	return render_template('pastebox_create.html')

@app.route('/paste/<uid>')
def pastebox_viewer(uid):
	data = getpaste(uid)
	return render_template('pastebox_show.html',hash=uid,data=data)

## urlshort handling

@app.route('/url',methods=['GET','POST'])
def ushort_handler():
	if request.method == 'GET':
		return render_template('ushort_create.html')
	elif request.method == 'POST':
		old = request.form['data']
		new = addurl(old)
		return render_template('ushort_disp.html',old=old,new=new)
@app.route('/url/',methods=['GET'])
def ushort_handler_():
	return render_template('ushort_create.html')


@app.route('/url/<uid>')
def ushort_redirect(uid):
	url = geturl(uid)
	return redirect(url, code=302) 

## other handlers

@app.route('/ip')
def ip_address():
	return request.remote_addr
	# ip address

@app.errorhandler(404)
def page_not_found(error):
	return render_template('errorpage.html',id=404,url='you just entered',reason='Page not found'), 404

@app.errorhandler(500)
def page_not_found(error):
	return render_template('errorpage.html',id=500,url='you just entered',reason='Internal server error'), 500

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=5000)
