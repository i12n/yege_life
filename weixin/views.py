# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import hashlib,time,re,datetime
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET

from yege_life import settings
from yege_life.write import write_news,write_user,register_record,write_not_news_or_not
# Create your views here.
def index(request):
	return HttpResponse("hello,i'm here")


def set_text_xml(msg):
	#print('set_text_xml')
	xml = """
		<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[%s]]></MsgType>
		<Content><![CDATA[%s]]></Content>
		</xml>"""%(msg['ToUserName'],msg['FromUserName'],msg['CreateTime'],msg['MsgType'], msg['Content'])
	#print msg['CreateTime']
	return xml

def get_msg(xml):
	print('get_msg')
	
	_msg={}
	for node in xml:
		_msg[node.tag]=node.text
	#print _msg['CreateTime']
	return _msg

def handle_subscribe(msg):
	print('handle_subscribe')
	_msg={}
	_msg['FromUserName']=msg['ToUserName']
	_msg['ToUserName']=msg['FromUserName']
	_msg['MsgType']='text'
	_msg['CreateTime']= str(int(time.time()))
	_msg['Content']='欢迎关注 yegelife,输入 cc 查询春纯毕业倒计时'
	_content=set_text_xml(_msg)
	return _content

def handle_location_or_image(msg,type):
	print('handle_location')
	msg_uid=msg['FromUserName']
	_msg={}
	_msg['FromUserName']=msg['ToUserName']
	_msg['ToUserName']=msg['FromUserName']
	_msg['MsgType']='text'
	_msg['CreateTime']= str(int(time.time()))
	_msg['Content']='发布成功'
	_content=set_text_xml(_msg)
	t=write_not_news_or_not(msg_uid,type)
	if t:
		write_news(msg_uid,msg)
	return _content

def handle_text(msg):
	print('handle_text')
	msg_content=msg['Content']
	cmd=msg_content[0:2]
	msg_uid=msg['FromUserName']
	msg['Content']=msg_content[2:]
	print(cmd)
	if cmd=='cc':
		today=datetime.date.today()
		end=datetime.date(2014,7,1)
		days=int((end-today).days)
		_msg={}
		_msg['FromUserName']=msg['ToUserName']
		_msg['ToUserName']=msg['FromUserName']
		_msg['MsgType']='text'
		_msg['CreateTime']= str(int(time.time()))
		_msg['Content']='距离春纯毕业还有'+str(days)+'天'
		if days<0:
			_msg['Content']='杨春纯已经毕业'
		_content=set_text_xml(_msg)
		return _content
	if cmd=='@@':	
		_msg={}
		_msg['FromUserName']=msg['ToUserName']
		_msg['ToUserName']=msg['FromUserName']
		_msg['MsgType']='text'
		_msg['CreateTime']= str(int(time.time()))
		_msg['Content']='发布成功'
		_content=set_text_xml(_msg)
		write_news(msg_uid,msg)
		print msg
		return _content
	if cmd=='@#':
		_msg={}
		_msg['FromUserName']=msg['ToUserName']
		_msg['ToUserName']=msg['FromUserName']
		_msg['MsgType']='text'
		_msg['CreateTime']= str(int(time.time()))
		_msg['Content']='注册失败'
		_user=msg_content[2:].split('#')
		_username=_user[0]
		_pwd=_user[1]
		t=write_user(msg_uid,_username,_pwd)
		if t==-1:
			_msg['Content']='注册失败,此微信号已经被注册'
		if t==-2:
			_msg['Content']='注册失败,此用户名已经被注册'
		if t==1:
			_msg['Content']='注册成功'
		_content=set_text_xml(_msg)
		return _content
		
	if cmd=='@+':
		t=register_record(msg_uid,'location')
		if t:
			_msg={}
			_msg['FromUserName']=msg['ToUserName']
			_msg['ToUserName']=msg['FromUserName']
			_msg['MsgType']='text'
			_msg['CreateTime']= str(int(time.time()))
			_msg['Content']='可以发布位置消息'
			_content=set_text_xml(_msg)
			return _content
	if cmd=='@*':
		t=register_record(msg_uid,'image')
		if t:
			_msg={}
			_msg['FromUserName']=msg['ToUserName']
			_msg['ToUserName']=msg['FromUserName']
			_msg['MsgType']='text'
			_msg['CreateTime']= str(int(time.time()))
			_msg['Content']='可以发布图片消息'
			_content=set_text_xml(_msg)
			return _content
			
def handle(msg):
	print('handle')
	print(msg['MsgType'])
	msg_type=msg['MsgType']
	if msg['MsgType']=='event':
		if msg['Event']=='subscribe':
			_content=handle_subscribe(msg)
			return _content
	if msg['MsgType']=='text':
		_content=handle_text(msg)
		return _content
	if msg['MsgType']=='location':
		_content=handle_location_or_image(msg,'location')
		return _content
	if msg['MsgType']=='image':
		_content=handle_location_or_image(msg,'image')
		return _content
	
#check weixin token

def check_signature(request):
	signature=request.GET.get('signature',None)
	timestamp=request.GET.get('timestamp',None)
	nonce=request.GET.get('nonce',None)
	echostr=request.GET.get('echostr',None)

	token=settings.WEIXIN_TOKEN

	tmplist=[token,timestamp,nonce]
	tmplist.sort()
	tmpstr="%s%s%s"%tuple(tmplist)
	tmpstr=hashlib.sha1(tmpstr).hexdigest()
	if tmpstr==signature:
		return echostr
	else:
		return None


@csrf_exempt
def check_signature1(request):
	print('this is test')
	if request.method == 'GET':
		response=HttpResponse(check_signature(request))
		print('get\n')
		return response
	else:
		print('post\n')
		xml = ET.fromstring(request.body)
		msg=get_msg(xml)
		content=handle(msg)
		return HttpResponse(content)
