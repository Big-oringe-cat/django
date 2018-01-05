from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os,sys
import paramiko
import pymysql
import re


def Smssubmit(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        startTime = req.REQUEST.get('startTime','0')
        nowDate = time.strftime('%Y-%m-%d')
        hour = req.REQUEST.get('hour','')
        logName_http=""
        logName_cmpp=""
        if startTime == "":
            startTime = nowDate
            logName_http = "/hskj/logs/cluster_server/info.log"
            logName_cmpp = "/hskj/logs/cluster_server/cmpp_info.log"
        else:
            if startTime == nowDate:
                logName_http = "/hskj/logs/cluster_server/info.log"
                logName_cmpp = "/hskj/logs/cluster_server/cmpp_info.log"
            else:
                logName_http = "/hskj/logs/cluster_server/info.log."+startTime
                logName_cmpp = "/hskj/logs/cluster_server/cmpp_info.log."+startTime
        command = "grep -a  '"+search1+"' "+logName_http+" "+logName_cmpp+"| grep -a '"+search2+"'|grep -a '"+startTime+" "+hour+"'|grep -v -a '\-\-'|grep -v 'send test'|grep -v 'receive test'"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        server_list ={}
        server_list = {"p5_node3":["202.108.253.232",10048],"p5_node2":["202.108.253.232",10045],"p5_node4":["202.108.253.232",10049]}
        for line in server_list.values():
                server = line[0]
                port = line[1]
                if port == 10048:
                    server_ip = "172.17.90.48"
                if port == 10045:
                    server_ip = "172.17.90.45"
                if port == 10049:
                    server_ip = "172.17.90.49"
                s = paramiko.SSHClient()
                s.load_system_host_keys()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                s.connect(server,port,username,pkey=key,timeout=10)
                stdin,stdout,stderr = s.exec_command(command)
                for result in stdout.readlines():
                    result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
                    if search2 != "":
                        result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                    result=re.sub('return','<strong style="color:red;">return</strong>',result)
                    table_list.append({'server':server_ip,'content':result})
        return render_to_response('Smssubmit.html',locals())
    else:
        return render_to_response('Smssubmit.html',locals())


def Smssend(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        startTime = req.REQUEST.get('startTime','0')
        nowDate = time.strftime('%Y-%m-%d')
        hour = req.REQUEST.get('hour','')
        logName_http=""
        logName_cmpp=""
        if startTime == "":
            startTime = nowDate
            logName_http = "/hskj/logs/cluster_sender/info.log"
        else:
            if startTime == nowDate:
                logName_http = "/hskj/logs/cluster_sender/info.log"
            else:
                logName_http = "/hskj/logs/cluster_sender/info.log."+startTime
        command = "grep -a  '"+search1+"' "+logName_http+" "+logName_cmpp+"| grep -a '"+startTime+" "+hour+"'|grep -a '"+search2+"'|grep -v -a '\-\-'|grep -v 'send test'|grep -v 'receive test'"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        server_list ={}
        server_list = {"p5_node3":["202.108.253.232",10048],"p5_node2":["202.108.253.232",10045],"p5_node4":["202.108.253.232",10049]}
        for line in server_list.values():
                server = line[0]
                port = line[1]
                if port == 10048:
                    server_ip = "172.17.90.48"
                if port == 10045:
                    server_ip = "172.17.90.45"
                if port == 10049:
                    server_ip = "172.17.90.49"
                s = paramiko.SSHClient()
                s.load_system_host_keys()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                s.connect(server,port,username,pkey=key,timeout=10)
                stdin,stdout,stderr = s.exec_command(command)
                for result in stdout.readlines():
                    result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
                    if search2 != "":
                        result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                    result=re.sub('return','<strong style="color:red;">return</strong>',result)
                    table_list.append({'server':server_ip,'content':result})
        return render_to_response('Smssend.html',locals())
    else:
        return render_to_response('Smssend.html',locals())
