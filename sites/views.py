#codeing=utf-8
from django.shortcuts import HttpResponse,render
from yege_life.write import read_news

import time
import json
from datetime import date
from datetime import datetime

def get_news(request,username,yyyyMM=None):
	print(yyyyMM)
	if request.POST:
		YYYYmm=yyyyMM or request.POST.get("YYYYmm") or None
		if YYYYmm==None:
			today=date.today()
			YYYYmm=today.strftime("%Y%m")
			print(yyyyMM)
			news=read_news(username,YYYYmm)
			print news
			return HttpResponse(news,content_type ="application/json")

	today=date.today()
	YYYYmm=yyyyMM or today.strftime("%Y%m")
	news=read_news(username,YYYYmm)
	#print news
	return HttpResponse(news,content_type ="application/json")

def index(request,username):
    return render(request, 'sites/index.html',{'username':username})
