# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import os
from urllib.parse import urlencode
from httplib2 import Http
import datetime
import time
import logging
import socket
import random

def ignore(req):
    #忽略方法
    ignore_identifier=''
    md5=''
    id = req.REQUEST.get('id')
    operatorName=req.session.get('username')

    sql = "select ignore_identifier,index_md5 from  notice_info  where sn="+str(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    for row in cur:
        ignore_identifier=row[0]
        md5=str(row[1])+'_'+str(random.uniform(10,100 ))

    if ignore_identifier==0:
       sql = "update notice_info set ignore_identifier=1  where sn="+str(id)
       conn,cur=ShareMethod.views.connDB()
       ShareMethod.views.exeUpdate(cur,sql)
       ShareMethod.views.connClose(conn,cur)
       ShareMethod.views.InfoLog(sql+"操作人: "+operatorName+"-忽略")
       return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/select')
    elif ignore_identifier==1:
       sql1="update notice_info set is_recover=1,status=1,note_taker='"+operatorName+"',update_time=now(),index_md5='"+md5+"' where sn="+str(id)
       conn1,cur1=ShareMethod.views.connDB()
       ShareMethod.views.exeUpdate(cur1,sql1)
       ShareMethod.views.connClose(conn1,cur1)
       ShareMethod.views.InfoLog(sql+"操作人: "+operatorName+"-恢复忽略")
       return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/NIselect_Ignored_select')

def select(req):
    session_tmp = req.session
    for key, value in session_tmp.items():
        print ("session----------->"+key + ' : ' + str(value))
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    admin_id = req.session.get('admin_id','')
    role = req.session.get('role','')
    if role == 4 or role ==6 or role == 8:
        sql= "select * from notice_info where 1 =1 and is_recover=0 and reason is not null and ignore_identifier=0 and comment!='余额预警'"
        sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=0 and reason is not null and ignore_identifier=0 and comment!='余额预警'"
    else:
        sql= "select * from notice_info where 1 =1 and is_recover=0 and reason is not null and ignore_identifier=0 and service_staff ='"+admin_id+"'"
        sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=0 and reason is not null and ignore_identifier=0 and service_staff='"+admin_id+"'"
    print (sql)
    
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='alarm_value'):
        sql += " and alarm_uname like '"+ value +"%'"
        sql2 += " and alarm_uname like '"+ value +"%'"
    if(search=='monitor_level'):
        if(value=='紧急'):
            sql += " and monitor_level like '0' "
            sql2 += " and monitor_level like '0' "
        elif(value=='重要'):
            sql += " and monitor_level like '1' "
            sql2 += " and monitor_level like '1' "
        elif(value=='一般'):
            sql += " and monitor_level like '2' "
            sql2 += " and monitor_level like '2' "
        else:
            sql += " and monitor_level like '%" + value + "%'"
            sql2 += " and monitor_level like '%" + value + "%'"
    if(search=='recover'):
        if(value=='恢复'):
            sql += " and is_recover like '1' "
            sql2 += " and is_recover like '1' "
        elif(value=='未恢复'):
            sql += " and is_recover like '0' "
            sql2 += " and is_recover like '0' "
        else:
            sql += " and is_recover like '%" + value + "%'"
            sql2 += " and is_recover like '%" + value + "%'"
    if(search=='status'):
        if(value=='已发送'):
            sql += " and status like '1' "
            sql2 += " and status like '1' "
        elif(value=='未发送'):
            sql += " and status like '0' "
            sql2 += " and status like '0' "
        else:
            sql += " and status like '%" + value + "%'"
            sql2 += " and status like '%" + value + "%'"    
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by update_time desc "
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)

    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    conn2,cur2=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    deal = ""
    monitor_sn=""
    for row in cur:
        sql2="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur2,sql2)
        for row2 in cur2:
            deal=row2[0] 
            monitor_sn=row2[1]
        alarm_uname=row[15].split(',')
        sql3="select count(*) from notice_detail_info where index_md5 like '%"+str(row[23])+"%'"
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            count=row3[0] 
        if len(alarm_uname) == 1:
            alarm_uname2=""
            table_list.append({'count':count,'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
        elif len(alarm_uname) == 2:
            alarm_uname2=""
            alarm_uname2=alarm_uname[1]
            table_list.append({'count':count,'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
        else:
            alarm_uname2=[]
            for i in range(1,(len(alarm_uname))):
                alarm_uname2.append(alarm_uname[i])
            alarm_uname2=','.join(alarm_uname2)
            table_list.append({'count':count,'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19])})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('NIselect.html',locals())

def recovered_select(req):
    admin_id = req.session.get('admin_id','')
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    operatorName=req.session.get('username')
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')

    if role == 4 or role ==6 or role == 8:
        sql= "select * from notice_info where 1 =1 and is_recover=1"
        sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=1"
    else:
        sql= "select * from notice_info where 1 =1 and is_recover=1 and service_staff='"+admin_id+"'"
        sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=1 and service_staff=+'"+admin_id+"'"

    if(search=='note_taker'):
        sql += " and note_taker like '%" + value + "%'"
        sql2 += " and note_taker like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by insert_time desc "

    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    monitor_sn=''
    deal=''
    for row in cur:
        sql3="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            deal=row3[0]
            monitor_sn=row3[1]
        alarm_uname=row[15].split(',')
        table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_type':row[2],'note_time':row[24],'alarm_uname':alarm_uname[0],'alarm_addname':row[17],'is_recover':row[19]})
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn3,cur3)
    return render_to_response('NIselect_Recovered.html',locals())

def NIselect_Ignored_select(req):
    admin_id = req.session.get('admin_id','')
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    operatorName=req.session.get('username')
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')

    if role == 4 or role ==6 or role == 8:
        sql= "select * from notice_info where 1 =1 and ignore_identifier=1 and is_recover=0"
        sql2 = "select count(*) as count from notice_info where 1=1 and ignore_identifier=1 and is_recover=0"
    else:
        sql= "select * from notice_info where 1 =1 and ignore_identifier=1 and is_recover=0 and service_staff='"+admin_id+"'"
        sql2 = "select count(*) as count from notice_info where 1=1 and ignore_identifier=1 and is_recover=0 and service_staff='"+admin_id+"'"

    if(search=='note_taker'):
        sql += " and note_taker like '%" + value + "%'"
        sql2 += " and note_taker like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by update_time desc "

    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    monitor_sn=""
    deal=""
    for row in cur:
        sql3="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            deal=row3[0]
            monitor_sn=row3[1]
        alarm_uname=row[15].split(',')
        table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'alarm_type':row[2],'note_time':row[24],'alarm_uname':alarm_uname[0],'is_recover':row[19]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('NIselect_Ignored.html',locals()) 

def reason_select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    operatorName=req.session.get('username')
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    
    sql= "select * from notice_info where reason !='' and reason != 'None' "
    sql2 = "select count(*) as count from notice_info where reason !='' and reason != 'None' "
    
    if(search=='note_taker'):
        sql += " and note_taker like '%" + value + "%'"
        sql2 += " and note_taker like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by insert_time desc "
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    table_list=[]
    monitor_sn=""
    deal=""
    for row in cur:
        sql3="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            deal=row3[0]
            monitor_sn=row3[1]
        alarm_uname=row[15].split(',')
        table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'alarm_type':row[2],'note_time':row[24],'alarm_uname':alarm_uname[0],'is_recover':row[19]})
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn3,cur3)
    return render_to_response('NIselect_reason.html',locals())

def newreason_select(req):
    admin_id = req.session.get('admin_id','')
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    operatorName=req.session.get('username')
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    id=req.REQUEST.get('id','0')
 
    if role == 4 or role ==6 or role == 8:
        sql= "select * from notice_info where (reason is NULL or content like '%分钟没有执行Linux命令监控%') and is_recover = 0"
        sql2 = "select count(*) as count from notice_info where (reason is NULL or content like '%分钟没有执行Linux命令监控%') and is_recover =0"
    else:
        sql= "select * from notice_info where (reason is NULL or content like '%分钟没有执行Linux命令监控%') and is_recover = 0 and service_staff='"+admin_id+"'"
        sql2 = "select count(*) as count from notice_info where (reason is NULL or content like '%分钟没有执行Linux命令监控%') and is_recover =0 and service_staff ='"+admin_id+"'"
    
    sql5= "update notice_info set note_time=now() where sn="+id 
    conn5,cur5=ShareMethod.views.connDB()
    ShareMethod.views.exeUpdate(cur5,sql5)
    ShareMethod.views.connClose(conn5,cur5)


    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='alarm_value'):
        sql += " and alarm_uname like '"+ value +"%'"
        sql2 += " and alarm_uname like '"+ value +"%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
   
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by insert_time desc "
   
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        print("hello 3",cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    conn4,cur4=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    monitor_sn=""
    deal=""
    for row in cur:
        sql3="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur3,sql3)
        print("hello 4",sql3)
        for row3 in cur3:
            deal=row3[0]
            monitor_sn=row3[1]
        sql4="select count(*) from notice_detail_info where index_md5 like '%"+str(row[23])+"%'"
        ShareMethod.views.exeQuery(cur4,sql4)
        for row4 in cur4:
            count=row4[0]
        alarm_uname=row[15].split(',')
        if len(alarm_uname) == 1:
            table_list.append({'count':count,'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'alarm_addname':row[17],'alarm_type':row[2],'alarm_uname1':alarm_uname[0],'is_recover':row[19],'note_time':row[24]})
        else:
            table_list.append({'count':count,'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'alarm_addname':row[17],'alarm_type':row[2],'alarm_uname1':alarm_uname[0],'alarm_uname2':alarm_uname[1],'is_recover':row[19],'note_time':row[24]})
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn3,cur3)
    return render_to_response('NIselect_new_reason.html',locals())

def addReason(req):
    session_tmp = req.session  
    for key, value in session_tmp.items():  
        print (key + ' : ' + str(value))
    print("session_key1:")
    print(req.session.session_key)
    operatorName=req.session.get('username')
    print("session_key2:")
    print(req.session.session_key)
    id = req.REQUEST.get('id')
    content = req.REQUEST.get('msg_content')
    reason = req.REQUEST.get('reason')
    note_taker = req.REQUEST.get('note_taker','0')
    is_recover=req.REQUEST.get('is_recover',0)
    yes=req.REQUEST.get('yes',0)
    search=req.REQUEST.get('search',0)
    md5=req.REQUEST.get('md5',0)
    rsql=""
    sql=""

    if req.method == 'POST':
        sql4='select response_standard from notice_info where sn='+str(id)
        conn4,cur4=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur4,sql4)
        ShareMethod.views.connClose(conn4,cur4)
        response_standard=""
        for row4 in cur4:
            response_standard = row4[0]
        sql6="select value from config_info where `key` = 'phone_resp_time'"
        sql8="select value from config_info where `key` = 'sms_resp_time'"
        sql9="select value from config_info where `key` = 'screen_resp_time'"
        sql10="select value from config_info where `key` = 'recovery_resp_time'"
        conn6,cur6=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur6,sql6)
        ShareMethod.views.connClose(conn6,cur6)
        conn8,cur8=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur8,sql8)
        ShareMethod.views.connClose(conn8,cur8)
        conn9,cur9=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur9,sql9)
        ShareMethod.views.connClose(conn9,cur9)
        conn10,cur10=ShareMethod.views.connDB()
        ShareMethod.views.exeUpdate(cur10,sql10)
        ShareMethod.views.connClose(conn10,cur10)
        for row6 in cur6:
            phone_resp_time=int(row6[0])
        for row8 in cur8:
            sms_resp_time=int(row8[0])
        for row9 in cur9:
            screen_resp_time=int(row9[0])
        for row10 in cur10:
            recovery_resp_time=int(row10[0])

        #try:
        if reason == 'None' and yes == '1' and reason == '请选择':
            return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/newreason_select')
        else:
            if yes == '1':
                if response_standard == None:
                    #response_time = note_time 
                    rsql = "update notice_info set reason='"+reason+"',note_taker='"+operatorName+"' where sn="+str(id)
                    rconn,rcur=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(rcur,rsql)
                    ShareMethod.views.connClose(rconn,rcur)
 
                    sql5="select timestampdiff(minute,insert_time,note_time) as response_time,monitor_level from notice_info where note_time!='None' and sn="+str(id)
                    conn5,cur5=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(cur5,sql5)
                    ShareMethod.views.connClose(conn5,cur5)
                    response_time=""
                    monitor_level=""
                    for row5 in cur5:
                        response_time = row5[0]
                        monitor_level = row5[1]
                    if monitor_level == 0 and response_time > phone_resp_time:
                        rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                    elif monitor_level == 1 and response_time > sms_resp_time:
                        rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                    elif monitor_level == 2 and response_time > screen_resp_time:
                        rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                    else:
                        rsql1 = "update notice_info set response_standard = '1'  where sn="+str(id)
                    rconn1,rcur1=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(rcur1,rsql1)
                    ShareMethod.views.connClose(rconn1,rcur1)
                else:
                    rsql = "update notice_info set reason='"+reason+"' where sn="+str(id)
                    rconn,rcur=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(rcur,rsql)
                    ShareMethod.views.connClose(rconn,rcur)
            else:
                if search == 'None':
                    return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/newreason_select')
                else:
                    if response_standard == None:
                        rsql = "update notice_info set reason='"+search+"',note_taker='"+operatorName+"' where sn="+str(id)
                        rconn,rcur=ShareMethod.views.connDB()
                        ShareMethod.views.exeUpdate(rcur,rsql)
                        ShareMethod.views.connClose(rconn,rcur)
                        sql5="select timestampdiff(minute,insert_time,note_time) as response_time,monitor_level from notice_info where note_time!='None' and sn="+str(id)
                        conn5,cur5=ShareMethod.views.connDB()
                        ShareMethod.views.exeUpdate(cur5,sql5)
                        ShareMethod.views.connClose(conn5,cur5)
                        response_time=""
                        monitor_level=""
                        for row5 in cur5:
                            response_time = row5[0]
                            monitor_level = row5[1]
                        if monitor_level == 0 and response_time > phone_resp_time:
                            rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                        elif monitor_level == 1 and response_time > sms_resp_time:
                            rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                        elif monitor_level == 2 and response_time > screen_resp_time:
                            rsql1 = "update notice_info set response_standard = '2'  where sn="+str(id)
                        else:
                            rsql1 = "update notice_info set response_standard = '1'  where sn="+str(id)
                        rconn1,rcur1=ShareMethod.views.connDB()
                        ShareMethod.views.exeUpdate(rcur1,rsql1)
                        ShareMethod.views.connClose(rconn1,rcur1)
                    else:
                        rsql = "update notice_info set reason='"+search+"' where sn="+str(id)
                        rconn,rcur=ShareMethod.views.connDB()
                        ShareMethod.views.exeUpdate(rcur,rsql)
                        ShareMethod.views.connClose(rconn,rcur)
            sql1="update notice_info set is_recover=1,status=1,recovery_time=now(),index_md5='"+md5+"' where sn="+str(id)
            print (sql1)
        if is_recover == '1':
            conn1,cur1=ShareMethod.views.connDB()
            ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
            sql7="select timestampdiff(minute,update_time,recovery_time) as response_time,monitor_level from notice_info where note_time!='None' and sn="+str(id)
            conn7,cur7=ShareMethod.views.connDB()
            ShareMethod.views.exeUpdate(cur7,sql7)
            ShareMethod.views.connClose(conn7,cur7)
            recovery_response_time=""
            for row7 in cur7:
                recovery_response_time = row7[0]
                monitor_level = row7[1]
            if monitor_level == 0 and recovery_response_time > phone_resp_time:
                rsql2 = "update notice_info set recovery_standard = '2'  where sn="+str(id)
            elif monitor_level == 1 and recovery_response_time > sms_resp_time:
                rsql2 = "update notice_info set recovery_standard = '2'  where sn="+str(id)
            elif monitor_level == 2 and recovery_response_time > screen_resp_time:
                rsql2 = "update notice_info set recovery_standard = '2'  where sn="+str(id)
            else:
                rsql2 = "update notice_info set recovery_standard = '1'  where sn="+str(id)
            rconn2,rcur2=ShareMethod.views.connDB()
            ShareMethod.views.exeUpdate(rcur2,rsql2)
            ShareMethod.views.connClose(rconn2,rcur2)
        #except Exception as e:
        #    if note_taker == '0':
        #        return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/select')
        #    else:
        #        return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/reason_select')
        
        if note_taker == '0':
            return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/Myalarm')
        else:
            return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/Myalarm')
            
    else:
        note_taker = req.REQUEST.get('note_taker','0')
        sql = "select content,reason,note_taker,is_recover,status,index_md5 from notice_info where sn="+str(id)
        conn,cur=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur,sql)
        reasonList = []
        table_list2=[]
        table_list3=[]
        for row in cur:
            sql2='select left(insert_time,10),count(*) from notice_info where index_md5 like "'+str(row[5])+'%" group by 1'
            conn2,cur2=ShareMethod.views.connDB()
            ShareMethod.views.exeQuery(cur2,sql2)
            for row2 in cur2:
                table_list2.append({'insert_time':str(row2[0]),'count':row2[1]})
            sql3='select reason,count(*) from notice_info where index_md5 like "'+str(row[5])+'%" group by 1'
            conn3,cur3=ShareMethod.views.connDB()
            ShareMethod.views.exeQuery(cur3,sql3)
            for row3 in cur3:
                table_list3.append({'reason':row3[0]})
            reasonList.append({'id':id,'content':row[0],'reason':row[1],'note_taker':row[2],'is_recover':str(row[3]),'status':row[4]})
        md5=str(row[5])+'_'+str(random.uniform(10,100 ))
        ShareMethod.views.connClose(conn,cur)
        ShareMethod.views.connClose(conn2,cur2)
        ShareMethod.views.connClose(conn3,cur3)
        return render_to_response('RSinsert.html',locals())
        
    
    
def FailureNotification(req):
    if req.method == 'POST':
        operatorName=req.session.get('username')
        notice_type=req.REQUEST.get('notice_type')
        startTime=req.REQUEST.get('startTime')
        servers=req.REQUEST.get('servers')
        time=req.REQUEST.get('time')
        content_owner=req.REQUEST.get('content_owner')
        content_user=req.REQUEST.get('content_user')
        alarm_type=req.REQUEST.get('check_box_list','0')
        http = Http(timeout=20)
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        url = "http://yj.baiwutong.com:8180/PlateWarning?"
        mobile_xs = "<qtxs>"
        mobile_kf = "<qtkf>"
        #phone = "13261289750"
        screen = "1000003" #客服全体的公用账号
        #screen = "1012079"
        email = "yykf@hongshutech.com,xskf@hongshutech.com,kfz@baiwutong.com,cpz@hongshutech.com,yunwei@baiwutong.com,bailei@hongshutech.com,system@hongshutech.com,idccpz@baiwutong.com"
        email_yunwei = "yunwei@baiwutong.com"
        emailtitle = "【通知】"+notice_type
        if alarm_type == "email":
            content="Dear All,</br> </br><B>影响服务器：<font color=red>"+str(servers)+"</font></B></br></br><B>内部通知内容：</B>"+str(content_owner)+"</br></br><B>建议通知客户内容：</B>"+str(content_user)+"</br></br><B>开始时间：<font color=red>"+str(startTime)+"</font></B></br></br><B>影响评估时间：<font color=red>"+str(time)+"</font></B></br></br></br>请诸位知悉并相互转告，谢谢。</br></br></br>【技术部运维组通知】"
            email_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "emailwarning":1,
                    "email":email,
                    "emailtitle":emailtitle,
                    "content":content
                    }
            #email="yykf@hognshutech.com,xskf@hognshutech.com,bwkf@hognshutech.com,hskf@hognshutech.com,cpz@hognshutech.com,yunwei@hognshutech.com,bailei@hongshutech.com,system@hongshutech.com,idccpz@baiwutong.com"
            #email = "jinyalin\@hongshutech.com"
           # command = "curl -w --data 'account=yunwei&passwd=123&emailwarning=1&email="+email+"&content="+content+"' http://yj.baiwutong.com:8180/PlateWarning"
           # print(command)
            resp, content2 = http.request(url,"POST",urlencode(email_body), headers=headers)
            print(resp,content2)
            print("content_email:"+content)
        if alarm_type == "email_yunwei":
            content="Dear All,</br> </br><B>影响服务器：<font color=red>"+str(servers)+"</font></B></br></br><B>内部通知内容：</B>"+str(content_owner)+"</br></br><B>建议通知客户内容：</B>"+str(content_user)+"</br></br><B>开始时间：<font color=red>"+str(startTime)+"</font></B></br></br><B>影响评估时间：<font color=red>"+str(time)+"</font></B></br></br></br>请诸位知悉并相互转告，谢谢。</br></br></br>【技术部运维组通知】"
            email_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "emailwarning":1,
                    "email":email,
                    "emailtitle":emailtitle,
                    "content":content
                    }
            #email="yykf@hognshutech.com,xskf@hognshutech.com,bwkf@hognshutech.com,hskf@hognshutech.com,cpz@hognshutech.com,yunwei@hognshutech.com,bailei@hongshutech.com,system@hongshutech.com,idccpz@baiwutong.com"
            #email = "jinyalin\@hongshutech.com"
           # command = "curl -w --data 'account=yunwei&passwd=123&emailwarning=1&email="+email+"&content="+content+"' http://yj.baiwutong.com:8180/PlateWarning"
           # print(command)
            resp, content2 = http.request(url,"POST",urlencode(email_body), headers=headers)
            print(resp,content2)
            print("content_email:"+content)
        if alarm_type == "email_jishu":
            email="jsb@hongshutech.com,xmjsb@jiweitech.com"
            content="Dear All,</br> </br><B>影响服务器：<font color=red>"+str(servers)+"</font></B></br></br><B>内部通知内容：</B>"+str(content_owner)+"</br></br><B>建议通知客户内容：</B>"+str(content_user)+"</br></br><B>开始时间：<font color=red>"+str(startTime)+"</font></B></br></br><B>影响评估时间：<font color=red>"+str(time)+"</font></B></br></br></br>请诸位知悉并相互转告，谢谢。</br></br></br>【技术部运维组通知】"
            email_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "emailwarning":1,
                    "email":email,
                    "emailtitle":emailtitle,
                    "content":content
                    }
            #email="yykf@hognshutech.com,xskf@hognshutech.com,bwkf@hognshutech.com,hskf@hognshutech.com,cpz@hognshutech.com,yunwei@hognshutech.com,bailei@hongshutech.com,system@hongshutech.com,idccpz@baiwutong.com"
            #email = "jinyalin\@hongshutech.com"
           # command = "curl -w --data 'account=yunwei&passwd=123&emailwarning=1&email="+email+"&content="+content+"' http://yj.baiwutong.com:8180/PlateWarning"
           # print(command)
            resp, content2 = http.request(url,"POST",urlencode(email_body), headers=headers)
            print(resp,content2)
            print("content_email:"+content)
        if alarm_type == "sms_kf":
            content="紧急通知：\r\n影响服务器："+str(servers)+"\r\n内部通知内容："+str(content_owner)+"\r\n建议通知客户内容："+str(content_user)+"\r\n开始时间："+str(startTime)+"\r\n影响评估时间："+str(time)+"\r\n请诸位知悉并相互转告，谢谢。\r\n【技术部运维组通知】"
            sms_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "smswarning":'1',
                    "mobile":mobile_kf,
                    "content":content
                    }
           # mobile = "13261289750"
            #command = "curl -w --data 'account=yunwei&passwd=123&smswarning=1&mobile="+mobile+"&content="+content+"' http://yj.baiwutong.com:8180/PlateWarning"
          #  print(command)
            resp, content2 = http.request(url,"POST",urlencode(sms_body), headers=headers)
            print(resp,content2)
            print("content_sms:"+content)
        if alarm_type == "sms_xs":
            content="紧急通知：\r\n影响服务器："+str(servers)+"\r\n内部通知内容："+str(content_owner)+"\r\n建议通知客户内容："+str(content_user)+"\r\n开始时间："+str(startTime)+"\r\n影响评估时间："+str(time)+"\r\n请诸位知悉并相互转告，谢谢。\r\n【技术部运维组通知】"
            sms_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "smswarning":'1',
                    "mobile":mobile_xs,
                    "content":content
                    }
            resp, content2 = http.request(url,"POST",urlencode(sms_body), headers=headers)
            print(resp,content2)
            print("content_sms:"+content)
        if alarm_type == "screen":
            #content="紧急通知：\r\n影响服务器："+str(servers)+"\r\n内部通知内容："+str(content_owner)+"\r\n建议通知客户内容："+str(content_user)+"\r\n开始时间："+str(startTime)+"\r\n影响评估时间："+str(time)+"\r\n请诸位知悉并相互转告，谢谢。\r\n【技术部运维组通知】"
            content="紧急通知：影响服务器："+str(servers)+"内部通知内容："+str(content_owner)+"建议通知客户内容："+str(content_user)+"开始时间："+str(startTime)+"\r\n影响评估时间："+str(time)+"请诸位知悉并相互转告，谢谢。【技术部运维组通知】"
            sms_body = {
                    "account":"yunwei",
                    "passwd":"123",
                    "screenwarning":'1',
                    "screenuser":screen,
                    "content":content
                    }
            resp, content2 = http.request(url,"POST",urlencode(sms_body), headers=headers)
            print(resp,content2)
            print("content_screen:"+content)
#         if alarm_type == "phone":
#             content="紧急通知：影响服务器："+str(servers)+"内部通知内容："+str(content_owner)+"建议通知客户内容："+str(content_user)+"开始时间："+str(startTime)+"影响评估时间："+str(time)+"请诸位知悉并相互转告，谢谢。【技术部运维组通知】"
#             phone_body = {
#                     "account":"yunwei",
#                     "passwd":"123",
#                     "smswarning":'1',
#                     "phone":phone,
#                     "emailtitle":emailtitle,
#                     "content":content
#                     }
#             resp, content2 = http.request(url,"POST",urlencode(phone_body), headers=headers)
#             print(resp,content2)
#             print("content_phone:"+content)
#                        
        return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/FailureNotification.do')
    else:
        serverNames=[]
        conn,cur=ShareMethod.views.connDB()
        sql="select server_name from server_info where status=0"
        ShareMethod.views.exeQuery(cur,sql)
        for row in cur:
            serverNames.append({'serverName':row[0]})
        ShareMethod.views.connClose(conn,cur)
        return render_to_response('FailureNotification.html',locals())


def recover(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    
    sql= "select * from notice_info where 1 =1 and is_recover=0 and ignore_identifier=0 and comment!='余额预警'"
    sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=0 and ignore_identifier=0 and comment!='余额预警'"
    
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='alarm_value'):
        sql += " and alarm_uname like '%"+ value +"%'"
        sql2 += " and alarm_uname like '%"+ value +"%'"
    if(search=='monitor_level'):
        if(value=='紧急'):
            sql += " and monitor_level like '0' "
            sql2 += " and monitor_level like '0' "
        elif(value=='重要'):
            sql += " and monitor_level like '1' "
            sql2 += " and monitor_level like '1' "
        elif(value=='一般'):
            sql += " and monitor_level like '2' "
            sql2 += " and monitor_level like '2' "
        else:
            sql += " and monitor_level like '%" + value + "%'"
            sql2 += " and monitor_level like '%" + value + "%'"
    if(search=='status'):
        if(value=='已发送'):
            sql += " and status like '1' "
            sql2 += " and status like '1' "
        elif(value=='未发送'):
            sql += " and status like '0' "
            sql2 += " and status like '0' "
        else:
            sql += " and status like '%" + value + "%'"
            sql2 += " and status like '%" + value + "%'"    
    if(search=='jilu'):
        sql += " and reason is Null and alarm_uname like '%"+ value +"%'"
        sql2 += " and reason is Null and alarm_uname like '%"+ value +"%'"
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by update_time desc "
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination1(sql, pageType, curPage, allPostCounts)

    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    conn2,cur2=ShareMethod.views.connDB()
    deal = ""
    monitor_sn=""
    for row in cur:
        sql2="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur2,sql2)
        for row2 in cur2:
            deal=row2[0] 
            monitor_sn=row2[1]
        alarm_uname2=""
        alarm_uname=row[15].split(',')
        if len(alarm_uname) == 1:
            alarm_uname2=""
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'recover':str(row[19])})
        elif len(alarm_uname) == 2:
            alarm_uname2=alarm_uname[1]
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'recover':str(row[19])})
        else:
            for i in (1,(len(alarm_uname)-2)):
                alarm_uname2=alarm_uname[i]+','+alarm_uname[i+1]
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'recover':str(row[19])})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('recover.html',locals())


def recover_add_reason(req):
    value=req.REQUEST.get('value')
    search=req.REQUEST.get('search')
    id = req.POST.getlist('id')
    id=','.join(id)
    md5=str(random.uniform(10,100 ))
    sql="select deal_way from monitor_info where sn in(select monitor_sn from notice_info where sn in("+ id +")) limit 1"
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    dealwayList=[]
    for row in cur:
        dealwayList.append({'dealway':row[0]})
    return render_to_response('recover_RSinsert.html',locals())

def recover_add_reason2(req):
    value=req.REQUEST.get('value','0')
    search=req.REQUEST.get('search','0')
    note_taker=req.REQUEST.get('note_taker','0')
    id=req.REQUEST.get('id')
    reason=req.REQUEST.get('reason')
    md5=str(random.uniform(10,100 ))
    return render_to_response('recover_RSinsert2.html',locals())

def recover_reason(req):
    value=req.REQUEST.get('value')
    search=req.REQUEST.get('search')
    operatorName=req.session.get('username')
    reason=req.REQUEST.get('reason')
    id = req.REQUEST.get('id')
    b=len(id)
    if b != 3:
        id=id.split(',')
    reason = req.REQUEST.get('reason')
    is_recover=req.REQUEST.get('is_recover',0)
    md5=req.REQUEST.get('md5',0)
    rsql=""
    sql=""
    #try:
    if reason == 'None':
        return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/select')
    else:
        if b == 3:
            sql2="select index_md5 from notice_info where sn="+id
            conn2,cur2=ShareMethod.views.connDB()
            ShareMethod.views.exeQuery(cur2,sql2)
            ShareMethod.views.connClose(conn2,cur2)
            index_md5=""
            for row2 in cur2:
                index_md5=row2[0]+'_'+md5
            rsql = "update notice_info set reason='"+reason+"',note_taker='"+operatorName+"',note_time=now() where sn="+str(id)
            rconn,rcur=ShareMethod.views.connDB()
            ShareMethod.views.exeUpdate(rcur,rsql)
            ShareMethod.views.connClose(rconn,rcur)
            sql1="update notice_info set is_recover=1,status=1,note_time=now(),index_md5='"+index_md5+"' where sn="+str(id)
            if is_recover == '1':
                conn1,cur1=ShareMethod.views.connDB()
                ShareMethod.views.exeUpdate(cur1,sql1)
                ShareMethod.views.connClose(conn1,cur1)
        else:
            for i in range(0,len(id)):
                sql="select index_md5 from notice_info where sn="+id[i]
                conn,cur=ShareMethod.views.connDB()
                ShareMethod.views.exeQuery(cur,sql)
                ShareMethod.views.connClose(conn,cur)
                index_md5=""
                for row in cur:
                    index_md5=row[0]+'_'+md5
                rsql = "update notice_info set reason='"+reason+"',note_taker='"+operatorName+"',note_time=now() where sn="+id[i]
                rconn,rcur=ShareMethod.views.connDB()
                ShareMethod.views.exeUpdate(rcur,rsql)
                ShareMethod.views.connClose(rconn,rcur)
                sql1="update notice_info set is_recover=1,status=1,note_time=now(),index_md5='"+index_md5+"' where sn="+id[i]
                if is_recover == '1':
                    conn1,cur1=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(cur1,sql1)
                    ShareMethod.views.connClose(conn1,cur1)
    #except Exception as e:
    #    return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/recover?')
    return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/recover')

def recover_reason2(req):
    value=req.REQUEST.get('value')
    search=req.REQUEST.get('search')
    operatorName=req.session.get('username')
    id = req.REQUEST.get('id')
    note_taker=req.REQUEST.get('note_taker')
    b=len(id)
    if b != 3:
        id=id.split(',')
    reason = req.REQUEST.get('reason')
    is_recover=req.REQUEST.get('is_recover',0)
    md5=req.REQUEST.get('md5',0)
    rsql=""
    sql=""
    #try:
    if reason == 'None':
        return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/select')
    else:
        if b == 3:
            sql2="select index_md5 from notice_info where sn="+id
            conn2,cur2=ShareMethod.views.connDB()
            ShareMethod.views.exeQuery(cur2,sql2)
            ShareMethod.views.connClose(conn2,cur2)
            index_md5=""
            for row2 in cur2:
                index_md5=row2[0]+'_'+md5
            rsql = "update notice_info set reason='"+reason+"',note_taker='"+operatorName+"',note_time=now() where sn="+str(id)
            rconn,rcur=ShareMethod.views.connDB()
            ShareMethod.views.exeUpdate(rcur,rsql)
            ShareMethod.views.connClose(rconn,rcur)
            sql1="update notice_info set is_recover=1,status=1,note_time=now(),index_md5='"+index_md5+"' where sn="+str(id)
            if is_recover == '1':
                conn1,cur1=ShareMethod.views.connDB()
                ShareMethod.views.exeUpdate(cur1,sql1)
                ShareMethod.views.connClose(conn1,cur1)
        else:
            for i in range(0,len(id)):
                sql="select index_md5 from notice_info where sn="+id[i]
                conn,cur=ShareMethod.views.connDB()
                ShareMethod.views.exeQuery(cur,sql)
                ShareMethod.views.connClose(conn,cur)
                index_md5=""
                for row in cur:
                    index_md5=row[0]+'_'+md5
                rsql = "update notice_info set reason='"+reason+"',note_taker='"+operatorName+"',note_time=now() where sn="+id[i]
                rconn,rcur=ShareMethod.views.connDB()
                ShareMethod.views.exeUpdate(rcur,rsql)
                ShareMethod.views.connClose(rconn,rcur)
                sql1="update notice_info set is_recover=1,status=1,note_time=now(),index_md5='"+index_md5+"' where sn="+id[i]
                if is_recover == '1':
                    conn1,cur1=ShareMethod.views.connDB()
                    ShareMethod.views.exeUpdate(cur1,sql1)
                    ShareMethod.views.connClose(conn1,cur1)
    #except Exception as e:
    #    return HttpResponseRedirect('../FailureMessage.do?message=NoticeInfo/recover?')
    if note_taker == '0':
            return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/select')
    else:
            return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/reason_select')
    #return HttpResponseRedirect('../SuccessMessage.do?message=NoticeInfo/recover')


def notice_detail(req):
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    sql= "select * from notice_detail_info where 1 =1"
    sql2 = "select count(*) as count from notice_detail_info where 1=1 "
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='monitor_sn'):
        sql += " and monitor_sn like '%" + value + "%'"
        sql2 += " and monitor_sn like '%" + value + "%'"
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by insert_time desc "
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'comment':row[1],'content':row[2],'server_id':row[3],'monitor_sn':row[4],'insert_time':row[5]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('notice_detail.html',locals())

def Myalarm(req):
    session_tmp = req.session
    operatorName = req.session.get('username', '0')
    for key, value in session_tmp.items():
        print ("session----------->"+key + ' : ' + str(value))
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    id = req.REQUEST.get('id','0')
    value=req.REQUEST.get('value','')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')

    sql5= "update notice_info set note_time=now() where sn="+id
    conn5,cur5=ShareMethod.views.connDB()
    ShareMethod.views.exeUpdate(cur5,sql5)
    ShareMethod.views.connClose(conn5,cur5)
    
    sql= "select * from notice_info where 1 =1 and is_recover=0 and ignore_identifier=0 and comment!='余额预警' and alarm_uname like '%" + operatorName + "%'"
    sql2 = "select count(*) as count from notice_info where 1=1 and is_recover=0 and ignore_identifier=0 and comment!='余额预警' and alarm_uname like '%" + operatorName + "%'"
    
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='alarm_value'):
        sql += " and alarm_uname like '"+ value +"%'"
        sql2 += " and alarm_uname like '"+ value +"%'"
    if(search=='monitor_level'):
        if(value=='紧急'):
            sql += " and monitor_level like '0' "
            sql2 += " and monitor_level like '0' "
        elif(value=='重要'):
            sql += " and monitor_level like '1' "
            sql2 += " and monitor_level like '1' "
        elif(value=='一般'):
            sql += " and monitor_level like '2' "
            sql2 += " and monitor_level like '2' "
        else:
            sql += " and monitor_level like '%" + value + "%'"
            sql2 += " and monitor_level like '%" + value + "%'"
    if(search=='recover'):
        if(value=='恢复'):
            sql += " and is_recover like '1' "
            sql2 += " and is_recover like '1' "
        elif(value=='未恢复'):
            sql += " and is_recover like '0' "
            sql2 += " and is_recover like '0' "
        else:
            sql += " and is_recover like '%" + value + "%'"
            sql2 += " and is_recover like '%" + value + "%'"
    if(search=='status'):
        if(value=='已发送'):
            sql += " and status like '1' "
            sql2 += " and status like '1' "
        elif(value=='未发送'):
            sql += " and status like '0' "
            sql2 += " and status like '0' "
        else:
            sql += " and status like '%" + value + "%'"
            sql2 += " and status like '%" + value + "%'"    
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by update_time desc "
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)

    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    conn2,cur2=ShareMethod.views.connDB()
    deal = ""
    monitor_sn=""
    for row in cur:
        sql2="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur2,sql2)
        for row2 in cur2:
            deal=row2[0] 
            monitor_sn=row2[1]
        alarm_uname=row[15].split(',')
        if len(alarm_uname) == 1:
            alarm_uname2=""
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19]),'note_time':row[24]})
        elif len(alarm_uname) == 2:
            alarm_uname2=""
            alarm_uname2=alarm_uname[1]
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19]),'note_time':row[24]})
        else:
            alarm_uname2=[]
            for i in range(1,(len(alarm_uname))):
                alarm_uname2.append(alarm_uname[i])
            alarm_uname2=','.join(alarm_uname2)
            table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':str(row[2]),'comment':row[4],'status':row[5],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'insert_time':row[7],'alarm_uname':alarm_uname2,'alarm_uname1':alarm_uname[0],'alarm_addname':row[17],'recover':str(row[19]),'note_time':row[24]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('Myalarm.html',locals())


def Myignore(req):
    operatorName = req.session.get('username', '0')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    operatorName=req.session.get('username')
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')

    sql= "select * from notice_info where 1 =1 and ignore_identifier=1 and is_recover=0 and alarm_uname like '%" + operatorName + "%'"
    sql2 = "select count(*) as count from notice_info where 1=1 and ignore_identifier=1 and is_recover=0 and alarm_uname like '%" + operatorName + "%'"

    if(search=='note_taker'):
        sql += " and note_taker like '%" + value + "%'"
        sql2 += " and note_taker like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by update_time desc "

    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    monitor_sn=""
    deal=""
    for row in cur:
        sql3="select a.deal_way,b.monitor_sn from monitor_info a,notice_info b where a.sn=b.monitor_sn and b.sn="+str(row[0])
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            deal=row3[0]
            monitor_sn=row3[1]
        alarm_uname=row[15].split(',')
        table_list.append({'monitor_sn':monitor_sn,'deal':deal,'id':row[0],'content':row[1],'monitor_level':row[2],'status':row[5],'insert_time':row[7],'reason':row[8],'note_taker':row[9],'alarm_amount':row[13],'alarm_type':row[2],'note_time':row[24],'alarm_uname':alarm_uname[0],'is_recover':row[19]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('Myignore.html',locals())

def alarm_detail(req):
    id=req.REQUEST.get('id',0)
    sn=req.REQUEST.get('sn','0')
    print('whello',sn)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from monitor_info where sn="+id)
    sql="select comment from monitor_info where sn='" +id+"'"
    sql2="select content from notice_info where sn="+sn
    print ('whello ',sql2)
    conn1,cur1=ShareMethod.views.connDB()  
    ShareMethod.views.exeQuery(cur1,sql)
    conn2,cur2=ShareMethod.views.connDB()  
    ShareMethod.views.exeQuery(cur2,sql2)
    ShareMethod.views.connClose(conn,cur) 
    ShareMethod.views.connClose(conn1,cur1)
    ShareMethod.views.connClose(conn2,cur2) 
    commentList=[]
    for row in cur1:
        commentList.append({'comment':row[0]})
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_command':row[1],'warning_content':row[2],'comment':row[3],'monitor_type':row[4],'expect_result':row[5],'monitor_level':str(row[6]),'alarm_count':row[7],'alarm_frequency':row[8],'alarm_time':row[9],'deal_way':row[10],'sensitivity':row[11]})
    print(table_list)
    contentList=[]
    for row in cur2:
        contentList.append({'alarm_content':row[0]})
    print("whello",contentList)
    return render_to_response('monitor_info_detail.html',{'table_list':table_list,'commentList':commentList,'contentList':contentList})
