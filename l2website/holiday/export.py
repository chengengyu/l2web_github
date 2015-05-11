from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from holiday.models import Application, Reward, Person, ApplicationRollback
from holiday.forms import RewardForm, PersonForm, ApplicationForm
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.forms.widgets import TextInput, NumberInput, DateInput
import datetime, time
from django.contrib.auth.decorators import permission_required
import xlwt
from holiday.views import * 



styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
          'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
          'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
          'header': xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00'),
          'default': xlwt.Style.default_style}

@login_required
def save_xls_person_info(request, username):
    person = Person.objects.get(name=username)
    applications = Application.objects.filter(apply_application=person)
    rewards = Reward.objects.filter(reward_reward=person)
    rollbacks = ApplicationRollback.objects.filter(apply_rollback=person)
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'个人信息')
    
    row = 0
    sheet.write(row,0, '个人信息', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '姓名')
    sheet.write(row,1, '现有倒休')
    sheet.write(row,2, '倒休之和')
    sheet.write(row,3, '已用倒休')
    row = row + 1
    sheet.write(row,0, person.chinese_name)
    sheet.write(row,1, person.holidayNum)
    sheet.write(row,2, person.holidayNumSum)
    sheet.write(row,3, person.holidayNumUsed)
    row = row + 1
    
    row = row + 1
    sheet.write(row,0, '倒休使用记录', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '申请原因')
    sheet.write(row,1, '申请天数')
    sheet.write(row,2, '批准天数')
    sheet.write(row,3, '申请日期')
    sheet.write_merge(row,row,4,5,'起始日期')
    sheet.write_merge(row,row,6,7,'结束日期')
    sheet.write(row,8, '审批结果')
    sheet.write(row,9, '审批日期')
    row = row + 1
    for application in applications:
        sheet.write(row,0, application.reason)
        sheet.write(row,1, application.days_apply)
        sheet.write(row,2, application.days_approve)
        sheet.write(row,3, application.date_apply, style=styles['date'])
        sheet.write(row,4, application.date_start, style=styles['date'])
        sheet.write(row,5, application.start_meridiem)
        sheet.write(row,6, application.date_end, style=styles['date'])
        sheet.write(row,7, application.end_meridiem)
        sheet.write(row,8, application.approve_flag)
        sheet.write(row,9, application.date_approve, style=styles['date'])
        row=row + 1
    
    row = row + 1
    sheet.write(row,0, '倒休奖励记录', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '奖励类别')
    sheet.write(row,1, '奖励原因')
    sheet.write(row,2, '申请天数')
    sheet.write(row,3, '批准天数')
    sheet.write(row,4, '申请日期')
    sheet.write(row,5, '申请人')
    sheet.write(row,6, '批准人')
    sheet.write(row,7, '审批结果') 
    sheet.write(row,8, '审批日期')    
    row = row + 1
    for reward in rewards:
        sheet.write(row,0, reward.type)
        sheet.write(row,1, reward.reason)
        sheet.write(row,2, reward.days_apply)
        sheet.write(row,3, reward.days_approve)
        sheet.write(row,4, reward.date_apply, style=styles['date'])
        sheet.write(row,5, reward.apply_reward.chinese_name)
        sheet.write(row,6, reward.approve_reward.chinese_name)
        sheet.write(row,7, reward.approve_flag)
        sheet.write(row,8, reward.date_approve, style=styles['date'])
        row=row + 1    
    
    row = row + 1
    sheet.write(row,0, '倒休使用取消记录', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '取消原因')
    sheet.write(row,1, '申请天数')
    sheet.write(row,2, '批准天数')
    sheet.write(row,3, '申请日期')
    sheet.write(row,4, '申请人')
    sheet.write(row,5, '批准人')
    sheet.write(row,6, '审批结果')
    sheet.write(row,7, '审批日期')    
    row = row + 1
    for rollback in rollbacks:
        sheet.write(row,0, rollback.reason)
        sheet.write(row,1, rollback.days_apply)
        sheet.write(row,2, rollback.days_approve)
        sheet.write(row,3, rollback.date_apply, style=styles['date'])
        sheet.write(row,4, rollback.apply_rollback.chinese_name)
        sheet.write(row,5, rollback.approve_rollback.chinese_name)
        sheet.write(row,6, rollback.approve_flag)
        sheet.write(row,7, rollback.date_approve, style=styles['date'])
        row=row + 1   
    
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename=personInfo.xls'  
    wb.save(response)  
    return response  

@login_required
def save_xls_rewards(request, rewards):
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'倒休申请记录')
    
    row = 0
    sheet.write(row,0, '倒休申请记录', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '奖励原因')
    sheet.write(row,1, '申请天数')
    sheet.write(row,2, '批准天数')
    sheet.write(row,3, '申请日期')
    sheet.write(row,4, '申请人')
    sheet.write(row,5, '批准人')
    sheet.write(row,6, '奖励人')
    sheet.write(row,7, '审批结果')
    sheet.write(row,8, '审批日期')    
    row = row + 1
    for reward in rewards:
        sheet.write(row,0, reward.reason)
        sheet.write(row,1, reward.days_apply)
        sheet.write(row,2, reward.days_approve)
        sheet.write(row,3, reward.date_apply, style=styles['date'])
        sheet.write(row,4, reward.apply_reward.chinese_name)
        sheet.write(row,5, reward.approve_reward.chinese_name)
        sheet.write(row,6, reward.reward_reward.chinese_name)
        sheet.write(row,7, reward.approve_flag)
        sheet.write(row,8, reward.date_approve, style=styles['date'])
        row=row + 1    
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename=rewards_apply.xls'  
    wb.save(response)  
    return response  

@login_required
def save_xls_applications(request, applications):
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'倒休使用记录')
    
    row = 0
    sheet.write(row,0, '倒休使用记录', style=styles['header'])
    row = row + 1
    sheet.write(row,0, '申请原因')
    sheet.write(row,1, '申请天数')
    sheet.write(row,2, '批准天数')
    sheet.write(row,3, '申请日期')
    sheet.write_merge(row,row,4,5,'起始日期')
    sheet.write_merge(row,row,6,7,'结束日期')
    sheet.write(row,8, '审批结果')   
    sheet.write(row,9, '审批日期')    
    row = row + 1
    for application in applications:
        sheet.write(row,0, application.reason)
        sheet.write(row,1, application.days_apply)
        sheet.write(row,2, application.days_approve)
        sheet.write(row,3, application.date_apply, style=styles['date'])
        sheet.write(row,4, application.date_start, style=styles['date'])
        sheet.write(row,5, application.start_meridiem)
        sheet.write(row,6, application.date_end, style=styles['date'])
        sheet.write(row,7, application.end_meridiem)
        sheet.write(row,8, application.approve_flag)
        sheet.write(row,9, application.date_approve, style=styles['date'])
        row=row + 1
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename=personInfo.xls'  
    wb.save(response)  
    return response  


@login_required
@csrf_protect
def save_xls_my_info(request):
    if 'search_name' in request.POST:
        search_name = request.POST['search_name']
    if not search_name:
        return (save_xls_person_info(request, request.user.username))
    else:
        if request.user.has_perm('holiday.approve'):
            return (save_xls_person_info(request, search_name))
        else:
            return no_permission(request)

def save_xls_search(request):
    if request.method == "POST":
        search_type = request.POST['search_type']
        search_string = request.POST['search_text']
        if search_type == 'apply_name':
            try:
                person = Person.objects.get(name=search_string)
                rewards = Reward.objects.filter(apply_reward=person)      
                return (save_xls_rewards(request, rewards))
            except:
                Results=()
        elif search_type == 'apply_application_time':
            date=time.strptime(search_string,"%Y%m") 
            #date_from = datetime.date(date[0], date[1], 1)
            #date_to = datetime.date(date[0], date[1], 31)
            #applications = Application.objects.filter(date_start__range=(date_from, date_to))
            applications = Application.objects.filter(date_start__year=date[0], date_start__month=date[1])
            return (save_xls_applications(request, applications))
        elif search_type == 'apply_reward_time':
            date=time.strptime(search_string,"%Y%m") 
            rewards = Reward.objects.filter(date_apply__year=date[0], date_apply__month=date[1])
            #date_from = datetime.date(date[0], date[1], 1)
            #date_to = datetime.date(date[0], date[1], 31)
            #rewards =Reward.objects.filter(date_apply__range=(date_from, date_to))
            return (save_xls_rewards(request, rewards))
        else:
            Results=()
        return render(request, 'search_result.html',{'Results': Results, 'search':search_form})



