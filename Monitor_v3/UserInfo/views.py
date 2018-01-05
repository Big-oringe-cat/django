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
            
            user_id=req.REQUEST.get('user_id','0')
            user_name=req.REQUEST.get('user_name','0')
            mobile=req.REQUEST.get('mobile','0')
            email=req.REQUEST.get('email','0')
            status=req.REQUEST.get('status','0')
            sql="insert into user_info(user_id,user_name,mobile,email,insert_time,status) values ('"+user_id+"','" + user_name +"','"+mobile+"','"+email+"','"+NowTime+"',"+str(status)+")"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=UserInfo/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=UserInfo/insert.do')
        else:
            return render_to_response('UIinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,user_id,user_name,mobile,email,insert_time,status from user_info where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'user_id':row[1],'user_name':row[2],'mobile':row[3],'email':row[4],'insert_time':row[5],'status':row[6]})
    print(table_list)
    return render_to_response('UIedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    user_id=req.REQUEST.get('user_id','0')
    user_name=req.REQUEST.get('user_name','0')
    mobile=req.REQUEST.get('mobile','0')
    email=req.REQUEST.get('email','0')
    status=req.REQUEST.get('status','0')
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update user_info set user_id='"+user_id+"',user_name='"+user_name+"',mobile='"+mobile+"',email='"+email+"',status="+str(status)+"  where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=UserInfo/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=UserInfo/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select sn,user_id,user_name,mobile,email,insert_time,status from user_info where 1 =1 "
    sql2="select count(*) from user_info where 1=1 "
    if(search=='user_name'):
        sql += " and user_name = '" + value + "'"
        sql2 += " and user_name = '" + value + "'"
    if(search=='user_id'):
        sql += " and user_id = '" + value + "'"
        sql2 += " and user_id = '" + value + "'"
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
        table_list.append({'id':row[0],'user_id':row[1],'user_name':row[2],'mobile':row[3],'email':row[4],'insert_time':row[5],'status':row[6]})
    return render_to_response('UIselect.html',locals())
