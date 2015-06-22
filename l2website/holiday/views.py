from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from holiday.models import Application, Reward, Person, ApplicationRollback, RewardDeadline
from holiday.forms import RewardForm, PersonForm, ApplicationForm, RollbackForm
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.forms.widgets import TextInput, NumberInput, DateInput, Select, HiddenInput
import datetime, time
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import xlwt
from holiday.email import *
from l2website.settings import approve_mail_list, reward_reason_choices
from l2website.views import login_home
import datetime
# Create your views here.


#获取审批者的邮箱地址，在setting中定义
def get_approve_mail_list():
    return approve_mail_list


#申请倒休页面的生成函数
@csrf_protect
@login_required
@permission_required('holiday.apply_reward', login_url="/no_permission/")
def apply_reward(request):
    datenow = datetime.date.today()
    deadline = RewardDeadline.objects.get(id=1)
    print(deadline.date)
    if datenow > deadline.date:
        return render(request, 'deadline.html', {'deadline': deadline, 'now': datenow})
    email_list = []
    if request.method == "POST":
        form = RewardForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person_apply = Person.objects.get(name=request.user.username)
            reward_apply = Reward(type=cd['type'], reason=cd['reason'], days_apply=cd['days_apply'], days_approve=cd['days_apply'],
                            apply_reward=person_apply, reward_reward=cd['person'], approve_reward=cd['person'],
                            date_approve=datetime.date.today(), approve_flag=False)
            reward_apply.save()
            email_list = get_approve_mail_list()
            #根据发送邮件的结果，进行提示
            if send_notify('新的倒休奖励申请', email_list, 'apply', 'reward', reward_apply):
                messages.success(request, '申请成功，提醒邮件发送成功')
            else:
                messages.error(request, '申请成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        #不是post时则生成一个默认空的界面，或者提交的数据有问题，重新生成界面可以显示错误信息
        form = RewardForm()
    return render(request, 'apply_reward.html', {'form':form})

#审批倒休申请的界面
@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def approve_reward(request):
    #定义formset，主要是定义显示的widget
    RewardFormSet = modelformset_factory(Reward, extra=0,
                                         widgets={
                                                  #'apply_reward': Select(attrs={'disabled': "disabled"}),
                                                  #'reward_reward': Select(attrs={'disabled': "disabled"}),
                                                  'days_apply': TextInput(attrs={'readonly': "readonly"}),
                                                  'approve_reward': HiddenInput(attrs={}),
                                                  'type': Select(choices=reward_reason_choices),
                                                  #'type' :  TextInput(attrs={'readonly': "readonly"}),
                                                  'date_apply' :  DateInput(attrs={'readonly': "readonly"}),
                                                  'date_approve': DateInput(attrs={'readonly': "readonly"}),
                                                  }
                                         )
    #获取当前的用户的数据信息
    person_approve = Person.objects.get(name=request.user.username)
    email_list = []
    if request.method == "POST": 
        rewards = RewardFormSet(request.POST)
        #对数据有效性进行验证
        if rewards and rewards.is_valid():
            for reward in rewards:
                #如果审批通过则进行保存
                if reward.cleaned_data['approve_flag'] == True:
                    #每次都需要现查一下，保证是最新的信息，不然网页获取的信息是一个固定的，当同时审批同一个人的时候就会出问题
                    person = Person.objects.get(name=reward.cleaned_data['reward_reward'].name)
                    person.holidayNum = person.holidayNum + reward.cleaned_data['days_approve']
                    person.holidayNumSum = person.holidayNumSum + reward.cleaned_data['days_approve']
                    reward.instance.approve_reward = person_approve
                    reward.instance.date_approve = datetime.date.today()
                    person.save()
                    reward.save()
                    #给申请人和倒休人都发送邮件   
                    email_list = [reward.cleaned_data['apply_reward'].email, reward.cleaned_data['reward_reward'].email]
                    if send_notify('您的倒休申请已审批', email_list, 'approve', 'reward', reward.instance):
                        messages.success(request, person.chinese_name + '的申请处理成功，提醒邮件发送成功')
                    else:
                        messages.error(request, person.chinese_name + '的申请处理成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        rewards = RewardFormSet(queryset=Reward.objects.exclude(approve_flag='1'))
    #如果数据有问题也会重新生成原来的界面，并显示错误的信息
    return render(request, 'approve_reward.html',{'Rewards': rewards})


#申请倒休取消的界面
@csrf_protect
@login_required
@permission_required('holiday.apply_application', login_url="/no_permission/")
def apply_rollback(request):
    person_apply = Person.objects.get(name=request.user.username)
    email_list = []
    if request.method == "POST":
        form = RollbackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  
            rollback_apply = ApplicationRollback(reason=cd['reason'], days_apply=cd['days_apply'], days_approve= cd['days_apply'],
                            apply_rollback=person_apply, approve_rollback=person_apply, date_approve=datetime.date.today(), approve_flag=False)
            rollback_apply.save()
            #给审批人发邮件提醒
            email_list = get_approve_mail_list()
            #send_email_apply_application(message_type='apply', subject_type='reward', name=person_apply.chinese_name, email_to=email_list)
            if send_notify('新的倒休取消申请', email_list, 'apply', 'rollback', rollback_apply):
                messages.success(request, '申请成功，提醒邮件发送成功')
            else:
                messages.error(request, '申请成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        form = RewardForm()
    return render(request, 'apply_rollback.html', {'form':form})

'''
审批倒休取消的界面生成函数
'''
@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def approve_rollback(request):
    RollbackFormSet = modelformset_factory(ApplicationRollback, extra=0,
                                           widgets={
                                                  #'approve_rollback': Select(attrs={'disabled': "disabled"}),
                                                  #'apply_rollback': Select(attrs={'disabled': "disabled"}),
                                                  '''
                                                                                              由于第一个页面只是显示数据，当数据被提交后，会用所有的数据进行保存，
                                                                                            所以必须提交数据库对象的所有字段，对于这种情况，把不需要显示出来的字段也提交到界面中但是隐藏起来
                                                  '''
                                                  'approve_rollback': HiddenInput(attrs={}),
                                                  'date_approve': DateInput(attrs={'readonly': "readonly"}),
                                                  'days_apply': TextInput(attrs={'readonly': "readonly"}),
                                                  }
                                           )
    person_approve = Person.objects.get(name=request.user.username)
    email_list = []
    if request.method == "POST": 
        rollbacks = RollbackFormSet(request.POST)
        if rollbacks and rollbacks.is_valid():
            for rollback in rollbacks:
                if rollback.cleaned_data['approve_flag'] == True:
                    person = Person.objects.get(name=rollback.cleaned_data['apply_rollback'].name)
                    person.holidayNum = person.holidayNum + rollback.cleaned_data['days_apply']
                    person.holidayNumUsed = person.holidayNumUsed - rollback.cleaned_data['days_apply']
                    rollback.instance.approve_rollback = person_approve
                    rollback.instance.date_approve = datetime.date.today()
                    person.save()
                    rollback.save()         
                    email_list = [rollback.cleaned_data['approve_rollback'].email]
                    if send_notify('您的倒休取消已审批', email_list, 'approve', 'rollback', rollback.instance):
                        messages.success(request, person.chinese_name + '的申请处理成功，提醒邮件发送成功')
                    else:
                        messages.error(request, person.chinese_name + '的申请处理成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        rollbacks = RollbackFormSet(queryset=ApplicationRollback.objects.exclude(approve_flag='1'))
    return render(request, 'approve_rollback.html',{'rollbacks': rollbacks})





'''
显示个人信息页面，获取当前的用户，并查找所有的数据
'''
@csrf_protect
@login_required
@permission_required('holiday.apply_application', login_url="/no_permission/")
def show_my_info(request):
    person = Person.objects.get(name=request.user.username)
    applications = Application.objects.filter(apply_application=person)
    rewards = Reward.objects.filter(reward_reward=person)
    rollbacks = ApplicationRollback.objects.filter(apply_rollback=person)
    return render(request, 'show_my_info.html', {'person': person, 'applications': applications, 'rewards': rewards, 'rollbacks':rollbacks})



'''
显示用户提交的倒休申请
'''
@csrf_protect
@login_required
@permission_required('holiday.apply_reward', login_url="/no_permission/")
def show_my_apply_reward(request):
    person = Person.objects.get(name=request.user.username)
    rewards = Reward.objects.filter(apply_reward=person)
    return render(request, 'show_my_apply_reward.html', {'person': person,'rewards': rewards})

'''
倒休使用界面生成
'''
@csrf_protect
@login_required
@permission_required('holiday.apply_application', login_url="/no_permission/")
def apply_application(request):
    person = Person.objects.get(name=request.user.username)
    applications = Application.objects.filter(apply_application=person, approve_flag=False)
    days_tobe_approve = 0
    for application in applications:
        days_tobe_approve = days_tobe_approve + application.days_apply
    email_list = []
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        form.holidayNum = person.holidayNum - days_tobe_approve
        if form.is_valid():
            cd = form.cleaned_data
            application = Application(reason=cd['reason'], days_apply=cd['days_apply'], days_approve=cd['days_apply'],
                            date_start=cd['date_start'], date_end=cd['date_end'], apply_application=person, start_meridiem=cd['start_meridiem'],
                            end_meridiem=cd['end_meridiem'], approve_application=person, date_approve=datetime.date.today(), approve_flag=False)
            application.save()
            email_list = get_approve_mail_list()
            if send_notify('新的倒休使用申请', email_list, 'apply', 'application', application):
                messages.success(request, '申请成功，提醒邮件发送成功')
            else:
                messages.error(request, '申请成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        form = ApplicationForm()
    return render(request, 'apply_application.html', {'form':form, 'person':person, 'days_tobe_approve': days_tobe_approve})


'''
审批倒休使用界面生成
'''
@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def approve_application(request):
    ApplicationFormSet = modelformset_factory(Application,extra=0,
                                              widgets={                                                  
                                                       'date_apply' :  DateInput(attrs={'readonly': "readonly"}),
                                                       'date_approve': DateInput(attrs={'readonly': "readonly"}),
                                                       'days_apply': TextInput(attrs={'readonly': "readonly"}),
                                                       #'apply_application': Select(attrs={'disabled': "disabled"}),
                                                       #'apply_application': TextInput(attrs={'readonly': "readonly", 'value': "apply_application.chinese_name"}),
                                                       'approve_application': HiddenInput(attrs={}),
                                                       }
                                              )
    person_approve = Person.objects.get(name=request.user.username)
    email_list = []
    if request.method == "POST": 
        applications = ApplicationFormSet(request.POST)
        if applications:
            if applications.is_valid():
                for application in applications:
                    if application.cleaned_data['approve_flag'] == True:
                        person = Person.objects.get(name=application.cleaned_data['apply_application'].name)
                        person.holidayNum = person.holidayNum - application.cleaned_data['days_approve']
                        person.holidayNumUsed = person.holidayNumUsed + application.cleaned_data['days_approve']
                        application.instance.approve_rollback = person_approve
                        application.instance.date_approve = datetime.date.today()
                        person.save()
                        application.save()
                        email_list = [person.email]
                        if send_notify('您的倒休使用已审批', email_list, 'approve', 'application', application.instance):
                            messages.success(request, person.chinese_name + '的申请处理成功，提醒邮件发送成功')
                        else:
                            messages.error(request, person.chinese_name + '的申请处理成功，提醒邮件发送失败')
                return HttpResponseRedirect("/accounts/login/home/")
    else:
        applications = ApplicationFormSet(queryset=Application.objects.exclude(approve_flag='1'))       
    return render(request, 'approve_application.html',{'Applications': applications})


'''
返回搜索的界面
'''
@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")    
def search_form(request):
    return render(request, 'search_form.html')


'''
根据提交的搜索类型和关键词进行搜索，并把类型关键词在此返回到界面中，当需要输出到excel中去时，会需要在此搜索
这里本来想是处理当前的界面的数据，直接输出到excel的，但是发现一个是界面只显示了部分的数据，因为界面大小的原因，一些不需要的字段未显示，但是输出到excel中就会显示的多一些，
另外将这两个部分独立开来，互相不会影响。其实可以把搜索的部分弄出来，生成界面或者excel的单独去做函数，但是目前还没有做的那么通用
这里本来是搜索输入的关键字有误时会直接报错，目前通过异常的形式，讲错误信息输出到搜索界面去
'''
@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def search(request):
    errors = []
    if 'search_string' in request.POST:
        search_string = request.POST['search_string']
        if not search_string:
            errors.append('请输入搜索内容')
        else:
            search_type = request.POST['search_type']
            search_form = {'type': search_type, 'text': search_string}
            #搜索个人信息，直接使用了个人信息的模板
            if search_type == 'person_name':
                try :
                    person = Person.objects.get(name=search_string)
                    applications = Application.objects.filter(apply_application=person)
                    rewards = Reward.objects.filter(reward_reward=person)
                    rollbacks = ApplicationRollback.objects.filter(apply_rollback=person)
                    return render(request, 'show_my_info.html', {'person': person, 'applications': applications, 
                                                                 'rewards': rewards, 'rollbacks': rollbacks, 'search':search_form})
                except:
                    errors.append('查无此人')
            #搜索某人提交的倒休申请
            elif search_type == 'apply_name':
                try:
                    person = Person.objects.get(name=search_string)
                    Results = Reward.objects.filter(apply_reward=person)
                    #RewardFormSet = modelformset_factory(Reward,extra=0)
                    #Results = RewardFormSet(queryset=Reward.objects.filter(apply_reward=person))
                except:
                #搜索有误时添加error
                    errors.append('查无此人')
            #按照倒休使用中的开始时间的年和月进行申请
            elif search_type == 'apply_application_time':
                try:
                    date=time.strptime(search_string,"%Y%m") 
                    Results = Application.objects.filter(date_start__year=date[0], date_start__month=date[1])
                except:
                    Results = ()
                    errors.append('请输入正确的格式')
                #date_from = datetime.date(date[0], date[1], 1)
                #date_to = datetime.date(date[0], date[1], 31)
                #ApplicationFormSet = modelformset_factory(Application,extra=0)
                #Results = ApplicationFormSet(queryset=Application.objects.filter(date_start__year=date[0], date_start__month=date[1]))
            #根据提交倒休申请的年和月进行搜索
            elif search_type == 'apply_reward_time':
                try:
                    date=time.strptime(search_string,"%Y%m") 
                    Results = Reward.objects.filter(date_apply__year=date[0], date_apply__month=date[1])
                except:
                    errors.append('请输入正确的格式')
                #date_from = datetime.date(date[0], date[1], 1)
                #date_to = datetime.date(date[0], date[1], 31)
                #RewardFormSet = modelformset_factory(Reward,extra=0)
                #Results = RewardFormSet(queryset=Reward.objects.filter(date_apply__year=date[0], date_apply__month=date[1]))
            #没有问题时或者搜索成功，进入结果显示界面
            if len(errors) == 0:
                return render(request, 'search_result.html',{'Results': Results, 'search':search_form})
    #当输入关键词出现 问题时会重新返回搜索界面
    return render(request, 'search_form.html',{'errors': errors})

#没有相关权限时的返回界面
@login_required
def no_permission(request):
    return render(request, 'no_permission.html')





