from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
def insert(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            monitor_name=req.REQUEST.get('monitor_name','0')
            method='POST'
            monitor_url=req.REQUEST.get('monitor_url','0')
            content=req.REQUEST.get('msg_content','0')
            response=req.REQUEST.get('response','0')
            frequence=req.REQUEST.get('frequence','0')
            status=req.REQUEST.get('status','0')
            sql="insert into protocol_monitor(monitor_name,method,monitor_url,content,response,frequence,status,last_time) values ('"+monitor_name+"','" + method +"','"+monitor_url+"','"+content+"','"+response+"','"+frequence+"',"+str(status)+",'"+NowTime+"')"
            try:
                conn,cur=ShareMethod.views.connDB_12()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=HttpMonitor/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=HttpMonitor/insert.do')
        else:
            return render_to_response('HMinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB_12()
    ShareMethod.views.exeQuery(cur,"select sn,monitor_name,monitor_url,content,response,frequence,status from protocol_monitor where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_name':row[1],'monitor_url':row[2],'content':row[3],'response':row[4],'frequence':row[5],'status':row[6]})
    print(table_list)
    return render_to_response('HMedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    monitor_name=req.REQUEST.get('monitor_name','0')
    monitor_url=req.REQUEST.get('monitor_url','0')
    content=req.REQUEST.get('msg_content','0')
    response=req.REQUEST.get('response','0')
    frequence=req.REQUEST.get('frequence','0')
    status=req.REQUEST.get('status','0')
    try:
        conn,cur=ShareMethod.views.connDB_12()
        sql="update protocol_monitor set monitor_name='"+monitor_name+"',monitor_url='"+monitor_url+"',content='"+content+"',response='"+response+"',frequence='"+frequence+"',status="+str(status)+" where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=HttpMonitor/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=HttpMonitor/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB_12()
    sql= "select sn,monitor_name,method,monitor_url,content,response,frequence,status,last_time from protocol_monitor where 1 =1 "
    sql2="select count(*) from protocol_monitor where 1=1 "
    if(search=='monitor_name'):
        sql += " and monitor_name like '%" + value + "%'"
        sql2 += " and monitor_name like '%" + value + "%'"
    if(search=='monitor_url'):
        sql += " and monitor_url like '%" + value + "%'"
        sql2 += " and monitor_url like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    
    sql += " order by status desc"        
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_12()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'monitor_name':row[1],'method':row[2],'monitor_url':row[3],'content':row[4],'response':row[5],'frequence':row[6],'status':row[7],'last_time':row[8]})
    return render_to_response('HMselect.html',locals())
