from django.template.loader import get_template
from urllib.parse import urlencode
from httplib2 import Http
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views
from django.http.response import HttpResponseRedirect
import time

def duty_table(req):
    month=req.REQUEST.get('month','0')
    day=time.strftime('%d',time.localtime(time.time()))
    month1=time.strftime('%m',time.localtime(time.time()))
    if month == '0':
        sql='select * from duty_table where month='+str(month1)
        month=month1
    else:
        sql='select * from duty_table where month='+str(month)
    conn,cur=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    for row in cur:
        table_list.append({'duty_name':row[1],'duty_time':str(row[2]),'content':row[3],'rest_time':row[4],'mobile':row[6]})
    ShareMethod.views.connClose(conn,cur)
    sql1="select * from month"
    conn1,cur1=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur1,sql1)
    count=[]
    for row1 in cur1:
        count.append({'id':row1[0]})
    ShareMethod.views.connClose(conn1,cur1)
    return render_to_response('dutytable.html',locals())

def dutyedit(req):
    month=req.REQUEST.get('month')
    sql='select * from duty_table where month='+str(month)
    conn,cur=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'duty_name':row[1],'duty_time':str(row[2]),'content':row[3],'rest_time':row[4],'mobile':row[6]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('dutyedit.html',locals())

def dutyinsert(req):
    month=req.REQUEST.get('month')
    sql1='insert into duty_table(month)value("'+str(month)+'")'
    conn1,cur1=ShareMethod.views.connDB_13()
    ShareMethod.views.exeInsert(cur1,sql1)
    ShareMethod.views.connClose(conn1,cur1)
    sql='select * from duty_table where month='+str(month)
    conn,cur=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'duty_name':row[1],'duty_time':str(row[2]),'content':row[3],'rest_time':row[4],'mobile':row[6]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('dutyedit.html',locals())

def update(req):
    sn=req.POST.getlist('sn','0')
    for i in range(0,(len(sn))):
        id=sn[i]
        duty_name=req.REQUEST.get('duty_name_'+str(id),'0')
        duty_time=req.REQUEST.get('duty_time_'+str(id),'0')
        content=req.REQUEST.get('content_'+str(id),'0')
        rest_time=req.REQUEST.get('rest_time_'+str(id),'0')
        mobile=req.REQUEST.get('mobile_'+str(id),'0')
        sql='update duty_table set duty_name="'+duty_name+'",duty_time="'+duty_time+'",content="'+content+'",rest_time="'+rest_time+'",mobile="'+mobile+'" where sn='+str(id)
        conn,cur=ShareMethod.views.connDB_13()
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    return HttpResponseRedirect('../SuccessMessage.do?message=dutytable/duty_table')

def delete(req):
    month=req.REQUEST.get('month')
    sn=req.REQUEST.get('sn')
    try:
        sql='delete from duty_table where sn='+sn
        conn,cur=ShareMethod.views.connDB_13()
        ShareMethod.views.exeDelete(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        return HttpResponseRedirect('../SuccessMessage.do?message=dutytable/dutyedit?month='+month)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('../FailureMessage.do?message=dutytable/dutyedit?month='+month)

def sendemail(req):
    month=req.REQUEST.get('month')
    nextmonth=int(month)+1
    http = Http(timeout=20)
    headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    url = "http://yj.baiwutong.com:8180/PlateWarning?"
    email="zhangwei@jiweitech.com,hushuqing@jiweitech.com,zhangyaqing@baiwutong.com,huangyufang@baiwutong.com,wangcan@baiwutong.com,zhanruishan@jiweitech.com"
    emailtitle="运维当月及下月值班表通知"
    content="查看本月值班表请点击:<a href='http://www.monitor.com/Monitor_v3/dutytable/dutyzhanshi'>http://www.monitor.com/Monitor_v3/dutytable/dutyzhanshi?month="+month+"</a></br></br>查看下月值班表请点击:<a href='http://www.monitor.com/Monitor_v3/dutytable/dutyzhanshi?month="+str(nextmonth)+"'>http://www.monitor.com/Monitor_v3/dutytable/dutyzhanshi?month="+str(nextmonth)+"</a><br><br>【技术部运维组通知】"
    email_body = {
                "account":"yunwei",
                "passwd":"123",
                "emailwarning":1,
                "email":email,
                "emailtitle":emailtitle,
                "content":content
                }
    resp, content2 = http.request(url,"POST",urlencode(email_body), headers=headers)
    return HttpResponseRedirect('../SuccessMessage.do?message=dutytable/duty_table')

def dutyduty(req):
    return render_to_response('dutyduty.html')

def dutyzhanshi(req):
    month=req.REQUEST.get('month','0')
    day=time.strftime('%d',time.localtime(time.time()))
    month1=time.strftime('%m',time.localtime(time.time()))
    if month == '0':
        sql='select * from duty_table where month='+str(month1)
        month=month1
    else:
        sql='select * from duty_table where month='+str(month)
    conn,cur=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur,sql)
    table_list=[]
    for row in cur:
        table_list.append({'duty_name':row[1],'duty_time':str(row[2]),'content':row[3],'rest_time':row[4],'mobile':row[6]})
    ShareMethod.views.connClose(conn,cur)
    sql1="select * from month"
    conn1,cur1=ShareMethod.views.connDB_13()
    ShareMethod.views.exeQuery(cur1,sql1)
    count=[]
    for row1 in cur1:
        count.append({'id':row1[0]})
    ShareMethod.views.connClose(conn1,cur1)
    return render_to_response('dutytable1.html',locals())
