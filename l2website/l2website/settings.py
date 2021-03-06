"""
Django settings for l2website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import EMAIL_USE_TLS
#获取当前目录作为基准路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gc0#o@tda)pf0z559l%5e^g=2c8%^yz-tcm^bi3$1q*$@6pzcg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
#添加的app
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'holiday',
)
#设置中间项
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'l2website.urls'

WSGI_APPLICATION = 'l2website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#设置数据库的类型和路径及名称
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
#设置本地语言和时区
LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC+8'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#FILE_CHARSET='gb18030'
#设置默认的文件编码方式
DEFAULT_CHARSET='utf-8' 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#配置静态文件的目录
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (  
    os.path.join(BASE_DIR, 'static').replace('\\','/'),  
)  
#配置模板的目录
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\','/'),
)
#登陆成功后的重定向界面
LOGIN_REDIRECT_URL = 'home/'
#当关闭浏览器的session失效
SESSION_EXPIRE_AT_BROWSER_CLOSE =  True

#配置邮件服务器
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cgy008@gmail.com'
EMAIL_HOST_PASSWORD = 'eling100'
EMAIL_PORT = 587

approve_mail_list = ['cgy008@gmail.com']
email_from = 'cgy008@gmail.com'
http_addr = 'http://localhost:8000/accounts/login/home/'

'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.datangmobile.cn'
EMAIL_HOST_USER = 'chengengyu'
EMAIL_HOST_PASSWORD = 'new.4321'
EMAIL_PORT = 587

approve_mail_list = ['chengengyu@datangmobile.cn']
email_from = 'chengengyu@datangmobile.cn'
http_addr = 'http://172.27.196.43:8000/'
'''

#提交倒休申请时的显示选项
reward_reason_choices = (
                         ('工作负荷高', '工作负荷高',),
                         ('团队活动突出', '团队活动突出',),
                         ('出差', '出差',),
                         ('专项支持', '专项支持',),
                         ('工作业绩突出', '工作业绩突出',),
                         ('法定假日加班', '法定假日加班',),
                        )
