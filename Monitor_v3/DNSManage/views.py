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
            yw_type=req.REQUEST.get('yw_type','0')
            yw_desc=req.REQUEST.get('yw_desc','0')
            dns_name=req.REQUEST.get('dns_name','0')
            port=req.REQUEST.get('port','0')
            ip=req.REQUEST.get('ip','0')
            insert_time=req.REQUEST.get('insert_time','0')
            update_time=req.REQUEST.get('update_time','0')
            sql="insert into dns_config(yw_type,yw_desc,dns_name,port,ip,insert_time,update_time) values ('"+yw_type+"','" + yw_desc +"','"+dns_name+"','"+port+"','"+ip+"','"+insert_time+"','"+update_time+"')"
            try:
                conn,cur=ShareMethod.views.connDB_12()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=DNSManage/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=DNSManage/insert.do')
        else:
            return render_to_response('DNSinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB_12()
    ShareMethod.views.exeQuery(cur,"select sn,yw_type,yw_desc,dns_name,port,ip,insert_time,update_time from dns_config where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'yw_type':row[1],'yw_desc':row[2],'dns_name':row[3],'port':row[4],'ip':row[5],'insert_time':row[6],'update_time':row[7]})
    print(table_list)
    return render_to_response('DNSedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    yw_type=req.REQUEST.get('yw_type','0')
    yw_desc=req.REQUEST.get('yw_desc','0')
    dns_name=req.REQUEST.get('dns_name','0')
    port=req.REQUEST.get('port','0')
    ip=req.REQUEST.get('ip','0')
    update_time=req.REQUEST.get('update_time','0')
    try:
        conn,cur=ShareMethod.views.connDB_12()
        sql="update dns_config set yw_type='"+yw_type+"',yw_desc='"+yw_desc+"',dns_name='"+dns_name+"',port='"+port+"',ip='"+ip+"',update_time='"+update_time+"' where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=DNSManage/select.do?type=0')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=DNSManage/select.do?type=0') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    type=req.REQUEST.get('type','1')
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value','')
    conn,cur=ShareMethod.views.connDB_12()
    sql= "select sn,yw_type,yw_desc,dns_name,port,ip,insert_time,update_time from dns_config where 1 =1 "
    sql2="select count(*) from dns_config where 1=1 "
    if(search=='yw_type'):
        sql += " and yw_type like '%" + value + "%'"
        sql2 += " and yw_type like '%" + value + "%'"
    if(search=='yw_desc'):
        sql += " and yw_desc like '%" + value + "%'"
        sql2 += " and yw_desc like '%" + value + "%'"
    if(search=='dns_name'):
        sql += " and dns_name like '%" + value + "%'"
        sql2 += " and dns_name like '%" + value + "%'"
    if(search=='port'):
        sql += " and port like '%" + value + "%'"
        sql2 += " and port like '%" + value + "%'"
    if(search=='ip'):
        sql += " and ip like '%" + value + "%'"
        sql2 += " and ip like '%" + value + "%'"
    
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
        table_list.append({'id':row[0],'yw_type':row[1],'yw_desc':row[2],'dns_name':row[3],'port':row[4],'ip':row[5],'insert_time':row[6],'update_time':row[7]})
    if type == "0":
        return render_to_response('DNSselect.html',locals())
    else:
        return render_to_response('DNSselect1.html',locals())
def delete(req): 
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB_12()
    sql="delete from dns_config where sn="+id
    print(sql)
    ShareMethod.views.exeDelete(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    return HttpResponseRedirect('../SuccessMessage.do?message=DNSManage/select.do?type=0') 
        
