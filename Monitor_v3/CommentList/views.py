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
            comment=req.REQUEST.get('comment','0')
            monitor_type=req.REQUEST.get('monitor_type','0')
            sql="insert into comment_list(comment,monitor_type) values ('"+comment+"','" + monitor_type +"')"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=CommentList/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=CommentList/insert.do')
        else:
            return render_to_response('CLinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,comment,monitor_type from comment_list where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'comment':row[1],'monitor_type':row[2]})
    print(table_list)
    return render_to_response('CLedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    comment=req.REQUEST.get('comment','0')
    monitor_type=req.REQUEST.get('monitor_type','0')
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update comment_list set comment='"+comment+"',monitor_type='"+monitor_type+"' where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=CommentList/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=CommentList/select.do') 
        
def select(req):
    role = req.session.get('role','')
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select sn,comment,monitor_type from comment_list where 1 =1 "
    sql2="select count(*) from comment_list where 1=1 "
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='monitor_type'):
        if value == 'LINUX命令':
            sql += " and monitor_type = '1'"
            sql2 += " and monitor_type = '1'"
        else:
            sql += " and monitor_type = '0'"
            sql2 += " and monitor_type = '0'"
    sql += " order by monitor_type"        
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
        table_list.append({'id':row[0],'comment':row[1],'monitor_type':row[2]})
    return render_to_response('CLselect.html',locals())
