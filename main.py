from flask import Flask, render_template,request
from mongo import *
from run import *
import json,ast
app = Flask(__name__)

Username = ""
Useremail = ""
quesids = ["" for i in range(15)]
q = ["" for i in range(15)]

#Renders the front page
@app.route('/')
def index(name=None):
	return render_template('index.htm', name=name)

#User Signup
@app.route('/signup',methods = ['GET','POST'])
def signup(name=None):
	if request.method == "POST":
		name = request.form['name']
		email = request.form['email']
		pas = request.form['pass']
		con_pass = request.form['con_pass']
		uexists = check_user(email,None)
		if uexists == None:		#check if user exists
			userdata_insert(name,email,pas)		
			return "You have sucessfully signed up"
		else:	
			return "User already exists"
	else:
		return render_template('index.htm', name = name)

#User Login
@app.route('/login',methods = ['GET','POST'])
def login(name=None):
	if request.method == "POST":
		email = request.form['email']
		pas = request.form['pass']
		em = check_user(email,pas)
		if em == 0:
			return "You have not registered yet. Please register to login"
		elif em == 1:
			return "Your email and password does not match"
		else:
			global Username
			global Useremail
			Useremail = em
			Username = em.split("@")[0]
			make_user_dir(Username)
			return render_template('afterlogin.htm', name = Username)
	else:
		return render_template('index.htm', name = name)
		
#User Logout
@app.route('/logout')
def logout(name = None):
	global Username
	global Useremail
	Username = ""
	Useremail = ""
	return render_template('index.htm',name = name)

#Python Language Selected 
@app.route('/python',methods = ['GET','POST'])
def lang_py(name=None):
	make_lang_dir(Username,"python")		
	insert_edoc(Useremail,"python")
	return render_template('pythoncontent.htm',name = name)
	
#Start Python Tutorial
@app.route('/pythonsyntax',methods = ['GET','POST'])
def py_tut(name = None):
	return render_template('pythonsyntax.htm',name = name)
	
@app.route('/p1',methods = ['GET','POST'])
def p1(name = None):
	return render_template('p1.htm',name = name)	

@app.route('/python/code',methods = ['GET','POST'])
def abcd(name = None):
	code = request.form['styled-textarea']
	insert_code(Username,"python",code)		#validation needed here
	a = run_code(Username,"python")
	return a
	
#Quiz attempt
@app.route('/python/quiz')
def mcqtest(name=None):
	result = get_random_doc()
	global quesids
	for i in range(15):
		quesids[i] = result[i][u'id']
	return render_template("quiz.html",name = result)

@app.route('/python/mcq/getscore', methods = ['GET','POST'])
def getscore(name = None):
	global quesids
	global useremail
	points = 0
	rightans=0
	wrongans=0
	attempted=0
	nonattempted=0
	j=[]
	k=[]
	for i in range(15):
		abc = 'q'+str(i+1)
		q[i] = request.form[abc]
		ans = checkmcq(int(quesids[i]),q[i])
		if q[i]  == "z":
			nonattempted=nonattempted+1
		else:
			attempted=attempted+1
			if ans == "Yes":
				points = points + 5
				rightans=rightans+1
				m=i+1
			
				j.append(m)
			else:
				m=i+1
				wrongans=wrongans+1
				k.append(m)
	result=[points,attempted,nonattempted,rightans,wrongans,j,k] 	
	quiz_record(Useremail,result)		
	return render_template("quizt.html",name = result)


@app.route('/addmcq', methods = ['GET','POST'])
def add(name = None):
		'''ques = request.form[ques]
		a = request.form[a]
		b = request.form[b]
		c = request.form[c]
 		d = request.form[d]
		ans = request.form[ans]
		'''
		ques="abcdefg"
		a="1"
		b="error"
		c= "abc"
		d="none"	
		ans="a"
		addmcq(ques,a,b,c,d,ans)
		return render_template("zzz.htm",name=None)

@app.route('/update_info', methods = ['GET','POST'])
def changeinfo(name = None):
		'''
		name = request.form[name]
		email = request.form[email]
		pas = request.form[pas]
		'''
		name1="abcdefg"
		pas="zzz"
		email="shivam@gmail.com"	
		update_info(email,name1,pas)
		return render_template("zzz.htm",name=None)
		
@app.route('/del_user', methods = ['GET','POST'])
def deluser(name = None):
		'''
		email = request.form[email]
		'''
	
		email="sakshimuttha04@gmail.com"	
		del_user(email)
		return render_template("zzz.htm",name=None)
		
@app.route('/l', methods = ['GET','POST'])
def lastrec(name = None):
		global useremail	
		result=last_test(Useremail)
		points=result['points']
		attempted=result['attempted']
		nonattempted=result['nonattempted']
		quiz_no=result['quiz_no']
		rightans=result['rightans']
		wrongans=result['wrongans']
		record=[quiz_no,points,attempted,nonattempted,rightans,wrongans] 
		print record	
		return render_template("zzz.htm",name=record)
		
		
@app.route('/k', methods = ['GET','POST'])
def max_sc(name = None):
		global useremail	
		result=max_score(Useremail)
		if result==100:
			return "You have not attempted any Quiz."	
		else:
			return "Best score is : %s "%result
		
@app.route('/pr', methods = ['GET','POST'])
def per(name = None):
		global useremail	
		tutorials(Useremail)
		return "pr"
		
		
