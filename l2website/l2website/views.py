# -*- coding=gb18030 -*-

from django.http import HttpResponse, Http404
import datetime
from django.shortcuts import render
from django.db.models.sql.datastructures import DateTime
from django.contrib.auth.decorators import login_required
from holiday.models import Person
from django.contrib.auth.views import login

@login_required
def hello(request):
    return HttpResponse("hello world")
'''
目前的base 模板中根据了是否有权限来选择是否显示导航栏，所以有可能出现已经登陆的时候回到登陆界面的情况，此时就会很怪异的即显示登陆的输入框，又显示导航栏，
所以讲登陆界面和登陆后的界面统一一个函数里，如果已经登录过则返回导航的界面，否则再进入调用django的登录界面
'''

def login_home(request):
    if request.user.is_authenticated():
        person = Person.objects.get(name=request.user.username)
        return render(request, 'login_home.html',{'person': person})
    else:
        return login(request)

'''
以下为练习中的测试函数
'''

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
  
def display_meta(request):  
    values = request.META.items()
    #values.sort()
    html= []
    for k,v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k,v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))