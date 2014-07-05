# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import hashlib,time,re,datetime
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET

from yege_life import settings
from yege_life.write import write_news,write_user,register_record,write_or_not
# Create your views here.
def index(request):
	return HttpResponse("hello,i'm here")

#将dict格式转换为xml格式 dict_to_xml
def dict_to_xml(msg):
	xml = """
		<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[%s]]></MsgType>
		<Content><![CDATA[%s]]></Content>
		</xml>"""%(msg['ToUserName'],msg['FromUserName'],msg['CreateTime'],msg['MsgType'], msg['Content'])
	return xml
	
#将xml格式转换为dict格式 xml_to_dict
def xml_to_dict(xml):
	_msg={}
	for node in xml:
		_msg[node.tag]=node.text
	return _msg

#生成回复文本消息
def reply_text_to_user(msg,content):
	_msg={}
	_msg['FromUserName']=msg['ToUserName']
	_msg['ToUserName']=msg['FromUserName']
	_msg['MsgType']='text'
	_msg['CreateTime']= str(int(time.time()))
	_msg['Content']=content
	return dict_to_xml(_msg)
	
#处理消息推送的订阅事件
def handle_subscribe(msg):
	content='欢迎关注 yegelife'
	reply_msg=reply_text_to_user(msg,content)
	return reply_msg

#处理图片消息或地理位置消息
def handle_location_or_image(msg,type):
	msg_uid=msg['FromUserName']
	t=write_or_not(msg_uid,type)
	if t:
		write_news(msg_uid,msg)
		content='发布成功'
		reply_msg=reply_text_to_user(msg,content)
		return reply_msg
		
#处理文本消息
def handle_text(msg):
	msg_content=msg['Content']
	cmd=msg_content[0:2]
	msg_uid=msg['FromUserName']
	msg['Content']=msg_content[2:]
	if cmd=='##':
		content='测试成功'
		reply_msg=reply_text_to_user(msg,content)
		return reply_msg
	if cmd=='@@':	
		content='发布成功'
		reply_msg=reply_text_to_user(msg,content)
		write_news(msg_uid,msg)
		return reply_msg
	if cmd=='@#':
		content='注册失败'
		_user=msg_content[2:].split('#')
		_username=_user[0]
		_pwd=_user[1]
		t=write_user(msg_uid,_username,_pwd)
		if t==-1:
			content='注册失败,此微信号已经被注册'
		if t==-2:
			content='注册失败,此用户名已经被注册'
		if t==1:
			content='注册成功'
		reply_msg=reply_text_to_user(msg,content)
		return reply_msg
		
	if cmd=='@+':
		t=register_record(msg_uid,'location')
		if t:
			content='可以发布位置消息'
			reply_msg=reply_text_to_user(msg,content)
			return reply_msg
	if cmd=='@*':
		t=register_record(msg_uid,'image')
		if t:
			content='可以发布图片消息'
			reply_msg=reply_text_to_user(msg,content)
			return reply_msg
			
#接收来自微信的消息			
def handle(msg):
	msg_type=msg['MsgType']
	#事件消息
	if msg_type=='event':
		if msg['Event']=='subscribe':
			_content=handle_subscribe(msg)
			return _content
	#文本消息
	if msg_type=='text':
		_content=handle_text(msg)
		return _content
	#地理位置消息
	if msg_type=='location':
		_content=handle_location_or_image(msg,'location')
		return _content
	#图片消息
	if msg_type=='image':
		_content=handle_location_or_image(msg,'image')
		return _content
	
#检测微信的 token

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
	if request.method == 'GET':
		response=HttpResponse(check_signature(request))
		return response
	else:
		xml = ET.fromstring(request.body)
		msg=xml_to_dict(xml)
		content=handle(msg)
		return HttpResponse(content)
