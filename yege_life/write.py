import time
import json
from datetime import date
from datetime import datetime
import os.path
import thread
import threading
import time
USER_WANT_TO_DO_RECORD={}
THREAD_RUN=False
RECORD_MUTEX = threading.Lock()

def register_record(uid,cmd_type,sec=100):
	global USER_WANT_TO_DO_RECORD
	global THREAD_RUN
	global RECORD_MUTEX
	username,ustate=get_username_by_uid(uid)
	if username == None:
		return False
	if RECORD_MUTEX.acquire():
		record=[cmd_type,sec]
		USER_WANT_TO_DO_RECORD[username]=record
		if not THREAD_RUN:
			THREAD_RUN=True
			thread.start_new_thread(thread_func,())
		RECORD_MUTEX.release()
	return True
        
def manage_record():
	global USER_WANT_TO_DO_RECORD
	global THREAD_RUN
	global RECORD_MUTEX
	for username in USER_WANT_TO_DO_RECORD.keys():
		if  USER_WANT_TO_DO_RECORD[username][1]<0:
			del USER_WANT_TO_DO_RECORD[username]
		else:
 			 USER_WANT_TO_DO_RECORD[username][1]-=1
        

def thread_func():
	global USER_WANT_TO_DO_RECORD
	global THREAD_RUN
	global RECORD_MUTEX
	while True:
		#print(USER_WANT_TO_DO_RECORD)
		time.sleep(5)
		if RECORD_MUTEX.acquire():
			if USER_WANT_TO_DO_RECORD:
				manage_record()
				RECORD_MUTEX.release()
			else:
				THREAD_RUN=False
				RECORD_MUTEX.release()
				break
 

#FILE_PATH='/home/git/yege_life.git/files/'
FILE_PATH='h:/life/yege_life/files/'
def write_months(username,YYYYmm):
	try:
		file_path=FILE_PATH+username+'/'
		file_name=YYYYmm[:-2]
		file_path+=file_name
		with open (file_path,"a+") as months_file:
			months=months_file.read()[:-1].split(',')
			month=YYYYmm[4:]
			for _month in months:
				if _month==month:
					return True
			content=month+','
			months_file.write(content)
			months_file.close()
			return True
	except IOError:
		return False

def read_months(username,YYYY):
	try:
		file_path=FILE_PATH+username+'/'
		file_name=YYYY
		file_path+=file_name
		with open (file_path,"r") as months_file:
			months=months_file.read()
			months_json='{"success":true,"months":['+months[:-1]+']}'
			months_file.close()
			return months_json
	except IOError:
		months_json='{"success":false}'
		return months_json

def convert_to_json(news_dict):
	create_time_stamp=int(news_dict["CreateTime"])+8*60*60
	create_time_str=(datetime.fromtimestamp(create_time_stamp)).strftime("%Y-%m-%d %H:%M:%S")
	create_date_str=(datetime.fromtimestamp(create_time_stamp)).strftime("%Y%m%d")
	news_dict["CreateTime"]=create_time_str
	news_json = json.dumps(news_dict)+','
	return create_date_str,news_json

def write_news(uid,news_dict):
	username,ustate=get_username_by_uid(uid)
	create_date_str,news_json=convert_to_json(news_dict)
	news_file_name=create_date_str[:6]
	if not write_months(username,news_file_name):
		return False
	try:
		file_path=FILE_PATH+username+'/'+news_file_name
		with open(file_path, "a") as news_file:
			news_file.write(news_json)
			news_file.close()
			return True
	except IOError:
		return False
	
def write_or_not(uid,ctype):
	#print ("write_not_or_not")
	global USER_WANT_TO_DO_RECORD
	global THREAD_RUN
	global RECORD_MUTEX
	hit=False
	username,ustate=get_username_by_uid(uid)
	#print(username)
	if username==None:
		return False
	if RECORD_MUTEX.acquire():
		if THREAD_RUN:
			#print("thread_run")
            #if username in USER_WANT_TO_DO_RECORD.keys():
			record= USER_WANT_TO_DO_RECORD[username]
			if record:
				if ctype==record[0]:
					print(hit)
					hit=True
					USER_WANT_TO_DO_RECORD[username][1]=100
		RECORD_MUTEX.release()
	#if hit:
		####################do write
		#print ("write")
	return hit



def read_news(username,news_file_name):
	try:
		file_path=FILE_PATH+username+'/'+news_file_name
		with open(file_path, "r") as news_file:
			news=news_file.read()
			news_file.close()
			news_json='{"success":true,"news":['+news[:-1]+']}'
			return news_json
	except  IOError:
		news_json='{"success":false}'
		return news_json


def write_user(uid,username,pwd,ustate='1'):
	if uid=='' or username=='':
		return  -8
	try:
		with open(FILE_PATH+'users',"a+") as users_file:
			for line in users_file:
				user=line.split('\t')
				if uid==user[0]:
					users_file.close()
					return -1
				if username==user[1]:
					users_file.close()
					return -2
			user_str=uid+'\t'+username+'\t'+pwd+'\t'+ustate+'\n'
			users_file.write(user_str)
			users_file.close()
			newpath=FILE_PATH+username+'/'
			if not os.path.exists(newpath): 
				os.makedirs(newpath)
			return 1
	except IOError:
		return -9

def get_username_by_uid(uid):
	try:
		with open(FILE_PATH+"users","r+") as users_file:
			for line in users_file:
				print (line)
				user=line.split('\t')
				if uid==user[0]:
					users_file.close()
					return (user[1],user[3][:-1])
			users_file.close()
			return (None,None)
	except IOError:
		return (None,None)

def change_uid_by_username(uid,username,pwd):
	try:
		with open(FILE_PATH+"users","r+") as users_file:
			lines=''
			username_exit=False
			for line in users_file:
				user=line.split('\t')
				if uid==user[0] :
					users_file.close()
					users_file.close()
					return -1
				if username==user[1] :
					if pwd!=user[2] :
						users_file.close()
						return -2
					line=uid+'\t'+user[1]+'\t'+user[2]+'\t'+user[3]
					username_exit=True
				lines+=line
			if username_exit:
				users_file.seek(0)
				users_file.write(lines)
				users_file.truncate()
				users_file.close()
				return 1
			return -3
	except IOError:
		return -9

