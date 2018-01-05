"""
Django settings for Monitor_v3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60*4800 



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'me3v!qrq3w2n3rj_s2%uvw4mfw+-1(z_5$yz($=fvzyojjlr^j'

import socket
# SECURITY WARNING: don't run with debug turned on in production!

#import sys 
#reload(sys) 
#sys.setdefaultencoding('gbk')

DEBUG = TEMPLATE_DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ShareMethod',
    'MonitorInfo',
    'ServerInfo',
    'ServerMonitorInfo',
    'NoticeInfo',
    'Login',
    'UserInfo',
    'UserGroup',
    'ServerManager',
    'AdminUser',
    'CommentList',
    'ServerManager',
    'HttpMonitor',
    'MonitorPort',
    'TableBackup',
    'DNSManage',
    'ConfigInfo',
    'dutytable',
    'Chart',
    'Monitor_ping',
    'CommandQuery',
    'LogAnalysis',
    'Smsweb',
    'LiuliangQuery',
    'VoiceQuery',
    'PhoneCard',
    'OutBox',
    'DeliverQuery',
    'SendQuery',
    'ServiceSmsInfo',
    'AutoSendConfig',
    'Repository',
    'clusterlog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     #'pagination.middleware.PaginationMiddleware',

)

ROOT_URLCONF = 'Monitor_v3.urls'

WSGI_APPLICATION = 'Monitor_v3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monitor_ping',
        'USER': 'yunwei',
        'PASSWORD': 'mobile707',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'
FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL='/media/'

STATIC_ROOT = 'static'

if socket.gethostname() == 'alarm-kvm.zhaowei':
    STATIC_PATH='/hskj/web/apache/htdocs/Monitor_v3_doc/Monitor_v3/static'

    TEMPLATE_DIRS = (
                 '/hskj/web/apache/htdocs/Monitor_v3_doc/Monitor_v3/ShareMethod/templates',
                 )

else:
    STATIC_PATH='E:\workspace\Monitor_v3\static'

    TEMPLATE_DIRS = (
                 'E:\workspace\Monitor_v3\ShareMethod\templates',
                 )
