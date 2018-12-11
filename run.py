import os
from subprocess import Popen,PIPE

def make_user_dir(name):
	os.system("mkdir ./user_codes/" + str(name))

def make_lang_dir(name,lang):
	os.system("mkdir ./user_codes/" + str(name)+"/"+str(lang))

def insert_code(name,lang,code):
	f = open("./user_codes/" + str(name)+"/"+str(lang)+"/code.py","w")
	f.write(code)

def run_code(name,lang):
	p = Popen("python ./user_codes/" + str(name)+"/"+str(lang)+"/code.py",stdin = PIPE,stdout = PIPE,stderr = PIPE, shell = True)
	return p.stdout.readline()

