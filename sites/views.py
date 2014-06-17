#codeing=utf-8
from django.shortcuts import HttpResponse,render
from yege_life.write import read_news

import time
import json
from datetime import date
from datetime import datetime

def get_news(request,username):
	print('get_news')
	if request.POST:
		YYYYmm=request.POST.get("YYYYmm") or None
		if YYYYmm==None:
			today=date.today()
			YYYYmm=today.strftime("%Y%m")
		news=read_news(username,YYYYmm)
        	return HttpResponse(news,mimetype="application/json")

	today=date.today()
	YYYYmm=today.strftime("%Y%m")
	news=read_news(username,YYYYmm)
	print news
	return HttpResponse(news,mimetype="application/json")

def index(request,username):
    return render(request, 'sites/index.html',{'username':username})
