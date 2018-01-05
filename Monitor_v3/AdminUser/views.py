from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import paramiko

def LogQuery(req):
    if req.method == 'POST':
        nowDate = time.strftime('%Y-%m-%d')
        startTime = req.REQUEST.get('startTime',nowDate)
        search1 = req.REQUEST.get('search1','0')
        search2 = req.REQUEST.get('search2','0')
        logName="/hskj/web/apache/htdocs/Monitor_v3_doc/Monitor_v3/info.log"
        if startTime == "":
           command = "grep -a '"+search1+"' "+logName+" | grep -a '"+search2+"'|sort -nr"
        else: 
           command = "grep -a '"+startTime+"' "+logName+" | grep -a '"+search1+"' | grep -a '"+search2+"'"
        table_list = []
        try:
           s = paramiko.SSHClient()
           s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
           s.connect(hostname="192.168.130.11",port=22,username="bjywb",password="ywb*scnb",timeout=10)
           stdin,stdout,stderr = s.exec_command(command)
        except IOError as e:
           print (e)
        for result in stdout.readlines():
            table_list.append({'content':result})

        return render_to_response("LogQuery.html",locals())
    else:
        return render_to_response("LogQuery.html",locals())

def insert(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            
            admin_id=req.REQUEST.get('admin_id','0')
            admin_name=req.REQUEST.get('admin_name','0')
            admin_pwd=req.REQUEST.get('admin_pwd','0')
            status=req.REQUEST.get('status','0')
            sql="insert into admin_user(admin_id,admin_name,admin_pwd,status,insert_time,update_time) values ('"+admin_id+"','" + admin_name +"','"+admin_pwd+"',"+str(status)+",'"+NowTime+"','"+NowTime+"')"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=AdminUser/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=AdminUser/insert.do')
        else:
            return render_to_response('AUinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,admin_id,admin_name,admin_pwd,status from admin_user where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'admin_id':row[1],'admin_name':row[2],'admin_pwd':row[3],'status':row[4]})
    print(table_list)
    return render_to_response('AUedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    admin_id=req.REQUEST.get('admin_id','0')
    admin_name=req.REQUEST.get('admin_name','0')
    admin_pwd=req.REQUEST.get('admin_pwd','0')
    status=req.REQUEST.get('status','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update admin_user set admin_id='"+admin_id+"',admin_name='"+admin_name+"',admin_pwd='"+admin_pwd+"',status="+str(status)+",update_time='"+NowTime+"'  where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=AdminUser/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=AdminUser/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select sn,admin_id,admin_name,status,insert_time,update_time from admin_user where 1 =1 "
    sql2="select count(*) from admin_user where 1=1 "
    if(search=='admin_name'):
        sql += " and admin_name = '" + value + "'"
        sql2 += " and admin_name = '" + value + "'"
    if(search=='admin_id'):
        sql += " and admin_id = '" + value + "'"
        sql2 += " and admin_id = '" + value + "'"
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
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
        table_list.append({'id':row[0],'admin_id':row[1],'admin_name':row[2],'status':row[3],'insert_time':row[4],'update_time':row[5]})
    return render_to_response('AUselect.html',locals())
