python manage.py shell



'''
进行批量往数据库添加对象的脚本
'''
from django.contrib.auth.models import User, Group
from holiday.models import Person

group = Group.objects.get(name='mortal')
group2 = Group.objects.get(name='hero')
group3 = Group.objects.get(name='titan')


names = [{'ename': 'yuanzejia', 'cname': '院泽嘉', 'holidayNum': 0, 'holidayNumSum': 0, 'holidayNumUsed': 0,'gourp':1},
				 {'ename': 'lixiaoyan', 'cname': '李晓燕', 'holidayNum': 0, 'holidayNumSum': 0, 'holidayNumUsed': 0,'gourp':2}]

for name in names:
	user = User.objects.create_user(username=name['ename'],email=name['ename']+'@datangmobile.cn',password='new.1234')	
	
	if name['gourp'] == 2:
		user.groups.add(group2)
	elif name['gourp'] == 3:
		user.groups.add(group3)
	else:
		user.groups.add(group)
	person = Person.objects.create(name=name['ename'],email=name['ename']+'@datangmobile.cn',chinese_name=name['cname'], holidayNum=name['holidayNum'], holidayNumSum=name['holidayNumSum'], holidayNumUsed=name['holidayNumUsed'])
	person.save()
	user.save()