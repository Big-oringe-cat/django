from django import forms
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

import ShareMethod.views
from tracemalloc import Snapshot

def ping_info(req):
    search1=req.REQUEST.get('search1','')
    search2=req.REQUEST.get('search2','')
    search3=req.REQUEST.get('search3','')
    value=req.REQUEST.get('value','')
    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))
    sql="select sn,server_id,src_ip,dest_ip,dest_type,dest_comment,replace_ip,monitor_level,src_type,flag from ping_info where 1=1 and (server_id like '%" + search1 + "%' or src_ip like '%" + search1 + "%') and (dest_ip like '%" + search2 + "%' or replace_ip like '%" + search2 + "%' or dest_type like '%" + search2 + "%' or dest_comment like '%" + search2 + "%') and (dest_comment like '%" + search3 + "%') order by sn"
    sql2="select count(*) from ping_info where 1=1 and (server_id like '%" + search1 + "%' or src_ip like '%" + search1 + "%') and (dest_ip like '%" + search2 + "%' or replace_ip like '%" + search2 + "%' or dest_type like '%" + search2 + "%' or dest_comment like '%" + search2 + "%') and (dest_comment like '%" + search3 + "%')"
    print(sql2)
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
            ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur = ShareMethod.views.connDB_14()
    ShareMethod.views.exeQuery(cur, sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'server_id':row[1],'src_ip':row[2],'dest_ip':row[3],'dest_type':row[4],'dest_comment':row[5],'replace_ip':row[6],'monitor_level':row[7],'src_type':row[8],'flag':row[9]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('ping_info.html',locals())

def ping_insert(req):
    operatorName=req.session.get('username')
    if req.method == 'POST':
        server_id=req.REQUEST.get('server_id','')
        dest_ip=req.REQUEST.get('dest_ip','')
        dest_type=req.REQUEST.get('dest_type','')
        dest_comment=req.REQUEST.get('dest_comment','')
        monitor_level=req.REQUEST.get('monitor_level','')
        sql2="select replace_ip from replace_info where gate_ip='"+dest_ip+"'"
        conn2,cur2=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur2, sql2)
        replace_ip=""
        for row2 in cur2:
            replace_ip=str(row2[0])
        ShareMethod.views.connClose(conn2, cur2)
        sql1="select server_ip,server_desc from server_info where server_id='"+server_id+"'"
        conn1,cur1=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur1, sql1)
        src_ip=""
        src_type=""
        for row1 in cur1:
            src_ip=str(row1[0])
            src_type=str(row1[1])
        ShareMethod.views.connClose(conn1, cur1)
        sql="insert into ping_info(server_id,src_ip,dest_ip,src_type,dest_type,dest_comment,replace_ip,flag,monitor_level) values ('"+server_id+"','"+src_ip+"','"+dest_ip+"','"+src_type+"','"+dest_type+"','"+dest_comment+"','"+replace_ip+"',1,"+monitor_level+")"
        try:
            conn,cur=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/ping_insert')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/ping_info')
    else:
         sql2="select server_id from server_info"
         conn2,cur2=ShareMethod.views.connDB_14()
         ShareMethod.views.exeQuery(cur2, sql2)
         table_list=[]
         for row2 in cur2:
             table_list.append({'server_id':row2[0]})
         return render_to_response('ping_insert.html',locals())

def ping_delete(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    try:
        conn,cur=ShareMethod.views.connDB_14()
        sql="delete from ping_info where sn="+str(sn)
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/ping_info')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/ping_info')

def ping_update(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn','')
    if req.method=='POST':
        server_id=req.REQUEST.get('server_id','')
        src_ip=req.REQUEST.get('src_ip','')
        dest_ip=req.REQUEST.get('dest_ip','')
        dest_type=req.REQUEST.get('dest_type','')
        src_type=req.REQUEST.get('src_type','')
        dest_comment=req.REQUEST.get('dest_comment','')
        replace_ip=req.REQUEST.get('replace_ip','')
        monitor_level=req.REQUEST.get('monitor_level','')
        sql1="update ping_info set dest_ip='"+dest_ip+"',dest_type='"+dest_type+"',dest_comment='"+dest_comment+"',replace_ip='"+replace_ip+"',monitor_level="+monitor_level+" where sn="+str(sn)
        try:
            conn1,cur1=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/ping_info')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/ping_info')
    else:
        conn,cur=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur,"select * from ping_info  where sn="+str(sn))
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'sn':row[0],'server_id':row[1],'src_ip':row[2],'dest_ip':row[3],'src_type':row[4],'dest_type':row[5],'dest_comment':row[6],'replace_ip':row[7],'monitor_level':str(row[9])})
        return render_to_response('ping_update.html',{'table_list':table_list})


def server_info(req):
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','')

    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))

    sql="select * from server_info where 1=1"
    sql2="select count(*) from server_info where 1=1"

    if(search=='server_ip'):
        sql += " and server_ip like '%" + value + "%'"
        sql2 += " and server_ip like '%" + value + "%'"
    if(search=='private_ip'):
        sql += " and private_ip like '%" + value + "%'"
        sql2 += " and private_ip like '%" + value + "%'"
    if(search=='server_id'):
        sql += " and server_id like '%" + value + "%'"
        sql2 += " and server_id like '%" + value + "%'"
    if(search=='server_desc'):
        sql += " and server_desc like '%" + value + "%'"
        sql2 += " and server_desc like '%" + value + "%'"

   #if search1:
   #    sql +=" and server_ip= '"+search1+"'"
   #    sql2 +=" and server_ip= '"+search1+"'"
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
            ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur = ShareMethod.views.connDB_14()
    ShareMethod.views.exeQuery(cur, sql)

    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'server_ip':row[1],'private_ip':row[2],'server_id':row[3],'server_desc':row[4],'type':row[5],'status':row[6],'domain_name':row[7]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('server_info.html',locals())

def server_insert(req):
    operatorName=req.session.get('username')
    if req.method == 'POST':
        server_ip=req.REQUEST.get('server_ip','')
        private_ip=req.REQUEST.get('private_ip','')
        server_id=req.REQUEST.get('server_id','')
        server_desc=req.REQUEST.get('server_desc','')
        domain_name=req.REQUEST.get('domain_name','')
        sql="insert into server_info (server_ip,private_ip,server_id,server_desc,domain_name) values ('"+server_ip+"','"+private_ip+"','"+server_id+"','"+server_desc+"','"+domain_name+"')"
        sql2="update ping_info set src_type='"+server_desc+"' where src_ip='"+server_ip+"'"
        try:
            conn,cur=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            conn2,cur2=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur2,sql2)
            ShareMethod.views.connClose(conn2,cur2)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/server_insert')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/server_info')
    else:
         return render_to_response('server_insert.html',locals())

def server_delete(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    try:
        conn,cur=ShareMethod.views.connDB_14()
        sql="delete from server_info where sn="+str(sn)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/server_info')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/server_info')

def server_update(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    if req.method=='POST':
        sn=req.REQUEST.get('sn','')
        server_ip=req.REQUEST.get('server_ip','')
        private_ip=req.REQUEST.get('private_ip','')
        server_id=req.REQUEST.get('server_id','')
        server_desc=req.REQUEST.get('server_desc','')
        domain_name=req.REQUEST.get('domain_name','')
        conn1,cur1=ShareMethod.views.connDB_14()
        sql1="update server_info set server_ip='"+server_ip+"',private_ip='"+private_ip+"',server_id='"+server_id+"',server_desc='"+server_desc+"',domain_name='"+domain_name+"' where sn="+str(sn)
        sql2="update ping_info set src_type='"+server_desc+"' where src_ip='"+server_ip+"'"
        try:
            conn1,cur1=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
            conn2,cur2=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur2,sql2)
            ShareMethod.views.connClose(conn2,cur2)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/server_insert')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/server_info')
    else:
        conn,cur=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur,"select * from server_info  where sn="+str(sn))
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'sn':row[0],'server_ip':row[1],'private_ip':row[2],'server_id':row[3],'server_desc':row[4],'type':row[5],'status':row[6],'domain_name':row[7]})
        return render_to_response('server_update.html',locals())

def replace_info(req):
    search1=req.REQUEST.get('search1','')
    value=req.REQUEST.get('value','')
    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))
    sql="select * from replace_info where 1=1"
    sql2="select count(*) from replace_info where 1=1"
    if search1:
        sql +=" and (gate_ip like  '%"+search1+"%' or replace_ip like  '%"+search1+"%')"
        sql2 +=" and (gate_ip like '%"+search1+"%' or replace_ip like  '%"+search1+"%')"
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
            ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur = ShareMethod.views.connDB_14()
    ShareMethod.views.exeQuery(cur, sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'gate_ip':row[1],'replace_ip':row[2]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('replace_info.html',locals())

def replace_insert(req):
    operatorName=req.session.get('username')
    if req.method == 'POST':
        gate_ip=req.REQUEST.get('gate_ip','')
        replace_ip=req.REQUEST.get('replace_ip','')
        sql1="update ping_info set replace_ip='"+replace_ip+"' where dest_ip='"+gate_ip+"'"
        sql="insert into replace_info (gate_ip,replace_ip) values ('"+gate_ip+"','"+replace_ip+"')"
        try:
            conn1,cur1=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeInsert(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
            conn,cur=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/replace_insert')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/replace_info')
    else:
         return render_to_response('replace_insert.html',locals())

def replace_delete(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    try:
        conn,cur=ShareMethod.views.connDB_14()
        sql="delete from replace_info where sn="+str(sn)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/replace_info')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/replace_info')

def replace_update(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    if req.method=='POST':
        gate_ip=req.REQUEST.get('gate_ip','')
        replace_ip=req.REQUEST.get('replace_ip','')
        sql1="update replace_info set gate_ip='"+gate_ip+"',replace_ip='"+replace_ip+"' where sn="+str(sn)
        sql2="update ping_info set replace_ip='"+replace_ip+"' where dest_ip='"+gate_ip+"'"
        try:
            conn1,cur1=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
            conn2,cur2=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur2,sql2)
            ShareMethod.views.connClose(conn2,cur2)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/replace_insert')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/replace_info')
    else:
        conn,cur=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur,"select * from replace_info  where sn="+str(sn))
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'sn':row[0],'gate_ip':row[1],'replace_ip':row[2]})
        return render_to_response('replace_update.html',locals())

def site_info(req):
    search1=req.REQUEST.get('search1','')
    value=req.REQUEST.get('value','')
    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))
    sql="select * from ping_monitor_site  where 1=1"
    sql2="select count(*) from ping_monitor_site where 1=1"
    if search1:
        sql +=" and (server_id like  '%"+search1+"%' or group_name like  '%"+search1+"%')"
        sql2 +=" and (server_id like '%"+search1+"%' or group_name like  '%"+search1+"%')"
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
            ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur = ShareMethod.views.connDB_14()
    ShareMethod.views.exeQuery(cur, sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'group_name':row[1],'server_id':row[2],'server_name':row[3]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('site_info.html',locals())

def site_insert(req):
    operatorName=req.session.get('username')
    if req.method == 'POST':
        group_name=req.REQUEST.get('group_name','')
        server_id=req.REQUEST.get('server_id','')
        server_name=req.REQUEST.get('server_name','')
        sql="insert into ping_monitor_site (group_name,server_id,server_name) values ('"+group_name+"','"+server_id+"','"+server_name+"')"
        try:
            conn,cur=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/site_insert')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/site_info')
    else:
         return render_to_response('site_insert.html',locals())

def site_delete(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    try:
        conn,cur=ShareMethod.views.connDB_14()
        sql="delete from ping_monitor_site where sn="+str(sn)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/site_info')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/site_info')

def site_update(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    if req.method=='POST':
        group_name=req.REQUEST.get('group_name','')
        server_id=req.REQUEST.get('server_id','')
        server_name=req.REQUEST.get('server_name','')
        sql1="update ping_monitor_site set group_name='"+group_name+"',server_id='"+server_id+"',server_name='"+server_name+"'  where sn="+str(sn)
        try:
            conn1,cur1=ShareMethod.views.connDB_14()
            SqlResult=ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Monitor_ping/site_info')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Monitor_ping/site_info')
    else:
        conn,cur=ShareMethod.views.connDB_14()
        ShareMethod.views.exeQuery(cur,"select * from ping_monitor_site  where sn="+str(sn))
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'sn':row[0],'group_name':row[1],'server_id':row[2],'server_name':row[3]})
        return render_to_response('site_update.html',locals())
