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
                
def CommandQuery(req):
    if req.method == 'POST':
        type = req.REQUEST.get('type','cmpp')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print("开始时间："+str(NowTime))
        command = req.REQUEST.get('command','0')
        print("---command=-------"+command+"----------")
        username = 'root'
        pkey_file='/root/.ssh/id_rsa'
        ip_file = '/hskj/script/ip.txt'
        table_list = []
        f = file(ip_file)
        for line in f.readlines():
            f.close()
            if type in line and "bak" not in line and "vpn" not in line:
                f_line = line.strip().split()
                server = f_line[2]
                port = f_line[5]
                if len(line) == 0:break
                s = paramiko.SSHClient()
                s.load_system_host_keys()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                key = paramiko.RSAKey.from_private_key_file(pkey_file,'666666')
                s.connect(server,port,username,pkey=key,timeout=10)
                stdin,stdout,stderr = s.exec_command(command)
                for result in stdout.readlines():
                    table_list.append({'server':server,'content':result})
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print("结束时间："+str(NowTime))
        return render_to_response("CmdResult.html",locals())
    else:
        return render_to_response("CmdResult.html",locals())
        
def clusterSubmit(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        hour = req.REQUEST.get('hour','')
        type = req.REQUEST.get('type','cluster_64')
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        nowDate = time.strftime('%Y-%m-%d')
        logName_http=""
        logName_cmpp=""
        if startTime == "":
            startTime = nowDate
            logName_http = "/hskj/logs/info.log"
            logName_cmpp = "/hskj/logs/cmpp_info.log"
            logName_sgip = "/hskj/logs/sgip_info.log"
            logName_smgp = "/hskj/logs/smgp_info.log"
        else:
            if startTime == nowDate:
                logName_http = "/hskj/logs/info.log"
                logName_cmpp = "/hskj/logs/cmpp_info.log"
                logName_sgip = "/hskj/logs/sgip_info.log"
                logName_smgp = "/hskj/logs/smgp_info.log"
            else:
                logName_http = "/hskj/logs/info.log."+startTime
                logName_cmpp = "/hskj/logs/cmpp_info.log."+startTime
                logName_sgip = "/hskj/logs/sgip_info.log."+startTime
                logName_smgp = "/hskj/logs/smgp_info.log."+startTime
        command = "grep -a  '"+search1+"' "+logName_http+" "+logName_cmpp+" "+logName_sgip+" "+logName_smgp+"|grep -a '"+startTime+" "+hour+"' | grep -a '"+search2+"'|grep -v -a '\-\-'|grep -v 'send test'|grep -v 'receive test'|grep -v 'report'"
        username = 'root'
        pkey_file='/root/.ssh/id_rsa'
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
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
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
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
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
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
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
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
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
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_local":
            server_list = {"c6_1":["192.168.81.203",22],"c6_2":["192.168.81.203",23]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 22:
                        server_ip = "192.168.81.203"
                    if port == 23:
                        server_ip = "192.168.81.203"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'666666')
                    ##s.connect(server,'22',username,pkey=key,timeout=30)
                    s.connect(server,22,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
                        if search2 != "":
                            result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
                        result=re.sub('return','<strong style="color:red;">return</strong>',result)
                        table_list.append({'server':server_ip,'content':result})

        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response("Cluster_Submit.html",locals())
    else:
        return render_to_response("Cluster_Submit.html",locals())
            
def clusterSend(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        type = req.REQUEST.get('type','cluster_64')
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        nowDate = time.strftime('%Y-%m-%d')
        hour = req.REQUEST.get('hour','')
        logName=""
        if startTime == "":
            startTime = nowDate
            logName = "/hskj/logs/info.log"
        else:
            if startTime == nowDate:
                logName = "/hskj/logs/info.log"
            else:
                logName = "/hskj/logs/info.log."+startTime
        command = "grep -a '"+search1+"' "+logName+" | grep -a '"+search2+"'|grep -a '"+startTime+" "+hour+"'"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        table_list = []
        server_list ={}
        if type == "cluster_64":
            server_list = {"c1_62":["210.14.134.81",10062],"c1_63":["210.14.134.81",10063],"c1_64":["210.14.134.81",10064],"c1_65":["210.14.134.81",10065],"c1_84":["210.14.134.81",10084]}
            for line in server_list.values():   
                    server = line[0]
                    port = line[1]
                    if port == 10062:
                        server_ip = "172.16.10.62"
                    if port == 10063:
                        server_ip = "172.16.10.63"
                    if port == 10064:
                        server_ip = "172.16.10.64"
                    if port == 10065:
                        server_ip = "172.16.10.65"
                    if port == 10084:
                        server_ip = "172.16.10.84"
                    
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_227":
            server_list = {"c2_29":["202.108.253.227",10029],"c2_30":["202.108.253.227",10030],"c2_31":["202.108.253.227",10031],"c2_32":["202.108.253.227",10032]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10029:
                        server_ip = "172.17.90.29"
                    if port == 10030:
                        server_ip = "172.17.90.30"
                    if port == 10031:
                        server_ip = "172.17.90.31"
                    if port == 10032:
                        server_ip = "172.17.90.32"
                    

                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_35":
            server_list = {"c3_81":["36.110.168.35",10081],"c3_82":["36.110.168.35",10082],"c3_83":["36.110.168.35",10083],"c3_84":["36.110.168.35",10084]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10081:
                        server_ip = "172.17.130.81"
                    if port == 10082:
                        server_ip = "172.17.130.82"
                    if port == 10083:
                        server_ip = "172.17.130.83"
                    if port == 10084:
                        server_ip = "172.17.130.84"

                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_226":
            server_list = {"c3_81":["111.13.124.226",10081],"c3_82":["111.13.124.226",10082],"c3_83":["111.13.124.226",10083],"c3_84":["36.110.168.35",10084]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10081:
                        server_ip = "172.17.140.81"
                    if port == 10082:
                        server_ip = "172.17.140.82"
                    if port == 10083:
                        server_ip = "172.17.140.83"
                    if port == 10084:
                        server_ip = "172.17.140.84"

                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'&U*I(O1208')
                    s.connect(server,port,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        table_list.append({'server':server_ip,'content':result})
        if type == "cluster_21":
            server_list = {"c5_81":["222.73.121.21",10081],"c5_82":["222.73.121.21",10082]}
            for line in server_list.values():
                    server = line[0]
                    port = line[1]
                    if port == 10081:
                        server_ip = "172.17.30.81"
                    if port == 10082:
                        server_ip = "172.17.30.82"
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
            
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response("Cluster_Send.html",locals())
    else:
        return render_to_response("Cluster_Send.html",locals())       


def clusterSpeed(req):
    if req.method == 'POST':
        operatorName=req.session.get('username')
        user_id = req.REQUEST.get('user_id','0').strip()
        print(user_id)
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        type = req.REQUEST.get('type','cluster_64')
        now = time.strftime('%Y%m%d%H%M%S')
        file = "/hskj/tmp/ClusterSpeed/"+user_id+"_"+now+".txt"

        if startTime == "":
            startTime = nowDate
        if search1 == "nowtype":
            if search2 == "smgp":
                logName = "/hskj/logs/smgp_info.log"
                command = "tail -100000 "+logName+" | grep -a '"+user_id+"' |grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c"
                cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
            elif search2 == "cmpp":
                logName = "/hskj/logs/cmpp_info.log"
                command = "tail -100000 "+logName+" | grep -a '"+user_id+"' |grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c"
                cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
            elif search2 == "sgip":
                logName = "/hskj/logs/sgip_info.log"
                command = "tail -100000 "+logName+" | grep -a '"+user_id+"' |grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c"
                cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
            else:
                logName = "/hskj/logs/info.log"
                command = "tail -100000 "+logName+" | grep -a '"+user_id+"' |grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c"
                cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"

            print ("logName="+logName)
            print(command)
        else:
            if startTime == nowDate:
                if search2 == "smgp":
                    logName = "/hskj/logs/smgp_info.log"
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                elif search2 == "cmpp":
                    logName = "/hskj/logs/cmpp_info.log"
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                elif search2 == "sgip":
                    logName = "/hskj/logs/sgip_info.log"
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                else:
                    logName = "/hskj/logs/info.log"
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
            else:
                if search2 == "smgp":
                    logName = "/hskj/logs/smgp_info.log."+startTime
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                elif search2 == "cmpp":
                    logName = "/hskj/logs/cmpp_info.log."+startTime
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                elif search2 == "sgip":
                    logName = "/hskj/logs/sgip_info.log."+startTime
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
                else:
                    logName = "/hskj/logs/info.log."+startTime
                    command = "grep -a '"+user_id+"' "+logName+" | grep -a 'submitResp' | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
                    cmd = "awk '{a[$3]+=$1}END{for(i in a){print a[i]\" \"$2\" \"i}}' " + file +" | sort -k2 -r"
        if type == "cluster_64":
            server_list = {"c1_56":["210.14.134.81",10056],"c1_57":["210.14.134.81",10057],"c1_58":["210.14.134.81",10058]}
        elif type == "cluster_227":
            server_list = {"c2_24":["202.108.253.227",10024],"c2_25":["202.108.253.227",10025],"c2_33":["202.108.253.227",10033],"c2_34":["202.108.253.227",10034]}
        elif type == "cluster_35":
            server_list = {"c3_61":["36.110.168.35",10061],"c3_62":["36.110.168.35",10062],"c3_63":["36.110.168.35",10063]}
        else:
           server_list = {"c4_61":["111.13.124.226",10061],"c4_62":["111.13.124.226",10062],"c4_63":["111.13.124.226",10063]}

        f = open(file, 'a')
        for line in server_list.values():
                server = line[0]
                port = line[1]
                username = 'bjywb'
                pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
                s = paramiko.SSHClient()
                s.load_system_host_keys()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                key = paramiko.RSAKey.from_private_key_file(pkey_file,"&U*I(O1208")
                s.connect(server,port,username,pkey=key,timeout=10)
                stdin,stdout,stderr = s.exec_command(command)
                for result in stdout.readlines():
                    f.write(result)
        f.close()
        print (cmd)
        table_list  = []
        for result in os.popen(cmd).readlines():
            table_list.append({"content":result})
        return render_to_response("ClusterSpeed.html",locals())
    else:
        return render_to_response("ClusterSpeed.html",locals())

def usepro(req):
    return render_to_response("usepro.html",locals())

def request_ip(req):
    if req.method == 'POST':
        type = req.REQUEST.get('type','cluster_64')
        pro = req.REQUEST.get('pro','http')
        user_id = req.REQUEST.get('user_id','')
        if pro == 'http':
            command="grep -a '"+user_id+"' /hskj/logs/httpPostLog.log |awk -F[\;:]+ '{print $6}'|sort|uniq"
        elif pro == 'cmpp':
            command="grep -a '"+user_id+"' /hskj/logs/cmpp_info.log |grep -a 'submitResp'|awk -F[' ':]+ '{print $(NF-3)}'|sort|uniq"
        elif pro == 'sgip':
            command="grep -a '"+user_id+"' /hskj/logs/sgip_info.log |grep -a 'return_code'|awk  '{print $9}'|sort|uniq"
        else:
            command="grep -a '"+user_id+"' /hskj/logs/smgp_info.log |grep -a 'return_code'|awk  '{print $9}'|sort|uniq"
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
                        table_list.append({'server':server_ip,'content':result})
        return render_to_response("request_ip.html",locals())
    else:
        return render_to_response('request_ip.html',locals())

def td_speed(req):
    if req.method == 'POST':
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        td_code = req.REQUEST.get('td_code','0')
        ##search2 = req.REQUEST.get('search2','0')
        hour = req.REQUEST.get('hour','')
        type = req.REQUEST.get('type','cluster_local')
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        nowDate = time.strftime('%Y-%m-%d')
        logName_http=""
        logName_cmpp=""
        if startTime == "":
            startTime = nowDate
            logName_http = "/hskj/logs/info.log"
            logName_cmpp = "/hskj/logs/cmpp_info.log"
            logName_sgip = "/hskj/logs/sgip_info.log"
            logName_smgp = "/hskj/logs/smgp_info.log"
        else:
            if startTime == nowDate:
                logName_http = "/hskj/logs/info.log"
                logName_cmpp = "/hskj/logs/cmpp_info.log"
                logName_sgip = "/hskj/logs/sgip_info.log"
                logName_smgp = "/hskj/logs/smgp_info.log"
            else:
                logName_http = "/hskj/logs/info.log."+startTime
                logName_cmpp = "/hskj/logs/cmpp_info.log."+startTime
                logName_sgip = "/hskj/logs/sgip_info.log."+startTime
                logName_smgp = "/hskj/logs/smgp_info.log."+startTime
        ##command = "grep -a  '"+search1+"' "+logName_http+" "+logName_cmpp+" "+logName_sgip+" "+logName_smgp+"|grep -a '"+startTime+" "+hour+"' | grep -a '"+search2+"'|grep -v -a '\-\-'|grep -v 'send test'|grep -v 'receive test'|grep -v 'report'"
        command = "for i in {"+logName_http+","+logName_cmpp+","+logName_sgip+","+logName_smgp+"};do tail -10000 $i;done | grep -a 'yw_code: "+td_code+"' |grep -a '"+startTime+" "+hour+"'| grep -a \"waitSubmitRespMap\" | awk -F \",\" '{print $1}' | sort | uniq -c|sort -k1 -nr | head -20 "
        username = 'root'
        pkey_file='/root/.ssh/id_rsa'
        table_list = []
        server_list ={}
        if type == "cluster_local":
            server_list = {"c6_1":["192.168.81.203",22,"c6_1"],"c6_2":["192.168.81.203",23,"c6_2"]}
            for line in server_list.values():
                    sender_code=line[2]   
                    server = line[0]
                    port = line[1]
                    if port == 22:
                        server_ip = "192.168.81.203"
                    if port == 23:
                        server_ip = "192.168.81.203"
                    s = paramiko.SSHClient()
                    s.load_system_host_keys()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    key = paramiko.RSAKey.from_private_key_file(pkey_file,'666666')
                    s.connect(server,22,username,pkey=key,timeout=10)
                    stdin,stdout,stderr = s.exec_command(command)
                    for result in stdout.readlines():
                        ##result=re.sub(td_code,'<strong style="color:red;">'+td_code+'</strong>',result)
                        result=re.sub(td_code,'',result)
                        ##if search2 != "":
                        ##    result=re.sub(search2,''+search2+'',result)
                        result=re.sub('return','',result)
                        table_list.append({'server':server_ip,'content':result,'sender':sender_code})
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response("td_speed.html",locals())
    else:
        return render_to_response("td_speed.html",locals())
