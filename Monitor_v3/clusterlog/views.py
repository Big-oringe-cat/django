from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os,sys
import paramiko
import threading
import re


def HttpLog(req):
    if req.method == 'POST':
        type = req.REQUEST.get('type','cluster_64')
        deal = req.REQUEST.get('deal','submit')
        user_id = req.REQUEST.get('user_id','你好')
        search1 = req.REQUEST.get('search1','')
        if search1 != '':
            if 'return_code' not in search1: 
                search1 = 'return_code: '+search1
        search2 = req.REQUEST.get('search2','0')
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        if startTime == "":
            startTime = nowDate
        if startTime == nowDate:
            if deal == 'Request_ip':
                command="grep -a '"+user_id+"' /hskj/logs/httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
            if deal == 'submit':
                command="grep -a '"+user_id+"' /hskj/logs/info.log |grep -a '"+search1+"' |grep -a '"+search2+"'|grep -v '状态'|grep -v '上行'|grep -v '余额'|awk -F '[\; ]+'  '{print $6,$7,$8,$9,$11,$14}'|sort|uniq"
#            if deal == '':
#                command="grep -a '"+user_id+"' httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
#            if deal == 'Request_ip':
#                command="grep -a '"+user_id+"' httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
        else:
            if deal == 'Request_ip':
                command="grep -a '"+user_id+"' /hskj/logs/httpPostLog.log."+startTime+" |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
            if deal == 'submit':
                command="grep -a '"+user_id+"' /hskj/logs/info.log."+startTime+" |grep -a '"+search1+"' |grep -a '"+search2+"'|grep -v '状态'|grep -v '上行'|grep -v '余额'|awk -F '[\; ]+'  '{print $6,$7,$8,$9,$11,$14}'|sort|uniq"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        server_list ={}
        if type == "cluster_64":
            server_list = {"c1_56":["210.14.134.81",10056],"c1_57":["210.14.134.81",10057],"c1_58":["210.14.134.81",10058]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10056:
                        server_ip = "172.16.10.56"
                    if port == 10057:
                        server_ip = "172.16.10.57"
                    if port == 10058:
                        server_ip = "172.16.10.58"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
#                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_227":
            server_list = {"c2_24":["202.108.253.227",10024],"c2_25":["202.108.253.227",10025],"c2_33":["202.108.253.227",10033],"c2_34":["202.108.253.227",10034]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10024:
                        server_ip = "172.17.90.24"
                    if port == 10025:
                        server_ip = "172.17.90.25"
                    if port == 10033:
                        server_ip = "172.17.90.33"
                    if port == 10034:
                        server_ip = "172.17.90.34"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
#                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_35":
            server_list = {"c3_61":["36.110.168.35",10061],"c3_62":["36.110.168.35",10062],"c3_63":["36.110.168.35",10063]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.130.61"
                    if port == 10062:
                        server_ip = "172.17.130.62"
                    if port == 10063:
                        server_ip = "172.17.130.63"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_226":
            server_list = {"c4_61":["111.13.124.226",10061],"c4_62":["111.13.124.226",10062],"c4_63":["111.13.124.226",10063]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.140.61"
                    if port == 10062:
                        server_ip = "172.17.140.62"
                    if port == 10063:
                        server_ip = "172.17.140.63"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_21":
            server_list = {"c5_61":["222.73.121.21",10061],"c5_62":["222.73.121.21",10062]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.30.61"
                    if port == 10062:
                        server_ip = "172.17.30.62"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})

        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response("HttpLog.html",locals())
    else:
        return render_to_response("HttpLog.html",locals())

def CmppLog(req):
    if req.method == 'POST':
#        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
#        search1 = req.REQUEST.get('search1','0')
#        search2 = req.REQUEST.get('search2','0')
#        hour = req.REQUEST.get('hour','')
        type = req.REQUEST.get('type','cluster_64')
        deal = req.REQUEST.get('deal','cluster_64')
        user_id = req.REQUEST.get('user_id','你好')
#        nowDate = time.strftime('%Y-%m-%d')
#        startTime = req.REQUEST.get('startTime',nowDate)
#        nowDate = time.strftime('%Y-%m-%d')
#        logName_http=""
#        if startTime == "":
#            startTime = nowDate
#            logName_http = "/hskj/logs/info.log"
#        else:
#            if startTime == nowDate:
#                logName_http = "/hskj/logs/info.log"
#            else:
#                logName_http = "/hskj/logs/info.log."+startTime
#        command = "grep -a  '"+search1+"' "+logName_http+" "+logName_cmpp+" "+logName_sgip+" "+logName_smgp+" | grep -a '"+search2+"'|grep -v -a '\-\-'|grep -v 'send test'|grep -v 'receive test'|grep -v 'report'"
        if deal == 'Request_ip':
            command="grep -a '"+user_id+"' /hskj/logs/httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
        else:
            command = "grep -a 'yh6851' /hskj/logs/httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq -c|awk '{print $2}'"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        server_list ={}
        if type == "cluster_64":
            server_list = {"c1_56":["210.14.134.81",10056],"c1_57":["210.14.134.81",10057],"c1_58":["210.14.134.81",10058]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10056:
                        server_ip = "172.16.10.56"
                    if port == 10057:
                        server_ip = "172.16.10.57"
                    if port == 10058:
                        server_ip = "172.16.10.58"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
#                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_227":
            server_list = {"c2_24":["202.108.253.227",10024],"c2_25":["202.108.253.227",10025],"c2_33":["202.108.253.227",10033],"c2_34":["202.108.253.227",10034]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10024:
                        server_ip = "172.17.90.24"
                    if port == 10025:
                        server_ip = "172.17.90.25"
                    if port == 10033:
                        server_ip = "172.17.90.33"
                    if port == 10034:
                        server_ip = "172.17.90.34"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
#                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_35":
            server_list = {"c3_61":["36.110.168.35",10061],"c3_62":["36.110.168.35",10062],"c3_63":["36.110.168.35",10063]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.130.61"
                    if port == 10062:
                        server_ip = "172.17.130.62"
                    if port == 10063:
                        server_ip = "172.17.130.63"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_226":
            server_list = {"c4_61":["111.13.124.226",10061],"c4_62":["111.13.124.226",10062],"c4_63":["111.13.124.226",10063]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.140.61"
                    if port == 10062:
                        server_ip = "172.17.140.62"
                    if port == 10063:
                        server_ip = "172.17.140.63"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_21":
            server_list = {"c5_61":["222.73.121.21",10061],"c5_62":["222.73.121.21",10062]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10061:
                        server_ip = "172.17.30.61"
                    if port == 10062:
                        server_ip = "172.17.30.62"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
#                        if search2 != "":
#                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
#                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})

        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response('CmppLog.html',locals())
    else:
        return render_to_response('CmppLog.html',locals())

def SmgpLog(req):
    return render_to_response('SmgpLog.html',locals())

def SgipLog(req):
    return render_to_response('SgipLog.html',locals())
