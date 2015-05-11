from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from holiday.models import Application, Reward, Person, ApplicationRollback
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



def get_approve_mail_list():
    return approve_mail_list

@csrf_protect
@login_required
@permission_required('holiday.apply_reward', login_url="/no_permission/")
def apply_reward(request):
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
            if send_notify('新的倒休奖励申请', email_list, 'apply', 'reward', reward_apply):
                messages.success(request, '申请成功，提醒邮件发送成功')
            else:
                messages.error(request, '申请成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        form = RewardForm()
    return render(request, 'apply_reward.html', {'form':form})


@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def approve_reward(request):
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
    person_approve = Person.objects.get(name=request.user.username)
    email_list = []
    if request.method == "POST": 
        rewards = RewardFormSet(request.POST)
        if rewards and rewards.is_valid():
            for reward in rewards:
                if reward.cleaned_data['approve_flag'] == True:                    
                    person = reward.cleaned_data['reward_reward']
                    person.holidayNum = person.holidayNum + reward.cleaned_data['days_approve']
                    person.holidayNumSum = person.holidayNumSum + reward.cleaned_data['days_approve']
                    reward.instance.approve_reward = person_approve
                    reward.instance.date_approve = datetime.date.today()
                    person.save()
                    reward.save()         
                    email_list = [reward.cleaned_data['apply_reward'].email, reward.cleaned_data['reward_reward'].email]
                    if send_notify('您的倒休申请已审批', email_list, 'approve', 'reward', reward.instance):
                        messages.success(request, person.chinese_name + '的申请处理成功，提醒邮件发送成功')
                    else:
                        messages.error(request, person.chinese_name + '的申请处理成功，提醒邮件发送失败')
            return HttpResponseRedirect("/accounts/login/home/")
    else:
        rewards = RewardFormSet(queryset=Reward.objects.exclude(approve_flag='1'))
    return render(request, 'approve_reward.html',{'Rewards': rewards})


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


@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")
def approve_rollback(request):
    RollbackFormSet = modelformset_factory(ApplicationRollback, extra=0,
                                           widgets={
                                                  #'approve_rollback': Select(attrs={'disabled': "disabled"}),
                                                  #'apply_rollback': Select(attrs={'disabled': "disabled"}),
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
                    person = rollback.cleaned_data['apply_rollback']
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






@csrf_protect
@login_required
@permission_required('holiday.apply_application', login_url="/no_permission/")
def show_my_info(request):
    person = Person.objects.get(name=request.user.username)
    applications = Application.objects.filter(apply_application=person)
    rewards = Reward.objects.filter(reward_reward=person)
    rollbacks = ApplicationRollback.objects.filter(apply_rollback=person)
    return render(request, 'show_my_info.html', {'person': person, 'applications': applications, 'rewards': rewards, 'rollbacks':rollbacks})

@csrf_protect
@login_required
@permission_required('holiday.apply_reward', login_url="/no_permission/")
def show_my_apply_reward(request):
    person = Person.objects.get(name=request.user.username)
    rewards = Reward.objects.filter(apply_reward=person)
    return render(request, 'show_my_apply_reward.html', {'person': person,'rewards': rewards})

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
                        person = application.cleaned_data['apply_application']
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

@csrf_protect
@login_required
@permission_required('holiday.approve', login_url="/no_permission/")    
def search_form(request):
    return render(request, 'search_form.html')

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
            elif search_type == 'apply_name':
                try:
                    person = Person.objects.get(name=search_string)
                    Results = Reward.objects.filter(apply_reward=person)
                    #RewardFormSet = modelformset_factory(Reward,extra=0)
                    #Results = RewardFormSet(queryset=Reward.objects.filter(apply_reward=person))
                except:
                    errors.append('查无此人')
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
            if len(errors) == 0:
                return render(request, 'search_result.html',{'Results': Results, 'search':search_form})
    return render(request, 'search_form.html',{'errors': errors})

@login_required
def no_permission(request):
    return render(request, 'no_permission.html')





