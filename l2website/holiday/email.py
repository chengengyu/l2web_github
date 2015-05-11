from django.core.mail import send_mail
from django.core import mail
from l2website.settings import email_from, http_addr
from django.core.mail import EmailMessage
from django.template import loader
from holiday.models import Application, Reward, Person, ApplicationRollback



'''
发送html格式的邮件的函数，调用django库中的函数进行html文本的生成。模板放在temlpate里。
'''

def send_notify(subject, email_to, message_type, context_type, context):
    html_content = loader.render_to_string('mail/mail_context.html', {'message_type': message_type, context_type: context})
    msg = EmailMessage(subject, html_content, email_from, email_to)
    msg.content_subtype = "html"
    #失败后不进行任何处理，外面调用者根据返回值来进行提醒。
    return msg.send(fail_silently=True)
    
'''
使用html格式邮件时的测试函数，本来都是都单独设置的模板，后来换成了通用的模板
'''
def send_html_mail(request):
    person_apply = Person.objects.get(name=request.user.username)
    html_content = loader.render_to_string('mail/mail_reward.html', {'person': person_apply})
    msg = EmailMessage('test', html_content, 'cgy008@gmail.com', ['cgy008@gmail.com'])
    msg.content_subtype = "html"
    msg.send()

'''
最初的send_mail函数，直接调用系统的函数，只是为了使用异常处理，所以才又封装了一下
'''
def send_email(subject, message, email_to):
    try:
        send_mail(subject, message, email_from, email_to, fail_silently=False)
        return True
    except:
        return False



'''
最早的发送通知邮件的函数，只能简单的设置发送的正文和标题，因为需要发送表格，所以废弃了此函数
'''
def send_email_apply_application(email_to, message_type='approve', subject_type='reward', name=''):
    if message_type == 'apply': 
        if subject_type == 'reward':    
                subject = "新的倒休奖励申请"
        else:
            subject = "新的倒休使用申请"
        message = name + "提了一份新的申请需要您审批\n 详情请点击" + http_addr

    else:
        if subject_type == 'reward':    
            subject = '倒休奖励申请审批结果'
        else:
            subject = '倒休使用审批结果'
        message = name + " 您的申请已审批结束，\n 详情请点击" + http_addr
    return send_email(subject, message, email_to)

