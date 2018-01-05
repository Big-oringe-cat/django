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
            group_name=req.REQUEST.get('group_name','0')
            user_all_check=req.POST.getlist('UserName','0')
            delimiter = ','
            user_sn=delimiter.join(user_all_check)
            status=req.REQUEST.get('status','0')
            sql="insert into user_group(group_name,user_sn,status,insert_time) values ('"+group_name+"','" + user_sn +"',"+str(status)+",'"+NowTime+"')"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=UserGroup/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=UserGroup/insert.do')
        else:
            conn,cur=ShareMethod.views.connDB()
            sql="select user_name,sn from user_info"  
            ShareMethod.views.exeQuery(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            UserNames=[]
            for row in cur:
                UserNames.append({'userName':row[0],'userSn':row[1]})
            return render_to_response('UGinsert.html',{'userNames':UserNames})


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,group_name,user_sn,status from user_group where sn="+str(id))
    ShareMethod.views.connClose(conn,cur) 
    conn1,cur1=ShareMethod.views.connDB()
    sql="select user_name,sn from user_info"  
    ShareMethod.views.exeQuery(cur1,sql)
    ShareMethod.views.connClose(conn1,cur1)
    UserNames=[]
    for row in cur1:
        UserNames.append({'userName':row[0],'userSn':str(row[1])})
    print(UserNames)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'group_name':row[1],'user_sn':row[2].split(','),'status':row[3]})
    print(table_list)
    return render_to_response('UGedit.html',{'table_list':table_list,'UserNames':UserNames})
    

def modify(req):
    group_name=req.REQUEST.get('group_name','0')
    user_all_check=req.POST.getlist('UserName','0')
    delimiter = ','
    status=req.REQUEST.get('status','0')
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    a=[]
    for i in range(len(user_all_check)):
        sql1="select user_name from user_info where sn="+user_all_check[i-1]
        conn1,cur1=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur1,sql1)
        ShareMethod.views.connClose(conn1,cur1)
        for row1 in cur1:
            a.append(row1[0])
            if group_name == row1[0]:
                b=user_all_check[i-1]
                user_all_check[i-1]=user_all_check[0]
                user_all_check[0]=b
    user_sn=delimiter.join(user_all_check)
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update user_group set group_name='"+group_name+"',user_sn='"+user_sn+"',status="+str(status)+" where sn="+str(id)
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=UserGroup/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=UserGroup/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn1,cur1=ShareMethod.views.connDB()
    conn2,cur2=ShareMethod.views.connDB()
    sql= "select * from user_group where 1 =1 "
    sql3= "select count(*) from user_group where 1 =1 "
    if(search=='group_name'):
        sql += " and group_name like '%" + value + "%'"
        sql3 += " and group_name like '%" + value + "%'"
    if allPostCounts == 0:
        conn3,cur3=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur3,sql3)
        for row in cur3:
            allPostCounts = row[0]
        print(sql3)
        ShareMethod.views.connClose(conn3,cur3)
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur1,sql) 
    table_list = []
    userSn_list = []
    for row in cur1:
        userName_list = []
        user_list=row[2].split(",")
        for user_sn in user_list:
            user_sql="select user_name from user_info where sn="+str(user_sn)
            ShareMethod.views.exeQuery(cur2,user_sql)
            for name in cur2:
                userName_list.append(name[0])
        delimiter = ','
        user_name = delimiter.join(userName_list)
        print(user_name)
        table_list.append({'id':row[0],'group_name':row[1],'user_name':user_name,'status':row[3],'insert_time':row[4],})
    ShareMethod.views.connClose(conn1,cur1)
    ShareMethod.views.connClose(conn2,cur2)
    return render_to_response('UGselect.html',locals())
