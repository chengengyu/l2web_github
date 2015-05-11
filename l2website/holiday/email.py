from django.core.mail import send_mail
from django.core import mail
from l2website.settings import email_from, http_addr
from django.core.mail import EmailMessage
from django.template import loader
from holiday.models import Application, Reward, Person, ApplicationRollback

def send_html_mail(request):
    person_apply = Person.objects.get(name=request.user.username)
    html_content = loader.render_to_string('mail/mail_reward.html', {'person': person_apply})
    msg = EmailMessage('test', html_content, 'cgy008@gmail.com', ['cgy008@gmail.com'])
    msg.content_subtype = "html"
    msg.send()

def send_notify(subject, email_to, message_type, context_type, context):
    html_content = loader.render_to_string('mail/mail_context.html', {'message_type': message_type, context_type: context})
    msg = EmailMessage(subject, html_content, email_from, email_to)
    msg.content_subtype = "html"
    return msg.send(fail_silently=True)
    
    
def send_email(subject, message, email_to):
    try:
        send_mail(subject, message, email_from, email_to, fail_silently=False)
        return True
    except:
        return False
    
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

