from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time

def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    print("select * from config_info where sn="+str(id))
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from config_info where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'key':row[1],'value':row[2],'desc_info':row[5]})
    print(table_list)
    return render_to_response('CIedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    key=req.REQUEST.get('key','0')
    value=req.REQUEST.get('value','0')
    desc_info=req.REQUEST.get('desc_info','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update config_info set value='"+value+"',insert_time='"+NowTime+"',desc_info='"+desc_info+"'  where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ConfigInfo/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ConfigInfo/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select sn,`key`,value,desc_info,insert_time from config_info where 1 =1 "
    sql2="select count(*) from config_info where 1=1 "
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
        table_list.append({'id':row[0],'key':row[1],'value':row[2],'desc_info':row[3],'insert_time':row[4]})
    return render_to_response('CIselect.html',locals())
