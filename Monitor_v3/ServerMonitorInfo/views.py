from django import forms
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

import ShareMethod.views
from tracemalloc import Snapshot
import time

def update(req):
    sn = req.REQUEST.get('sn', 0)
    print(sn)
    monitor_type=req.REQUEST.get('monitor_type','0')
    sql = "select a.sn,b.ip,c.monitor_command,a.value,a.mark,a.frequency,a.last_time,a.status,a.group_sn,a.add_group_sn from server_monitor_info a,server_info b ,monitor_info c where a.monitor_sn=c.sn and a.server_sn=b.sn and c.monitor_type='"+monitor_type+"' and a.sn="+str(sn)
    conn, cur = ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur, sql)
    ShareMethod.views.connClose(conn, cur)
    conn2, cur2 = ShareMethod.views.connDB()
    sql2 = "select group_name,sn from user_group"
    ShareMethod.views.exeQuery(cur2,sql2)
    ShareMethod.views.connClose(conn2,cur2)
    GroupNames=[]
    for row in cur2:
        GroupNames.append({'groupName':row[0],'groupSn':str(row[1]),'groupSnCmp':","+str(row[1])+","})
    print(GroupNames)
    conn4,cur4=ShareMethod.views.connDB()
    sql4="select b.group_name,a.group_sn from server_manager a,user_group b where a.group_sn=b.sn"
    ShareMethod.views.exeQuery(cur4,sql4)
    user_name=[]
    for row4 in cur4:
        user_name.append({'user_name':row4[0],'user_sn':str(row4[1])})
    ShareMethod.views.connClose(conn4,cur4)
    table_list = []
    for row in cur:
        table_list.append({'sn':row[0], 'ip':row[1], 'monitor_command':row[2], 'value':row[3], 'mark':row[4], 'frequency':row[5], 'last_time':row[6], 'status':row[7], 'group_sn':str(row[8]), 'add_group_sn':","+row[9]+","})
    print(table_list)
    print ("monitor_type=:%s"%monitor_type)
    if (monitor_type=='0'):
        return render_to_response('SMIedit_sql.html', {'table_list':table_list,'GroupNames':GroupNames,'user_name':user_name})
    if (monitor_type=='1'):
        return render_to_response('SMIedit_linux.html', {'table_list':table_list,'GroupNames':GroupNames,'user_name':user_name})
    

def modify(req):
    sn = req.REQUEST.get('sn', 0)
    operatorName = req.session.get('username', '0')
    monitor_type=req.REQUEST.get('monitor_type',0)
    value = req.REQUEST.get('value', 0)
    mark = req.REQUEST.get('mark', '>')
    frequency = req.REQUEST.get('frequency', 0)
    status = req.REQUEST.get('status', 0)
    group_sn = req.REQUEST.get('group_sn',0)
    group_all_check=req.POST.getlist('GroupName','0')
    delimiter = ','
    add_group_sn=delimiter.join(group_all_check)
    conn, cur = ShareMethod.views.connDB()
    sql = "update server_monitor_info set value=" + str(value) + ",mark='"+mark+"',frequency=" + str(frequency) + ",status=" + str(status) + ",group_sn  =" + group_sn +",add_group_sn  ='" + add_group_sn + "'  where sn=" + str(sn)
    print("modify_sql:%s " % sql)
    try:
        conn, cur = ShareMethod.views.connDB()
        result = ShareMethod.views.exeUpdate(cur, sql)
        ShareMethod.views.connClose(conn, cur) 
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e) + "操作人：" + operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ServerMonitorInfo/select.do?monitor_type='+str(monitor_type))
    ShareMethod.views.InfoLog(sql + "操作人：" + operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ServerMonitorInfo/select.do?monitor_type='+str(monitor_type))

def delete(req): 
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    monitor_type=req.REQUEST.get('monitor_type',0)
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="delete from server_monitor_info where sn="+sn
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ServerMonitorInfo/select.do?monitor_type='+str(monitor_type))
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ServerMonitorInfo/select.do?monitor_type='+str(monitor_type)) 

def select(req):
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))
    
    search = req.REQUEST.get('search', '0')
    value = req.REQUEST.get('value', '0')
    monitor_type=req.REQUEST.get('monitor_type','0')
    conn, cur = ShareMethod.views.connDB()
    sql = "select a.sn,b.ip,c.monitor_command,a.value,a.mark,a.frequency,a.last_time,a.status,a.group_sn,a.add_group_sn from server_monitor_info a,server_info b ,monitor_info c where a.monitor_sn=c.sn and a.server_sn=b.sn and c.monitor_type='"+monitor_type+"'"
    sql2 = "select count(*) as count from server_monitor_info a,server_info b ,monitor_info c where a.monitor_sn=c.sn and a.server_sn=b.sn and c.monitor_type='"+monitor_type+"'"
    if(search == 'ip'):
        sql += " and b.ip like '%" + value + "%'" 
        sql2 += " and b.ip like '%" + value + "%'" 
    if(search == 'monitor_command'):
        sql += " and c.monitor_command like '%" + value + "%'" 
        sql2 += " and c.monitor_command like '%" + value + "%'" 
    if(search == 'status'):
        sql += " and a.status = '" + value + "'"
        sql2 += " and a.status = '" + value + "'"
    sql += " order by a.last_time "
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
        ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(sql)
    ShareMethod.views.exeQuery(cur, sql) 
    ShareMethod.views.connClose(conn, cur) 
    table_list = []
    groupSnList = []
    for row in cur:
        groupNameList = []
        groupsn=row[8]
        conn4, cur4 = ShareMethod.views.connDB()
        sql4="select group_name from user_group where sn="+str(groupsn)
        ShareMethod.views.exeQuery(cur4,sql4)
        for row4 in cur4:
            group_sn=row4[0]
        if(row[9] == ""):
            table_list.append({'sn':row[0], 'ip':row[1], 'monitor_command':row[2], 'value':row[3], 'mark':row[4], 'frequency':row[5], 'last_time':row[6], 'status':row[7], 'group_sn':group_sn, 'add_group_sn':row[9]})
        elif(str(row[9]) == "None"):
            table_list.append({'sn':row[0], 'ip':row[1], 'monitor_command':row[2], 'value':row[3], 'mark':row[4], 'frequency':row[5], 'last_time':row[6], 'status':row[7], 'group_sn':group_sn, 'add_group_sn':row[9]})
        else:
            groupSnList = row[9].split(",")
            for add_groupSn in groupSnList:
                conn3, cur3 = ShareMethod.views.connDB()
                sql3="select group_name from user_group where sn="+str(add_groupSn)
                ShareMethod.views.exeQuery(cur3,sql3)
                for name in cur3:
                    groupNameList.append(name[0])
            delimiter = ','
            add_group_sn = delimiter.join(groupNameList) 
            table_list.append({'sn':row[0], 'ip':row[1], 'monitor_command':row[2], 'value':row[3], 'mark':row[4], 'frequency':row[5], 'last_time':row[6], 'status':row[7], 'group_sn':group_sn, 'add_group_sn':add_group_sn})
    sql5="select add_group_sn from server_monitor_info where add_group_sn is Null limit 1"
    conn5, cur5 = ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur5,sql5)
    ShareMethod.views.connClose(conn5, cur5)
    if (monitor_type == '0'):
        return render_to_response('SMIselect_sql.html', locals())
    if (monitor_type == '1'):
        return render_to_response('SMIselect_linux.html', locals())

