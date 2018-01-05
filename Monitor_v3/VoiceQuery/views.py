from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os,sys
import paramiko
import pymysql
import re


def voicereceive(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        mobile = req.REQUEST.get('mobile','0')
        startTime = req.REQUEST.get('startTime','0')
        nowDate = time.strftime('%Y-%m-%d')
        if startTime == "":
            startTime = nowDate
            logName_http = "/hskj/logs/receive/info.log"
        else:
            if startTime == nowDate:
                logName_http = "/hskj/logs/receive/info.log"
            else:
                logName_http = "/hskj/logs/receive/info.log."+startTime
        command = "grep -a -A2 '"+mobile+"' "+logName_http
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
        s.connect("202.108.253.231",22,"bjywb",pkey=key,timeout=10)
        stdin,stdout,stderr = s.exec_command(command)
        for result in stdout.readlines():
            result=re.sub(mobile,'<strong style="color:red;">'+mobile+'</strong>',result)
            result=re.sub('return','<strong style="color:red;">return</strong>',result)
            table_list.append({'content':result})
        return render_to_response('voicereceive.html',locals())
    else:
        return render_to_response('voicereceive.html',locals())
