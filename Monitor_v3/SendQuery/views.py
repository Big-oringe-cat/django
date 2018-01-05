from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views

def select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')

    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    sql= "select * from inbox where 1 =1 "
    sql2="select count(*) from inbox where 1=1 "
    if(search=='Sender'):
        sql += " and Sender like '%" + value + "%'"
        sql2 += " and Sender like '%" + value + "%'"
    if(search=='CommPort'):
        sql3="select commport from phone_card where mobile like '%"+value+"%'"
        print (sql3)
        ShareMethod.views.exeQuery(cur3,sql3)
        commport = "0"
        for mobile in cur3:
            commport=mobile[0]
        sql += " and CommPort = " + str(commport)
        sql2 += " and CommPort = " + str(commport)
        ShareMethod.views.connClose(conn3,cur3) 

    if startTime!=endTime:
        if startTime!='':
            sql +=" and ArrivedTime >='"+startTime+"'"
            sql2 +=" and ArrivedTime >='"+startTime+"'"
        if endTime!='':
            sql +=" and ArrivedTime <='"+endTime+"'"
            sql2 +=" and ArrivedTime <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and ArrivedTime like '%"+startTime+"%'"
            sql2 +=" and ArrivedTime like '%"+startTime+"%'"
            
    sql += " order by  ID desc "  
    
    if allPostCounts == 0:
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    table_list = []
    for row in cur:
        sql4="select mobile,province from phone_card where commport="+str(row[4])
        mobile=""
        ShareMethod.views.exeQuery(cur4,sql4) 
        for row4 in cur4:
            mobile=row4[0]+"("+row4[1]+")"
        table_list.append({'id':row[0],'Sender':row[1],'mobile':mobile,'Msg':row[2],'ArrivedTime':row[3]})
    ShareMethod.views.connClose(conn,cur) 
    ShareMethod.views.connClose(conn4,cur4) 
    return render_to_response(html,locals())

def select_un(req):
    html='SQselect_un.html'
    conn,cur=ShareMethod.views.connDB_un()
    conn2,cur2=ShareMethod.views.connDB_un()
    conn3,cur3=ShareMethod.views.connDB_un()
    conn4,cur4=ShareMethod.views.connDB_un()
    return select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html)
    
def select_cm(req):
    html='SQselect_cm.html'
    conn,cur=ShareMethod.views.connDB_cm()
    conn2,cur2=ShareMethod.views.connDB_cm()
    conn3,cur3=ShareMethod.views.connDB_cm()
    conn4,cur4=ShareMethod.views.connDB_cm()
    return select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html)    

def select_dianxin(req,conn,cur,conn2,cur2,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    sql= "select * from sms_recv where 1=1 "
    sql2="select count(*) from sms_recv where 1=1 "

    if(search=='smsNumbser'):
        sql += " and smsNumber like '%" + value + "%'"
        sql2 += " and smsNumber like '%" + value + "%'"
    if(search=='PhoNum'):
        sql += " and PhoNum like '%" + value + "%'"
        sql2 += " and PhoNum like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and smsDate >='"+startTime+"'"
            sql2 +=" and smsDate >='"+startTime+"'"
        if endTime!='':
            sql +=" and smsDate <='"+endTime+"'"
            sql2 +=" and smsDate <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and smsDate like '%"+startTime+"%'"
            sql2 +=" and smsDate like '%"+startTime+"%'"
            
    sql += " order by smsDate desc "  
    print(sql)
    if allPostCounts == 0:
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    table_list = []
    for row in cur:
        table_list.append({'Id':row[0],'smsNumber':row[2],'PhoNum':row[4],'smsContent':row[3],'smsDate':row[1]})
        print("smsDate:"+row[4])
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response(html,locals())

def select_cdma(req):
    html="SQselect_cdma.html"
    conn2,cur2=ShareMethod.views.connDB_cdma()
    conn,cur=ShareMethod.views.connDB_cdma()
    return select_dianxin(req,conn,cur,conn2,cur2,html)

#def select_cdma1(req):
#    html="SQselect_cdma1.html"
#    conn2,cur2=ShareMethod.views.connDB_cdma1()
#    conn,cur=ShareMethod.views.connDB_cdma1()
#    return select_dianxin(req,conn,cur,conn2,cur2,html)

def select_auto(req,sql,sql2,conn3,cur3,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    conn,cur=ShareMethod.views.connDB_auto()
#    sql= "select * from receive_report_info where mobile in (select mobile from provinces_test_un.phone_card) "
#    sql2="select count(*) from receive_report_info where mobile in (select mobile from provinces_test_un.phone_card) "
    if(search=='mobile'):
        sql += " and mobile like '%" + value + "%'"
        sql2 += " and mobile like '%" + value + "%'"
    if(search=='td_code'):
        sql += " and td_code like '%" + value + "%'"
        sql2 += " and td_code like '%" + value + "%'"

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
            
    sql += " order by sn desc "  
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_auto()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    province=""
    for row in cur:
        sql3 = "select province from phone_card where mobile='"+row[3]+"'"
        ShareMethod.views.exeQuery(cur3,sql3) 
        for row3 in cur3:
            province = row3[0]
        table_list.append({'id':row[0],'td_code':row[1],'mobile':row[3],'province':province,'status':row[4],'result':row[5],'fail_describe':row[6],'insert_time':row[7]})
    ShareMethod.views.connClose(conn3,cur3) 
    return render_to_response(html,locals())

def select_auto_un(req):
    html="SQselect_auto_un.html"
    conn3,cur3=ShareMethod.views.connDB_un()
    sql= "select * from receive_report_info where mobile in (select mobile from provinces_test_un.phone_card)  "
    sql2="select count(*) from receive_report_info where mobile in (select mobile from provinces_test_un.phone_card) "
    return select_auto(req,sql,sql2,conn3,cur3,html)
def select_auto_cm(req):
    html="SQselect_auto_cm.html"
    conn3,cur3=ShareMethod.views.connDB_cm()
    sql= "select * from receive_report_info where mobile in (select mobile from provinces_test_cm.phone_card)  "
    sql2="select count(*) from receive_report_info where mobile in (select mobile from provinces_test_cm.phone_card) "
    return select_auto(req,sql,sql2,conn3,cur3,html)
def select_auto_cdma(req):
    html="SQselect_auto_cdma.html"
    conn3,cur3=ShareMethod.views.connDB_cdma()
    sql= "select * from receive_report_info where mobile in (select mobile from spcard.phone_card) "
    sql2="select count(*) from receive_report_info where mobile in (select mobile from spcard.phone_card) "
    return select_auto(req,sql,sql2,conn3,cur3,html)
