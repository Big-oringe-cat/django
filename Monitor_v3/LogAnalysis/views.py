from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os,sys
import paramiko
import pymysql
import re

def GateLog(req,command,html,server,port):
    if req.method == 'POST':
        operatorName=req.session.get('username')
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        startTime = req.REQUEST.get('startTime','0')
        server = req.REQUEST.get('server','0')
        user_sp_number = req.REQUEST.get('user_sp_number','0')
        td_code = req.REQUEST.get('td_code','0')
        search = req.REQUEST.get('search','0')
        ##username = 'bjywb'
        username = 'root'
        ##pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        pkey_file='/root/.ssh/id_rsa'
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        key = paramiko.RSAKey.from_private_key_file(pkey_file,"666666")
        s.connect(server,port,username,pkey=key,timeout=10)
        stdin,stdout,stderr = s.exec_command(command)
        #cmd_result = stdout.read(),stderr.read()
        table_list = []
        for result in stdout.readlines():
            result=re.sub(search1,'<strong style="color:red;">'+search1+'</strong>',result)
            if search2 != "":
                result=re.sub(search2,'<strong style="color:red;">'+search2+'</strong>',result)
            result=re.sub('return','<strong style="color:red;">return</strong>',result)
            table_list.append({'content':result.strip("\n")})
        s.close()
        server_list = select_server()
        serverName=''
        for serverlist in server_list:
            if serverlist.get("ip") == server:
                serverName = serverlist.get("server_name")
        if 'cmpp' in serverName:
            dbname = "cluster_server"
        if 'smgp' in serverName:
            dbname = "smgp_server_new"
        if 'sgip' in serverName:
            dbname = "sgip_server"
        tdSpeed = select_tdSpeed(td_code,server,dbname)
        ShareMethod.views.InfoLog(command+"操作人："+operatorName)
        return render_to_response(html,locals())
    else:
        server_list = select_server()
        print(server_list)
        return render_to_response(html,locals())
    
def customerSubmit(req):
    session_tmp = req.session
    for key, value in session_tmp.items():
        print ("log_server.session----------->"+key + ' : ' + str(value))
    print("session_key_log_server:")
    print(req.session.session_key)
    operatorName=req.session.get('login_username')
    search1 = req.REQUEST.get('search1','0')
    search2 = req.REQUEST.get('search2','0')
    hour = req.REQUEST.get('hour','')
    nowDate = time.strftime('%Y-%m-%d')
    startTime = req.REQUEST.get('startTime',nowDate)
    server = req.REQUEST.get('server','0')
    print("server="+server)
    html = "CustomerSubmit.html"
    port = 22
    if server == '218.207.183.118':
        port = 10023
    if server == '61.147.118.16':
        port = 10002
    if server == '115.85.192.72':
        port = 10022
    nowDate = time.strftime('%Y-%m-%d')
    if startTime == "":
        startTime = nowDate
        logName = "/hskj/logs/gate/receiver.txt"
    if startTime == nowDate:
        logName = "/hskj/logs/gate/receiver.txt"
    else:
        logName = "/hskj/logs/gate/receiver.txt."+startTime
        
    command = "grep -a -A1 '"+search1+"' "+logName+" | grep -a '"+startTime+" "+hour+"'|grep -a '"+search2+"'|grep -v -a '\-\-'"
    print("command="+command)
    return GateLog(req,command,html,server,port)

def customerSpeed(req):
    operatorName=req.session.get('username')
    user_sp_number = req.REQUEST.get('user_sp_number','0').strip()
    print(user_sp_number)
    search = req.REQUEST.get('search','0')
    nowDate = time.strftime('%Y-%m-%d')
    startTime = req.REQUEST.get('startTime',nowDate)
    server = req.REQUEST.get('server','0')
    print(server)   
    html = "CustomerSpeed.html"
    port = 22
    if server == '218.207.183.118':
        port = 10023
    if server == '61.147.118.16':
        port = 10002
    if server == '115.85.192.72':
        port = 10022
    if startTime == "":
        startTime = nowDate
    if search == "nowtype":
        logName = "/hskj/logs/gate/receiver.txt"
        print ("logName="+logName)
        command = "tail -100000 "+logName+" | grep -a '"+user_sp_number+"' | awk -F \",\" '{print $1}' | sort | uniq -c"
        print(command)
    else:
        if startTime == nowDate:
            logName = "/hskj/logs/gate/receiver.txt"
            command = "grep -a '"+user_sp_number+"' "+logName+" | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
            print(command)
        else:
            logName = "/hskj/logs/gate/receiver.txt."+startTime
            print ("logName="+logName)
            command = "grep -a '"+user_sp_number+"' "+logName+" | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
            print(command)
        
    return GateLog(req,command,html,server,port)

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
            
        

    
def tdSend(req):
    operatorName=req.session.get('username')
    td_code = req.REQUEST.get('td_code','0').strip()
    search = req.REQUEST.get('search','0')
    hour = req.REQUEST.get('hour','')
    nowDate = time.strftime('%Y-%m-%d')
    startTime = req.REQUEST.get('startTime',nowDate)
    server = req.REQUEST.get('server','0')
    print(server)
    html = "TdSend.html"
    port = 22
    if server == '218.207.183.118':
        port = 10023
    if server == '61.147.118.16':
        port = 10002
    if server == '115.85.192.72':
        port = 10022
    if startTime == "":
        startTime = nowDate
    if search == "nowtype":
        logName = "/hskj/logs/send/info.log"
        print ("logName="+logName)
        command = "tail -100000 "+logName+" | grep -a 'yw_code:"+td_code+"' |grep -a '"+nowDate+" "+hour+"'| grep -a \"waitSubmitRespMap\" | awk -F \",\" '{print $1}' | sort | uniq -c " 
        print(command)
    else:
        if startTime == nowDate:
            logName = "/hskj/logs/send/info.log"
            command = "grep -a 'yw_code:"+td_code+"' "+logName+" |grep -a \"waitSubmitRespMap\" | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
            print(command)
        else:
            logName = "/hskj/logs/send/info.log."+startTime
            print ("logName="+logName)
            command = "grep -a 'yw_code:"+td_code+"' "+logName+" |grep -a \"waitSubmitRespMap\" | awk -F \",\" '{print $1}' | sort | uniq -c | sort -k1 -nr | head -20"
            print(command)
        
        
    return GateLog(req,command,html,server,port)

# def tdOverStock(req):
#     if req.method == 'POST':
#         port=3306
#         operatorName=req.session.get('username')
#         server = req.REQUEST.get('server','0')
#         server_list = select_server()
#         serverName = ''
#         dbname=''
#         for serverlist in server_list:
#             if serverlist.get("ip") == server:
#                 serverName = serverlist.get("server_name")
#         if 'cmpp' in serverName:
#             dbname = "cmpp_server"
#         if 'smgp' in serverName:
#             dbname = "smgp_server_new"
#         if 'sgip' in serverName:
#             dbname = "sgip_server"
#         sql = "select b.td_name as td_name,a.yw_code as yw_code,count(*) as file_count ,sum(a.mobile_count) as mobile_count from file_info_submit a,td_info b where b.td_code=a.yw_code and timestampdiff(second, a.create_time, now()) > 30 group by 1,2"
#         conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
#         ShareMethod.views.exeQuery(cur,sql)
#         table_list = []
#         for row in cur:
#             table_list.append({'td_name':row[0],'td_code':row[1],'file_count':row[2],'mobile_count':row[3]})
#         ShareMethod.views.connClose(conn,cur)
#         ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
#         return render_to_response('TdOverStock.html',locals())
#     else:
#         server_list = select_server()
#         return render_to_response('TdOverStock.html',locals())
        
    
def select_server():   
    server_list = [] 
    conn,cur=ShareMethod.views.connDB1()
    sql = "select server_ip,server_id from server_info where status=0 and (server_id like '%cmpp%' or server_id like '%sgip%' or server_id like '%smgp%')"
    print(sql)  
    ShareMethod.views.exeQuery(cur,sql)
    for row in cur:
        server_list.append({'ip':row[0],'server_name':row[1]})
    ShareMethod.views.connClose(conn,cur)
    return server_list  

def select_tdSpeed(td_code,server,dbname):
    tdSpeed = ''
    tdName = ''
    port=3306
    conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
    conn2,cur2=ShareMethod.views.connDB_yw(server,dbname,port)
    sql = "select substring_index(substring_index(thread_param,' ',9),' ',-2) as speed from thread_controller where group_id='"+td_code+"'"
    sql2 = "select td_name from td_info where td_code='"+td_code+"'"
    print(sql)
    print(sql2)
    ShareMethod.views.exeQuery(cur,sql)
    ShareMethod.views.exeQuery(cur2,sql2)
    for row in cur:
        tdSpeed = row[0]
    for row in cur2:
        tdName = row[0]
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn2,cur2)
    return tdSpeed,tdName
   
def net_switch_mobile(req):
    mobile=req.REQUEST.get('mobile',0)
    if req.method=='POST':
        conn=  pymysql.connect(host='111.13.124.226',port=3306,user='remote_query',passwd='20141024',db='super_plate',charset='utf8')
        cur = conn.cursor()
        sql="select * from net_switched_mobile where mobile="+str(mobile)
        cur.execute(sql)
        table_list=[]
        for row in cur:
            table_list.append({'mobile':row[1],'ori':str(row[2]),'dest':str(row[3])})
        return render_to_response('net_switch_mobile.html',locals())
    else:
        return render_to_response('net_switch_mobile.html')

def request_ip(req):
    if req.method == 'POST':
        server = req.REQUEST.get('server','')
        user_id = req.REQUEST.get('user_id','')
        port = 22
        if server == '218.207.183.118':
            port = 10023
        if server == '61.147.118.16':
            port = 10002
        if server == '115.85.192.72':
            port = 10022
        command="grep -a '"+user_id+"' /hskj/logs/gate/receiver.txt|grep -a 'submitResp'|awk -F [' ':]+ '{print $(NF-3)}'|sort|uniq"
        username = 'bjywb'
        pkey_file='/home/bjywb/.ssh/hskj_20130620_bjywb'
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(pkey_file,"&U*I(O1208")
        s.connect(server,port,username,pkey=key,timeout=10)
        stdin,stdout,stderr = s.exec_command(command)
        #cmd_result = stdout.read(),stderr.read()
        table_list = []
        for result in stdout.readlines():
            print(result)
            table_list.append({'content':result.strip("\n")})
        s.close()
        server_list = select_server()
        serverName=''
        for serverlist in server_list:
            if serverlist.get("ip") == server:
                serverName = serverlist.get("server_name")
        return render_to_response('request_ip1.html',locals())
    else:
        server_list = select_server()
        return render_to_response('request_ip1.html',locals())
