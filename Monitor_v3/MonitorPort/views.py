from django.shortcuts import render
from django.shortcuts import render_to_response
import ShareMethod.views
from django.http.response import HttpResponseRedirect
from django import forms
from django.http import HttpResponse

def select(req):
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    print(search)
    print(value)
    sql="select b.sn,a.server_id,b.parameter_value,b.status,b.insert_time,b.update_time from service_monitor_param b,server_info a where( b.parameter_value like '%8855%' or b.parameter_value like '%8801%' or b.parameter_value like '%8890%') and a.accessible_ip=substring_index(b.parameter_value,':',1) or( b.parameter_value ='172.17.140.50:8855' and a.server_id='cluster_226') or (b.parameter_value like '%222.73.121.21%' and a.server_id='cluster_21')"
    sql2="select count(*) as count from service_monitor_param b,server_info a where ( b.parameter_value like '%8855%' or b.parameter_value like '%8801%' or b.parameter_value like '%8890%') and a.accessible_ip=substring_index(b.parameter_value,':',1) or( b.parameter_value ='172.17.140.50:8855' and a.server_id='cluster_226') or (b.parameter_value like '%222.73.121.21%' and a.server_id='cluster_21')"
    if(search=='parameter_name'):
        sql += " and b.parameter_name like '%" + value + "%'"
        sql2 += " and b.parameter_name like '%" + value + "%'"
    if(search=='parameter_value'):
        sql += " and b.parameter_value like '%" + value + "%'"
        sql2 += " and b.parameter_value like '%" + value + "%'"
    if(search=='status'):
        if '启动' in value:
            value = '0'
        if '关闭' in value:
            value = '1'
        sql += " and b.status like '%" + value + "%'"
        sql2 += " and b.status like '%" + value + "%'"
    sql += " order by a.server_id "
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB1()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    conn,cur=ShareMethod.views.connDB1()
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'parameter_name':row[1],'parameter_value':row[2],'status':row[3],'insert_time':row[4]})
    print(table_list)
    return render_to_response('Portselect.html',locals())
    
    
def insert(req):

    operatorName=req.session.get('username')
    parameter_name=req.REQUEST.get('parameter_name','0')
    parameter_value=req.REQUEST.get('parameter_value','0')
    status=req.REQUEST.get('status','0')
    print(status)
    
    if req.method == 'POST':
        sql="insert into service_monitor_param(parameter_name,parameter_value,status,insert_time,update_time) values ('"+parameter_name+"','" + parameter_value +"','"+status+"',now(),now())"
        print(sql)
        try:
            conn,cur=ShareMethod.views.connDB1()
            result=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur) 
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"op："+operatorName)
            print("123")
            return HttpResponseRedirect('../FailureMessage.do?message=MonitorPort/insert.do')
        ShareMethod.views.InfoLog(sql+"op："+operatorName)
        req.session['sql'] = parameter_value 
        return HttpResponseRedirect('../SuccessMessage.do?message=MonitorPort/insert.do')
    else:
        return render_to_response('Portinsert.html',locals())
        
 
def update(req):
    id=req.REQUEST.get('id',0)
    conn,cur=ShareMethod.views.connDB1()
    ShareMethod.views.exeQuery(cur,"select * from service_monitor_param where sn="+str(id))
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'parameter_name':row[1],'parameter_value':row[2],'status':row[3]})
    print(table_list)
    return render_to_response('Portedit.html',{'table_list':table_list})

def modify(req):
    id=req.REQUEST.get('id',0)
    operatorName=req.session.get('username')
    parameter_name=req.REQUEST.get('parameter_name','0')
    parameter_value=req.REQUEST.get('parameter_value','0')
    status=req.REQUEST.get('status','0')
    conn,cur=ShareMethod.views.connDB1()
    sql="update service_monitor_param set parameter_name='"+parameter_name+"',parameter_value='"+parameter_value+"',status='"+status+"',update_time='now()' where sn="+str(id)
    print(sql)
    try:
        conn,cur=ShareMethod.views.connDB1()
        result=ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=MonitorPort/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=MonitorPort/select.do')
