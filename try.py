from flask import Flask, render_template,request
from mongo import userdata_insert,userdata_retrive
#from run imoport run 
app = Flask(__name__)

@app.route('/')
def index(name=None):
	return render_template('index.html', name=name)

@app.route('/signup',methods = ['GET','POST'])
def signup(name=None):
	if request.method == "POST":
		name = request.form['name']
		email = request.form['email']
		pas = request.form['pass']
		con_pass = request.form['con_pass']
		userdata_insert(name,email,pas)
		return "You and sucessfully signed up"
	else:
		return render_template('signup.html', name = name)

@app.route('/login',methods = ['GET','POST'])
def login(name=None):
	if request.method == "POST":
		email = request.form['email']
		pas = request.form['pass']
		userdata_retrive(email,pas)
		return "You and sucessfully logged in"
	else:
		return render_template('login.html', name = name)

"""@app.route('/try')
def ptut(name = None):
	return render_template('try.html',name = name)
		
@app.route('/python_tut_01',methods = ['GET','POST'])
def ptut1(name = None):
	if request.method == "POST":
		code = request.form['code']
		
	else:
		return render_template('ptut1.html',name = name)
"""
	
