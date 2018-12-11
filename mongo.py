from pymongo import MongoClient
from random import randint
import json,ast 
c = MongoClient()
db = c.elearn
db
def userdata_insert(name, email, pas):
	query = {"Name" : name, "Email" : email, "Password" : pas}
	db.user.insert(query)

def check_user(email,pas):
	if pas == None:
		query = {"Email" : email}
	else:
		query = {"Email" : email, "Password" : pas}
	result =  list(db.user.find(query))
	if not result:					#indicates that user with specified pass does not exists when signup 				
		if pas:
			query = {"Email" : email}
			result =  list(db.user.find(query))
			if not result:
				return 0		#indicates that user does not exists
			else:
				return 1		#indicates that user exists but email and pass don not match
		return None
	else:						#indicates that user exists
		return result[0]['Email']

def insert_edoc(email,lang):
	query = {"Email": email,"Courses.Course-Name":lang}
	cexists = list(db.user.find(query))
	if not cexists:
		query = {"Email": email},{"$push" : {"Courses" : {"Course-Name":lang,"Total_Tut":"13","Tut_comp":"0","tpoints":0}}}
		db.user.update({"Email": email},{"$push" : {"Courses" : {"Course-Name":lang,"Total_Tut":"13","Tut_comp":"0","tpoints":0}}})
	
def get_random_doc():
    	return list(db.mcq.find({},{"_id" : 0}).limit(15).skip(randint(0,35)))
    	
def checkmcq(id,ans):
	result = list(db.mcq.find({"id":id},{"_id":0}))
	answer = result[0]['ans']
	if(ans == answer):
		return "Yes"
	else:
		return "No"

def addmcq(ques,a,b,c,d,ans):
	counts=db.mcq.find()
	result=counts.count()
	print result
	result=result+1
	db.mcq.insert({"id":result,"question":ques,"a":a,"b":b,"c":c,"d":d,"ans":ans})
	
def update_info(email,name,pas):
	db.user.update({"Email":email},{"Name":name,"Password":pas})		
	
def del_user(email):
	db.user.remove({"Email":email})
	
def quiz_record(email,result):
	clist=list(db.user.find({"Email":email},{"_id":0}))
	temp=dict(clist[0])
	temp1=temp['Courses']
	temp2=dict(temp1[0])
	cname=temp2['Course-Name']
	len1=len(temp2)	
	a=result[0]
	if len1 ==4:
		qlen=0
		mscore=[]
		mscore.append(a)
		
	else:
		
		temp3=temp2['quiz']
		qlen=len(temp3)
		temp4=dict(temp3[qlen-1])
		mscore=temp4['score']
		mscore.append(a)
	qlen=qlen+1
	db.user.update({"Email":email,"Courses.Course-Name":cname},{"$push":{"Courses.$.quiz":{"quiz_no":qlen,"points":result[0],"attempted":result[1],"nonattempted":result[2],"rightans":result[3],"wrongans":result[4],"score":mscore}}})
	
def last_test(email):
	clist=list(db.user.find({"Email":email},{"_id":0}))
	temp=dict(clist[0])
	temp1=temp['Courses']
	temp2=dict(temp1[0])
	cname=temp2['Course-Name']
	len1=len(temp2)	
	if len1 ==4:
		qlen=0
		print " sorry...You have not attempted any test yet."
	else:
		temp3=temp2['quiz']
		qlen=len(temp3)
		if qlen ==1:
			print "you have attempted %s test."%qlen
		else:
			print "you have attempted %s tests."%qlen
			
		a=qlen-1	
		temp4=dict(temp3[a])
		return ast.literal_eval(json.dumps(temp4))
		
		
		
		
def max_score(email):
	clist=list(db.user.find({"Email":email},{"_id":0}))
	temp=dict(clist[0])
	temp1=temp['Courses']
	temp2=dict(temp1[0])
	cname=temp2['Course-Name']
	len1=len(temp2)	
	if len1 ==4:
		return 100
		
	else:
		temp3=temp2['quiz']
		qlen=len(temp3)
		temp4=dict(temp3[qlen-1])
		mscore=temp4['score']
		ms=max(mscore)
		return ms

def tutorials(email):
	clist=list(db.user.find({"Email":email},{"_id":0}))
	temp=dict(clist[0])
	temp1=temp['Courses']
	temp2=dict(temp1[0])
	cname=temp2['Course-Name']
	tutpoints=temp2['tpoints']
	tutcomplete=temp2['Tut_comp']
	TotTut=temp2['Total_Tut']
	print TotTut
	print tutcomplete
	print tutpoints
	
	complete_pr=float(5.0/float(TotTut))
	per=complete_pr*100
	print per
	#print per
	

