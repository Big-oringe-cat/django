from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views

   
def insert(req):

    operatorName=req.session.get('username')
    
    monitor_type=req.REQUEST.get('monitor_type','0')
    command=req.REQUEST.get('monitor_command','0')
    monitor_command1=command.replace('\\','\\\\')
    monitor_command=monitor_command1.replace('\'','\\\'')
    warning_content=req.REQUEST.get('warning_content','0')
    expect=req.REQUEST.get('expect_result','0')
    expect_result=expect.replace('\\','\\\\')
    print(expect)
    comment=req.REQUEST.get('comment','0')
    monitor_level=req.REQUEST.get('monitor_level','0')
    alarm_count=req.REQUEST.get('alarm_count','0')
    alarm_frequency=req.REQUEST.get('alarm_frequency','0')
    startTime=req.REQUEST.get('startTime','08:00')
    endTime=req.REQUEST.get('endTime','21:00')
    alarm_time=startTime+'-'+endTime
    deal_way=req.REQUEST.get('deal_way',"")
    sensitivity=req.REQUEST.get('sensitivity',1)
    
    if(monitor_type=='0'):
        if req.method == 'POST':
                sql="insert into monitor_info(monitor_command,warning_content,comment,expect_result,monitor_type,monitor_level,alarm_count,alarm_frequency,alarm_time,deal_way,sensitivity) values ('"+monitor_command+"','" + warning_content +"','"+comment+"','"+expect_result+"','"+monitor_type+"','"+monitor_level+"','"+alarm_count+"','"+alarm_frequency+"','"+alarm_time+"','"+deal_way+"',"+sensitivity+")"
                print(sql)
                try:
                    conn,cur=ShareMethod.views.connDB()
                    result=ShareMethod.views.exeInsert(cur,sql)
                    ShareMethod.views.connClose(conn,cur) 
                except Exception as e:
                    ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/insert.do?monitor_type=0')
                ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                req.session['sql'] = command 
                return HttpResponseRedirect('ServerConfig.do?monitor_type=0')
        else:
            sql="select comment from comment_list where monitor_type=0" 
            conn,cur=ShareMethod.views.connDB()  
            ShareMethod.views.exeQuery(cur,sql)
            commentList=[]
            for row in cur:
                commentList.append({'comment':row[0]})
            return render_to_response('MIinsert_sql.html',{'commentList':commentList})
        
    if(monitor_type=='1'):
        if req.method == 'POST':
                sql="insert into monitor_info(monitor_command,warning_content,comment,expect_result,monitor_type,monitor_level,alarm_count,alarm_frequency,alarm_time,deal_way,sensitivity) values ('"+monitor_command+"','" + warning_content +"','"+comment+"','"+expect_result+"','"+monitor_type+"','"+monitor_level+"','"+alarm_count+"','"+alarm_frequency+"','"+alarm_time+"','"+deal_way+"',"+sensitivity+")"
                print(sql)
                try:
                    conn,cur=ShareMethod.views.connDB()
                    ShareMethod.views.exeInsert(cur,sql)
                    ShareMethod.views.connClose(conn,cur)
                except Exception as e:
                    ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/insert.do?monitor_type=1')
                ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                req.session['linux'] = command 
                return HttpResponseRedirect('ServerConfig.do?monitor_type=1')
        else:
            sql="select comment from comment_list where monitor_type=1" 
            conn,cur=ShareMethod.views.connDB()  
            ShareMethod.views.exeQuery(cur,sql)
            commentList=[]
            for row in cur:
                commentList.append({'comment':row[0]})
            return render_to_response('MIinsert_linux.html',{'commentList':commentList})
 
def update(req):
    id=req.REQUEST.get('id',0)
    monitor_type=req.REQUEST.get('monitor_type','0')
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from monitor_info where sn="+id)
    sql="select comment from comment_list where monitor_type='" +monitor_type+"'"
    conn1,cur1=ShareMethod.views.connDB()  
    ShareMethod.views.exeQuery(cur1,sql)
    ShareMethod.views.connClose(conn,cur) 
    ShareMethod.views.connClose(conn1,cur1) 
    commentList=[]
    for row in cur1:
        commentList.append({'comment':row[0]})
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_command':row[1],'warning_content':row[2],'comment':row[3],'monitor_type':row[4],'expect_result':row[5],'monitor_level':str(row[6]),'alarm_count':row[7],'alarm_frequency':row[8],'alarm_time':row[9],'deal_way':row[10],'sensitivity':row[11]})
    print(table_list)
    if(monitor_type=='0'):
        return render_to_response('MIedit_sql.html',{'table_list':table_list,'commentList':commentList})
        #return render_to_response('aa.html',locals())
    if(monitor_type=='1'):
        return render_to_response('MIedit_linux.html',{'table_list':table_list,'commentList':commentList})
        
    

def modify(req):
    id=req.REQUEST.get('id',0)
    operatorName=req.session.get('username')
    monitor_type=req.REQUEST.get('monitor_type','0')
    command=req.REQUEST.get('monitor_command','0')
    monitor_command1=command.replace('\\','\\\\')
    monitor_command=monitor_command1.replace('\'','\\\'')
    warning_content=req.REQUEST.get('warning_content','0')
    expect=req.REQUEST.get('expect_result','0')
    expect_result=expect.replace('\\','\\\\')
    print(expect_result)
    comment=req.REQUEST.get('comment','0')
    monitor_level=req.REQUEST.get('monitor_level','0')
    alarm_count=req.REQUEST.get('alarm_count','0')
    alarm_frequency=req.REQUEST.get('alarm_frequency','0')
    alarm_time=req.REQUEST.get('alarm_time','')
    deal_way=req.REQUEST.get('deal_way','')
    deal_way=deal_way.replace('\"','\\\"')
    deal_way=deal_way.replace("\'","\\\'")
    sensitivity=req.REQUEST.get('sensitivity',1)
    sql="update monitor_info set monitor_command='"+monitor_command+"',warning_content='"+warning_content+"',comment='"+comment+"',monitor_type='"+monitor_type+"',expect_result='"+expect_result+"',monitor_level='"+monitor_level+"',alarm_count='"+alarm_count+"',alarm_frequency='"+alarm_frequency+"',alarm_time='"+alarm_time+"',deal_way='"+deal_way+"',sensitivity="+sensitivity+" where sn="+str(id)
    print(sql)
    if(monitor_type=='0'):
            try:
                conn,cur=ShareMethod.views.connDB()
                result=ShareMethod.views.exeUpdate(cur,sql)
                ShareMethod.views.connClose(conn,cur) 
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=0')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=0')
    if(monitor_type=='1'):
            try:
                conn,cur=ShareMethod.views.connDB()
                ShareMethod.views.exeUpdate(cur,sql)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=1')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=1')
        
def delete(req): 
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    sql="delete from monitor_info where sn="+id
    print(sql)
    ShareMethod.views.exeDelete(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('MImessage.html',{'message':"删除成功"})

def select(req):
    role = req.session.get('role','')
    username = req.session.get('username','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    monitor_type=req.REQUEST.get('monitor_type','0')
    print(search)
    print(value)
    sql= "select * from monitor_info where 1 =1 and monitor_type='"+monitor_type+"'"
    sql2 = "select count(*) as count from monitor_info where monitor_type='"+monitor_type+"'"
    if(search=='monitor_sn'):
        sql += " and sn like '%" + value + "%'"
        sql2 += " and sn like '%" + value + "%'"
    if(search=='monitor_command'):
        sql += " and monitor_command like '%" + value + "%'"
        sql2 += " and monitor_command like '%" + value + "%'"
    if(search=='warning_content'):
        sql += " and warning_content like '%" + value + "%'"
        sql2 += " and warning_content like '%" + value + "%'"
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='alarm_type'):
        sql += " and monitor_level like '%" + value + "%'"
        sql2 += " and monitor_level like '%" + value + "%'"
    if(search=='expect_result'):
        sql += " and expect_result like '%" + value + "%'"
        sql2 += " and expect_result like '%" + value + "%'"    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_command':row[1],'warning_content':row[2],'comment':row[3],'monitor_type':row[4],'expect_result':row[5],'monitor_level':str(row[6]),'sensitivity':str(row[11])})
    if(monitor_type=='0'):
        return render_to_response('MIselect_sql.html',locals())
    else:
        return render_to_response('MIselect_linux.html',locals())
    
def ServerConfig(req):
    operatorName=req.session.get('username')
    sql_command=req.session.get('sql')
    linux_command=req.session.get('linux')
    monitor_type=req.REQUEST.get('monitor_type','0')
    
    value=int(req.REQUEST.get('value','0'))
    mark=req.REQUEST.get('mark','0')
    frequency=int(req.REQUEST.get('frequency','0'))
    status=int(req.REQUEST.get('status','0'))
    servers_SN=req.POST.getlist('serverName','0')
    groupSns=req.POST.getlist('groupName','0')
    group_all_check=req.POST.getlist('GroupName','0')
    print (group_all_check)
    id=req.REQUEST.get('id','0')
    add_group_sn=""
    if(monitor_type=='0'):
        if req.method == 'POST':
                delimiter = ','
                if groupSns != "" and groupSns != '0':
                    if group_all_check != "" and group_all_check != '0' and group_all_check != 0:
                        add_group_sn=delimiter.join(group_all_check)
                else:
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=0')
                print("add_group_sn:"+add_group_sn)    
                print(groupSns)
                sn=req.REQUEST.get('sn','0')
                sql_sn="select sn from monitor_info where monitor_type=0 order by sn desc limit 1"
                try:
                    sql=""
                    conn,cur=ShareMethod.views.connDB()
                    ShareMethod.views.exeQuery(cur,sql_sn) 
                    if(id=='0'):
                        for row in cur:
                            monitor_sn=row[0]
                    else:
                        monitor_sn=id
                    print(monitor_sn)
                    for group_sn in groupSns:
                        serverSns=req.POST.getlist('serverName_'+str(group_sn),'0')
                        print(serverSns)
                        if(serverSns != '0'): 
                            for server_sn in serverSns:
                                sql="insert into server_monitor_info(server_sn,monitor_sn,value,mark,frequency,status,group_sn,add_group_sn) values ("+str(server_sn)+"," + str(monitor_sn) +","+str(value)+",'"+mark+"',"+str(frequency)+","+str(status)+",'"+group_sn+"','"+add_group_sn+"')"
                                print(sql)
                                ShareMethod.views.exeInsert(cur,sql)
                    ShareMethod.views.connClose(conn,cur) 
                except Exception as e:
                    print(e)
                    ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/ServerConfig.do?monitor_type=0')
                ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=0')
        else:
            conn1,cur1=ShareMethod.views.connDB()
            conn2,cur2=ShareMethod.views.connDB() 
            conn3,cur3=ShareMethod.views.connDB() 
            conn4,cur4=ShareMethod.views.connDB() 
            conn5,cur5=ShareMethod.views.connDB() 
            conn6,cur6 = ShareMethod.views.connDB()
            conn7,cur7 = ShareMethod.views.connDB()
            sql6 = "select group_name,sn from user_group"
            ShareMethod.views.exeQuery(cur6,sql6)
            ShareMethod.views.connClose(conn6,cur6)
            GroupNames=[]
            for row in cur6:
                GroupNames.append({'groupName':row[0],'groupSn':str(row[1]),'groupSnCmp':","+str(row[1])+","})
            print(GroupNames)
            sql1="select group_sn,server_sn from server_manager"  
            sql4="select monitor_command from monitor_info where sn="+str(id) 
            sql5="select value,mark,frequency,server_sn from server_monitor_info where monitor_sn="+str(id)+" limit 1"
            print(sql5)
            ShareMethod.views.exeQuery(cur4,sql4)
            ShareMethod.views.exeQuery(cur5,sql5)
            monitor_command=""
            config=[]
            for row4 in cur4:
                monitor_command=row4[0]
            for row5 in cur5:
                config.append({'value':row5[0],'mark':row5[1],'frequency':row5[2]})
            print(config)
            sql7='select server_sn from server_monitor_info where monitor_sn='+str(id)
            server_sn5=[]
            ShareMethod.views.exeQuery(cur7,sql7)
            for row7 in cur7:
                server_sn5.append(str(row7[0]))
            ShareMethod.views.connClose(conn7,cur7)
            ShareMethod.views.exeQuery(cur1,sql1)
            servers=[]
            serverNames=[]
            serverManagers=[]
            groupNames=[]
            for row1 in cur1:
                serverNames=[]
                groupNames=[]
                sql2="select group_name from user_group where sn="+str(row1[0])
                ShareMethod.views.exeQuery(cur2,sql2)
                for row2 in cur2:
                    groupNames.append({'groupName':row2[0],'groupSn':row1[0]})
                servers=row1[1].split(',')
                for server_sn in servers:
                    sql3="select server_name from server_info where sn="+str(server_sn)
                    ShareMethod.views.exeQuery(cur3,sql3)
                    for row3 in cur3:
                        serverNames.append({'serverName':row3[0],'serverSn':server_sn})

                serverManagers.append({'groupNames':groupNames,'serverNames':serverNames})
            ShareMethod.views.connClose(conn1,cur1)
            ShareMethod.views.connClose(conn2,cur2)
            ShareMethod.views.connClose(conn3,cur3)
            ShareMethod.views.connClose(conn4,cur4)
            ShareMethod.views.connClose(conn5,cur5)
            
            print(serverManagers)
            conn8,cur8 = ShareMethod.views.connDB() 

            if(id == "0"):
                return render_to_response('ServerConfig_sql.html',{'serverManagers':serverManagers,'sql_command':sql_command,'id':0,'GroupNames':GroupNames})
            else:
                return render_to_response('ServerConfig_sql.html',{'serverManagers':serverManagers,'sql_command':monitor_command,'id':id,'config':config,'GroupNames':GroupNames,'server_sn5':server_sn5})
    if(monitor_type == '1'):
        if req.method == 'POST':
                delimiter = ','
                if groupSns != "" and groupSns != '0':
                    if group_all_check != "" and group_all_check != '0' and group_all_check != 0:
                        add_group_sn=delimiter.join(group_all_check)
                else:
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=1')
                print("add_group_sn:"+add_group_sn)    
                print(groupSns)
                id=req.REQUEST.get('id','0')
                sql_sn="select sn from monitor_info where monitor_type=1 order by sn desc limit 1"
                try:
                    sql=""
                    conn,cur=ShareMethod.views.connDB()
                    ShareMethod.views.exeQuery(cur,sql_sn) 
                    if(id=='0'):
                        for row in cur:
                            monitor_sn=row[0]
                    else:
                        monitor_sn=id
                    print(monitor_sn)
                    for group_sn in groupSns:
                        serverSns=req.POST.getlist('serverName_'+str(group_sn),'0')
                        print(serverSns)
                        if(serverSns != '0'): 
                            for server_sn in serverSns:
                                sql="insert into server_monitor_info(server_sn,monitor_sn,frequency,status,group_sn,add_group_sn) values ("+str(server_sn)+"," + str(monitor_sn) +","+str(frequency)+","+str(status)+",'"+group_sn+"','"+add_group_sn+"')"
                                print(sql)
                                ShareMethod.views.exeInsert(cur,sql)
                    ShareMethod.views.connClose(conn,cur) 
                except Exception as e:
                    print(e)
                    ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                    return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/ServerConfig.do?monitor_type=1')
                ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=1')
        else:
            conn1,cur1=ShareMethod.views.connDB()
            conn2,cur2=ShareMethod.views.connDB() 
            conn3,cur3=ShareMethod.views.connDB() 
            conn4,cur4=ShareMethod.views.connDB() 
            conn5,cur5=ShareMethod.views.connDB() 
            conn6, cur6 = ShareMethod.views.connDB()
            conn7,cur7=ShareMethod.views.connDB() 
            sql6 = "select group_name,sn from user_group"
            ShareMethod.views.exeQuery(cur6,sql6)
            ShareMethod.views.connClose(conn6,cur6)
            GroupNames=[]
            for row in cur6:
                GroupNames.append({'groupName':row[0],'groupSn':str(row[1]),'groupSnCmp':","+str(row[1])+","})
            print(GroupNames)
            sql1="select group_sn,server_sn from server_manager"  
            
            sql4="select monitor_command from monitor_info where sn="+str(id) 
            sql5="select frequency,status,server_sn,add_group_sn from server_monitor_info where monitor_sn="+str(id)+" limit 1"

            ShareMethod.views.exeQuery(cur4,sql4)
            ShareMethod.views.exeQuery(cur5,sql5)
            monitor_command=""
            config=[]
            for row4 in cur4:
                monitor_command=row4[0]

            for row5 in cur5:
                config.append({'frequency':row5[0],'status':row5[1],'server_sn':row5[2],'add_group_sn':row5[3]})
            print(config)    
            ShareMethod.views.exeQuery(cur1,sql1)
            sql7='select server_sn from server_monitor_info where monitor_sn='+str(id)
            server_sn5=[]
            ShareMethod.views.exeQuery(cur7,sql7)
            for row7 in cur7:
                server_sn5.append(str(row7[0]))
            ShareMethod.views.connClose(conn7,cur7)
            servers=[]
            serverNames=[]
            serverManagers=[]
            groupNames=[]
            for row1 in cur1:
                serverNames=[]
                groupNames=[]
                sql2="select group_name from user_group where sn="+str(row1[0])
                ShareMethod.views.exeQuery(cur2,sql2)
                for row2 in cur2:
                    groupNames.append({'groupName':row2[0],'groupSn':row1[0]})
                servers=row1[1].split(',')
                for server_sn in servers:
                    sql3="select server_name from server_info where sn="+str(server_sn)
                    ShareMethod.views.exeQuery(cur3,sql3)
                    for row3 in cur3:
                        serverNames.append({'serverName':row3[0],'serverSn':server_sn})

                serverManagers.append({'groupNames':groupNames,'serverNames':serverNames})
            ShareMethod.views.connClose(conn1,cur1)
            ShareMethod.views.connClose(conn2,cur2)
            ShareMethod.views.connClose(conn3,cur3)
            ShareMethod.views.connClose(conn4,cur4)
            ShareMethod.views.connClose(conn5,cur5)
            
            print(serverManagers)
            
            if(id=="0"):
                return render_to_response('ServerConfig_linux.html',{'serverManagers':serverManagers,'linux_command':linux_command,'id':0,'GroupNames':GroupNames})
            else:
                return render_to_response('ServerConfig_linux.html',{'serverManagers':serverManagers,'linux_command':monitor_command,'id':id,'config':config,'GroupNames':GroupNames,'server_sn5':str(server_sn5)})


def panduan(req):
        id=req.REQUEST.get('id',0)
        monitor_type=req.REQUEST.get('monitor_type',0)
        conn,cur=ShareMethod.views.connDB()
        conn1,cur1=ShareMethod.views.connDB()

        sql6="select monitor_command from monitor_info where sn="+str(id)
        conn6,cur6=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur6,sql6)
        ShareMethod.views.connClose(conn6,cur6)
        monitor_command=""
        for row6 in cur6:        
            monitor_command=row6[0]

        conn3,cur3=ShareMethod.views.connDB()
        sql3="select value,mark,frequency from server_monitor_info where monitor_sn="+str(id)+" limit 1"
        ShareMethod.views.exeQuery(cur3,sql3)
        ShareMethod.views.connClose(conn3,cur3)
        config=[]
        for row3 in cur3:
            config.append({'value':row3[0],'mark':row3[1],'frequency':row3[2]})
        sql="select server_sn from server_monitor_info where monitor_sn="+str(id)+" limit 1"
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        a=""
        for row in cur:
            a=row[0]
        conn2,cur2=ShareMethod.views.connDB()
        sql2="select server_sn from server_monitor_info where monitor_sn="+str(id)
        ShareMethod.views.exeQuery(cur2,sql2)
        ShareMethod.views.connClose(conn2,cur2)
        if a:
            servers=[]
            server_Name=[]
            for row2 in cur2:
                sql1="select server_name from server_info where sn="+str(row2[0])
                ShareMethod.views.exeQuery(cur1,sql1)
                for row1 in cur1:
                    servers.append({"server_Name":row1[0],'server_sn':row2[0]})
            return render_to_response('panduan1.html',locals())
        else:
            if(monitor_type=='0'):
                return HttpResponseRedirect('ServerConfig?monitor_type=0&id='+id)
            else:
                return HttpResponseRedirect('ServerConfig?monitor_type=1&id='+id)

def updatenew(req):
    id=req.REQUEST.get('id',0)
    monitor_type=req.REQUEST.get('monitor_type',0)
    server_id=req.REQUEST.get('server_id',0)
    if server_id != 0:
        conn,cur=ShareMethod.views.connDB()
        conn1,cur1=ShareMethod.views.connDB()
        conn2,cur2=ShareMethod.views.connDB()
        conn3,cur3=ShareMethod.views.connDB()
        sql3="select b.group_name,a.group_sn from server_manager a,user_group b where a.group_sn=b.sn"
        ShareMethod.views.exeQuery(cur3,sql3)
        user_name=[]
        for row3 in cur3:
            user_name.append({'user_name':row3[0],'user_sn':str(row3[1])})
        ShareMethod.views.connClose(conn3,cur3)
        sql = "select group_name,sn from user_group"
        ShareMethod.views.exeQuery(cur,sql)
        GroupNames=[]
        for row in cur:
            GroupNames.append({'groupName':row[0],'groupSn':str(row[1]),'groupSnCmp':","+str(row[1])+","})
        sql1="select value,mark,frequency,add_group_sn,group_sn,status from server_monitor_info where monitor_sn="+str(id)+" and server_sn="+str(server_id)
        ShareMethod.views.exeQuery(cur1,sql1)
        config=[]
        for row1 in cur1:
            config.append({'value':row1[0],'mark':row1[1],'frequency':row1[2],'add_group_sn':","+str(row1[3])+",",'group_sn':str(row1[4]),'status':row1[5]})
        sql2="select monitor_command from monitor_info where sn="+str(id)
        ShareMethod.views.exeQuery(cur2,sql2)
        sql_command=""
        for row2 in cur2:
            sql_command=row2[0]
        ShareMethod.views.connClose(conn,cur)
        ShareMethod.views.connClose(conn1,cur1)
        ShareMethod.views.connClose(conn2,cur2)
        return render_to_response('ServerConfig_new.html',locals())
    else:
         return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do')

def sqlxiugai(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    monitor_type=req.REQUEST.get('monitor_type',0)
    server_id=req.REQUEST.get('server_id',0)
    value=req.REQUEST.get('value',0)
    mark=req.REQUEST.get('mark',0)
    group_sn=req.REQUEST.get('group_sn',0)
    status=req.REQUEST.get('status',0)
    frequency=req.REQUEST.get('frequency',0)
    add_group_sn=req.POST.getlist('GroupName',0)
    delimiter = ','
    if add_group_sn != 0:
        add_group_sn=delimiter.join(add_group_sn)
    conn,cur=ShareMethod.views.connDB()
    try:
        sql="update server_monitor_info set add_group_sn='"+str(add_group_sn)+"',group_sn="+group_sn+",value="+str(value)+",mark='"+str(mark)+"',frequency="+str(frequency)+",status="+str(status)+" where monitor_sn=" + str(id)+" and server_sn="+str(server_id)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do')
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do')

def piliang(req):
        id=req.REQUEST.get('id',0)
        monitor_type=req.REQUEST.get('monitor_type',0)
        value=int(req.REQUEST.get('value','0'))
        mark=req.REQUEST.get('mark','>')
        frequency=req.REQUEST.get('frequency','0')
        try:
            conn,cur=ShareMethod.views.connDB()
            sql="update server_monitor_info set value="+str(value)+",mark='"+str(mark)+"',frequency="+str(frequency)+" where monitor_sn="+str(id)
            ShareMethod.views.exeUpdate(cur,sql)
            ShareMethod.views.connClose(conn,cur)
        except Exception as e:
            print(e)
            if monitor_type == 0:
               return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=0')
            else:
               return HttpResponseRedirect('../FailureMessage.do?message=MonitorInfo/select.do?monitor_type=1')
        if monitor_type == '0':
           return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=0')
        elif monitor_type == '1':
           return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do?monitor_type=1')

            
 
def deal(req):
    id=req.REQUEST.get('id',0)
    deal_way=req.REQUEST.get('deal_way',"")
    deal_way=deal_way.replace('\"','\\\"')
    if req.method == 'POST':
        sql1='update monitor_info set deal_way="'+deal_way+'" where sn='+id
        conn1,cur1=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur1,sql1)
        ShareMethod.views.connClose(conn1,cur1)
        return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do')
        #return render_to_response('abc.html',locals())
    else:
        sql='select monitor_command,deal_way from monitor_info where sn='+str(id)
        conn,cur=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        table_list=[]
        for row in cur:
            table_list.append({'monitor_command':row[0],'deal_way':row[1]})
        return render_to_response('deal_way.html',locals())

def add_group(req):
    id=req.REQUEST.get('id')
    if req.method == 'POST':
        add_group_sn=req.POST.getlist('GroupName',0)
        delimiter = ','
        if add_group_sn != 0:
            add_group_sn=delimiter.join(add_group_sn)
        sql3='update server_monitor_info set add_group_sn="'+add_group_sn+'" where monitor_sn='+str(id)
        conn3,cur3=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur3,sql3)
        ShareMethod.views.connClose(conn3,cur3)
        return HttpResponseRedirect('../SuccessMessage.do?message=MonitorInfo/select.do')
    else:
        sql="select add_group_sn from server_monitor_info where monitor_sn="+str(id)+" limit 1"
        conn,cur=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        add_group_sn=[]
        for row in cur:
            add_group_sn=row[0].split(',')
        conn1,cur1=ShareMethod.views.connDB()
        sql1 = "select group_name,sn from user_group"
        ShareMethod.views.exeQuery(cur1,sql1)
        GroupNames=[]
        for row1 in cur1:
            GroupNames.append({'groupName':row1[0],'groupSn':str(row1[1])})
        conn2,cur2=ShareMethod.views.connDB()
        sql2="select monitor_command from monitor_info  where sn="+str(id)
        ShareMethod.views.exeQuery(cur2,sql2)
        monitor_command=""
        for row2 in cur2:
            monitor_command=row2[0]
        ShareMethod.views.connClose(conn2,cur2)
        return render_to_response('add_group.html',locals())
        
