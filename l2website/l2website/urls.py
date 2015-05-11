# -*- coding=gb18030 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change
from l2website.views import hello, login_home
from holiday.views import * 
from holiday.export import *


from django.contrib import admin
admin.autodiscover()


#配置处理各种链接的函数，用正则表达式进行匹配，大部分是准确匹配，个别连接只匹配最后的单词
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'l2website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', login_home),
    #结尾为home的链接都调用此函数处理
    (r'home/$', login_home),
    (r'^accounts/login/home/$', login_home),
    (r'^accounts/login/$', login_home),      
    #设置修改密码的界面，并配置修改成功后的重定向界面
    (r'^accounts/changpass/$', password_change, {'post_change_redirect': '/accounts/login/home/'}),
    (r'^accounts/logout/$', logout, {'next_page': '/accounts/login'}),
    (r'^apply_reward/$', apply_reward),
    (r'^approve_reward/$', approve_reward),
    (r'^apply_application/$', apply_application),
    (r'^show_my_info/$', show_my_info),
    (r'^approve_application/$', approve_application),
    (r'^show_my_apply_reward/$', show_my_apply_reward),
    (r'^search_form/$', search_form),
    (r'^search/$', search),
    (r'^apply_rollback/$', apply_rollback),
    (r'^approve_rollback/$', approve_rollback),
    (r'^no_permission/$', no_permission),
    (r'^save_xls_my_info/$', save_xls_my_info),
    (r'^save_xls_search/$', save_xls_search),
    (r'^send_email/$', send_html_mail),
    #url( r'^static/(?P<path>.*)$', 'django.views.static.serve',
)
