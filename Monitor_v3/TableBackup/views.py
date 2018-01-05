# -*- coding: utf-8 -*-
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
            
            remote_ip=req.REQUEST.get('remote_ip','0')
            remote_db=req.REQUEST.get('remote_db','0')
            remote_bak_data_tables=req.REQUEST.get('remote_bak_data_tables','0')
            status=req.REQUEST.get('status','0')
            sql="insert into remote_db_spec_config(remote_ip,remote_port,remote_db,remote_bak_data_tables,status,insert_time,update_time) values ('"+remote_ip+"','3306','" + remote_db +"','"+remote_bak_data_tables+"',"+str(status)+",'"+NowTime+"','"+NowTime+"')"
            try:
                conn,cur=ShareMethod.views.connDB2()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=TableBackup/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=TableBackup/insert.do')
        else:
            return render_to_response('TBinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB2()
    ShareMethod.views.exeQuery(cur,"select id,remote_ip,remote_db,remote_bak_data_tables,status from remote_db_spec_config where id="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'remote_ip':row[1],'remote_db':row[2],'remote_bak_data_tables':row[3],'status':row[4]})
    print(table_list)
    return render_to_response('TBedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    remote_ip=req.REQUEST.get('remote_ip','0')
    remote_db=req.REQUEST.get('remote_db','0')
    remote_bak_data_tables=req.REQUEST.get('remote_bak_data_tables','0')
    status=req.REQUEST.get('status','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn,cur=ShareMethod.views.connDB2()
        sql="update remote_db_spec_config set remote_ip='"+remote_ip+"',remote_db='"+remote_db+"',remote_bak_data_tables='"+remote_bak_data_tables+"',status="+str(status)+",update_time='"+NowTime+"'  where id="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=TableBackup/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=TableBackup/select.do') 

def delete(req): 
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    try:
        conn,cur=ShareMethod.views.connDB2()
        sql="delete from remote_db_spec_config where id="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=TableBackup/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=TableBackup/select.do') 

def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    
    sql= "select * from remote_db_spec_config where 1 =1 "
    sql2 = "select count(*) as count from remote_db_spec_config where 1=1 "
    if(search=='remote_ip'):
        sql += " and remote_ip like '%" + value + "%'"
        sql2 += " and remote_ip like '%" + value + "%'"
    if(search=='remote_db'):
        sql += " and remote_db like '%" + value + "%'"
        sql2 += " and remote_db like '%" + value + "%'"
    if(search=='remote_bak_data_tables'):
        sql += " and remote_bak_data_tables like '%" + value + "%'"
        sql2 += " and remote_bak_data_tables like '%" + value + "%'"
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB2()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur=ShareMethod.views.connDB2()
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'remote_ip':row[1],'remote_db':row[3],'remote_bak_data_tables':row[5],'status':row[6],'insert_time':row[7],'remote_last_bak_time':row[4],'interval_time':row[9]})
    return render_to_response('TBselect.html',locals())
