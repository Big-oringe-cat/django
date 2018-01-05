from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views

def insert(req):
        operatorName=req.session.get('username')
        if req.method == 'POST':
            config=req.REQUEST.get('config','0')
            
            ip=req.REQUEST.get('ip','0')
            db_name=req.REQUEST.get('db_name','0')
            server_name=req.REQUEST.get('server_name','0')
            status=req.REQUEST.get('status','0')
            server_room=req.REQUEST.get('server_room','0')
            sql="insert into server_info(ip,port,username,password,db_name,server_name,status,server_room) values ('"+ip+"','3306','hs','V1ja89zab','"+db_name+"','"+server_name+"','"+status+"','"+server_room+"')"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                print(username)
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=ServerInfo/insert.do')
            
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            if config=="config":
                return HttpResponseRedirect('CommandConfig.do')
            else:
                return HttpResponseRedirect('../SuccessMessage.do?message=ServerInfo/insert.do')
        else:
            
            return render_to_response('SIinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from server_info where sn="+str(id))
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'ip':row[1],'port':row[2],'username':row[3],'password':row[4],'db_name':row[5],'server_name':row[6],'status':row[7],'server_room':row[8]})
    print(table_list)
    return render_to_response('SIedit.html',{'table_list':table_list})
    

def modify(req):
    id=req.REQUEST.get('id',0)
    operatorName=req.session.get('username')
    ip=req.REQUEST.get('ip','0')
    db_name=req.REQUEST.get('db_name','0')
    server_name=req.REQUEST.get('server_name','0')
    status=req.REQUEST.get('status','0')
    server_room=req.REQUEST.get('server_room','0')
    conn,cur=ShareMethod.views.connDB()
    sql="update server_info set ip='"+ip+"',db_name='"+db_name+"',server_name='"+server_name+"',status="+str(status)+",server_room='"+server_room+"' where sn="+str(id)
    print(sql)
    try:
        conn,cur=ShareMethod.views.connDB()
        result=ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ServerInfo/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ServerInfo/select.do')
        


def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select * from server_info where 1 =1 "
    sql2 = "select count(*) as count from server_info where 1=1"
    if(search=='server_name'):
        sql += " and server_name like '%" + value + "%'"
        sql2 += " and server_name like '%" + value + "%'"
    if(search=='server_room'):
        sql += " and server_room like '%" + value + "%'"
        sql2 += " and server_room like '%" + value + "%'" 
    if(search=='ip'):
        sql += " and ip like '%" + value + "%'"
        sql2 += " and ip like '%" + value + "%'"
    if(search=='port'):
        sql += " and port like '%" + value + "%'"
        sql2 += " and port like '%" + value + "%'"
    if(search=='db_name'):
        sql += " and db_name like '%" + value + "%'"
        sql2 += " and db_name like '%" + value + "%'"
    sql += "order by status desc "
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
        table_list.append({'id':row[0],'ip':row[1],'port':row[2],'username':row[3],'password':row[4],'db_name':row[5],'server_name':row[6],'status':row[7],'server_room':row[8]})
    return render_to_response('SIselect.html',locals())

def CommandConfig(req):
        operatorName=req.session.get('username')
        refer_sn=req.REQUEST.get('serverName','0')
        
        if req.method == 'POST':
            try:
                conn,cur=ShareMethod.views.connDB() 
                sql_sn="select sn from server_info order by sn desc limit 1"
                ShareMethod.views.exeQuery(cur,sql_sn)
                server_sn=0
                for row in cur:
                    server_sn=row[0]
                sql="insert into server_monitor_info(server_sn,monitor_sn,value,mark,frequency,status,group_sn) select "+str(server_sn)+",monitor_sn,value,mark,frequency,status,group_sn from server_monitor_info where server_sn="+str(refer_sn)
                print(sql)
                ShareMethod.views.exeInsert(cur,sql)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                print(e)
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=ServerInfo/CommandConfig.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=ServerInfo/insert.do') 
               
        else:
            try:
                conn,cur=ShareMethod.views.connDB() 
                sql_sn="select sn from server_info order by sn desc limit 1"
                ShareMethod.views.exeQuery(cur,sql_sn)
                server_sn=0
                for row in cur:
                    server_sn=row[0]
                    
                sql="select server_name,sn from server_info where sn !="+str(server_sn)+" order by server_name"  
                print(sql)
                ShareMethod.views.exeQuery(cur,sql)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                print(e)
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=ServerInfo/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            serverNames=[]
            for row in cur:
                serverNames.append({'serverName':row[0],'serverSn':row[1]})
            return render_to_response('CommandConfig.html',{'serverNames':serverNames})
