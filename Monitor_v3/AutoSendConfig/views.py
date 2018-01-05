#coding:utf-8
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os
def insert(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            td_type=req.REQUEST.get('td_type','0')
            td_code=req.REQUEST.get('td_code','0')
            td_sp_number=req.REQUEST.get('td_sp_number','0')
            td_sign=req.REQUEST.get('td_sign','0')
            gate_ip=req.REQUEST.get('gate_ip','0')
            gate_port=req.REQUEST.get('gate_port','0')
            gate_user=req.REQUEST.get('gate_user','0')
            gate_pwd=req.REQUEST.get('gate_pwd','0')
            gate_corp_code=req.REQUEST.get('gate_corp_code','0')
            gate_server_id=req.REQUEST.get('gate_server_id','0')
            gate_max_connect=req.REQUEST.get('gate_max_connect','0')
            gate_max_speed=req.REQUEST.get('gate_max_speed','0')
            sgip_node_id=req.REQUEST.get('sgip_node_id','3000099050')
            sgip_local_port=req.REQUEST.get('sgip_local_port','0')
            if td_type == "cmpp":
                thread_name = "cmppSendByNioThread"
                app_name = "sendThread"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_corp_code+"#"+gate_user+"#"+gate_pwd+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect
                print (thread_param)
            if td_type == "smgp":
                thread_name = "smgp30nioSendThread"
                app_name = "smgpSend"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_user+"#"+gate_pwd+"#"+gate_corp_code+"#"+gate_server_id+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect
                print (thread_param)
            if td_type == "sgip":
                thread_name = "sgipSendThread"
                app_name = "sgipSend"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_user+"#"+gate_pwd+"#"+gate_corp_code+"#"+gate_server_id+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect+"#"+sgip_node_id+"#"+td_sp_number+"#"+sgip_local_port
                print (thread_param)                
            sql=""
            status=req.REQUEST.get('status','0')
            sql2="select max(thread_id) from thread_controller"
            try:
                conn,cur=ShareMethod.views.connDB_auto()
                conn2,cur2=ShareMethod.views.connDB_auto()
                print(sql)
                ShareMethod.views.exeQuery(cur2,sql2)
                for row in cur2:
                    if row[0]:
                        thread_id = int(row[0])+1
                    else:
                        thread_id = 1
                sql="insert into thread_controller(thread_name,thread_id,status,thread_param,thread_type,group_id,app_name) values ('"+thread_name+"'," + str(thread_id) +","+str(1)+",'"+thread_param+"',"+str(1)+","+str(0)+",'"+app_name+"')"
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=AutoSendConfig/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=AutoSendConfig/select.do')
        else:
            return render_to_response('ASCinsert.html')

def update(req):
        id=req.REQUEST.get('id',0)
        print(id)
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            td_type=req.REQUEST.get('td_type','0')
            sn=req.REQUEST.get('id','0')
            td_code=req.REQUEST.get('td_code','0')
            td_sp_number=req.REQUEST.get('td_sp_number','0')
            td_sign=req.REQUEST.get('td_sign','0')
            gate_ip=req.REQUEST.get('gate_ip','0')
            gate_port=req.REQUEST.get('gate_port','0')
            gate_user=req.REQUEST.get('gate_user','0')
            gate_pwd=req.REQUEST.get('gate_pwd','0')
            gate_corp_code=req.REQUEST.get('gate_corp_code','0')
            gate_server_id=req.REQUEST.get('gate_server_id','0')
            gate_max_connect=req.REQUEST.get('gate_max_connect','0')
            gate_max_speed=req.REQUEST.get('gate_max_speed','0')
            sgip_node_id=req.REQUEST.get('sgip_node_id','0')
            sgip_local_port=req.REQUEST.get('sgip_local_port','0')
            status1=req.REQUEST.get('status1')
            if td_type == "移动":
                thread_name = "cmppSendByNioThread"
                app_name = "sendThread"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_corp_code+"#"+gate_user+"#"+gate_pwd+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect
                print (thread_param)
            if td_type == "电信":
                thread_name = "smgp30nioSendThread"
                app_name = "smgpSend"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_user+"#"+gate_pwd+"#"+gate_corp_code+"#"+gate_server_id+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect
                print (thread_param)
            if td_type == "联通":
                thread_name = "sgipSendThread"
                app_name = "sgipSend"
                thread_param = td_code+"#"+gate_ip+"#"+gate_port+"#"+gate_user+"#"+gate_pwd+"#"+gate_corp_code+"#"+gate_server_id+"#"+td_sign+"#"+gate_max_speed+"#"+gate_max_connect+"#"+sgip_node_id+"#"+td_sp_number+"#"+sgip_local_port
                print (thread_param)                
            sql=""
            status=req.REQUEST.get('status',0)
            status2=int(status)+2
            try:
                conn,cur=ShareMethod.views.connDB_auto()
                conn2,cur2=ShareMethod.views.connDB_auto()
                print(sql)
                if str(status2) == status1:
                    sql="update  thread_controller set thread_param='"+thread_param+" where sn = "+str(sn)
                else:
                    if status == '1':
                        thread_type = '0'
                        sql="update  thread_controller set thread_param='"+thread_param+"',status="+status+",thread_type="+thread_type+" where sn = "+str(sn)
                    else:
                        sql="update  thread_controller set thread_param='"+thread_param+"',status="+status+" where sn = "+str(sn)
                SqlResult=ShareMethod.views.exeUpdate(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=AutoSendConfig/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            #return render_to_response('tiaoshi.html',locals())
            return HttpResponseRedirect('../SuccessMessage.do?message=AutoSendConfig/select.do')
        else:
            conn,cur=ShareMethod.views.connDB_auto()
            ShareMethod.views.exeQuery(cur,"select sn,thread_name,thread_param,app_name,status,thread_type from thread_controller where sn="+str(id))
            ShareMethod.views.connClose(conn,cur)
            table_list = []
            for row in cur:
                table_list.append({'id':row[0],'thread_name':row[1],'thread_param':row[2],'app_name':row[3],'status':row[4],'thread_type':row[5]})
                tread_param=row[2].split('#')
                print(table_list)
            sn=row[0]
            if row[1]=="cmppSendByNioThread":
                td_type="移动"
                td_code=tread_param[0]
                gate_ip=tread_param[1]
                gate_port=tread_param[2]
                gate_corp_code=tread_param[3]
                gate_user=tread_param[4]
                gate_pwd=tread_param[5]
                td_sign=tread_param[6]
                gate_max_speed=tread_param[7]
                gate_max_connect=tread_param[8]
                return render_to_response('ASCedit.html',locals())
            if row[1]=="smgp30nioSendThread":
                td_type="电信"
                td_code=tread_param[0]
                gate_ip=tread_param[1]
                gate_port=tread_param[2]
                gate_corp_code=tread_param[5]
                gate_user=tread_param[3]
                gate_pwd=tread_param[4]
                gate_server_id=tread_param[6]
                td_sign=tread_param[7]
                gate_max_speed=tread_param[8]
                gate_max_connect=tread_param[9]
                return render_to_response('ASCedit.html',locals())
            if row[1]=="sgipSendThread":
                td_type="联通"
                td_code=tread_param[0]
                gate_ip=tread_param[1]
                gate_port=tread_param[2]
                gate_corp_code=tread_param[5]
                gate_user=tread_param[3]
                gate_pwd=tread_param[4]
                gate_server_id=tread_param[6]
                td_sign=tread_param[7]
                gate_max_speed=tread_param[8]
                gate_max_connect=tread_param[9]
                sgip_node_id=tread_param[10]
                td_sp_number=tread_param[11]
                sgip_local_port=tread_param[12]
                return render_to_response('ASCedit.html',locals())

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    thread_name=req.REQUEST.get('thread_name','0')
    thread_param=req.REQUEST.get('thread_param','0')
    app_name=req.REQUEST.get('app_name','0')
    status=req.REQUEST.get('status','0')
    thread_type=req.REQUEST.get('thread_type','0')
    print("---------------------"+status)
    sql=""
    if thread_type == '1':
        if status == '6':
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "',status=4  where sn="+id
        else:
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "'  where sn="+id
    else:
        if status == '3':
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "',status=1,thread_type=1  where sn="+id   
        else:
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "'  where sn="+id
        
    try:
        conn,cur=ShareMethod.views.connDB_auto()
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=AutoSendConfig/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=AutoSendConfig/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB_auto()
    sql= "select * from thread_controller where 1 =1 "
    sql2="select count(*) from thread_controller where 1=1 "
    if(search=='thread_param'):
        sql += " and thread_param like '%" + value + "%'"
        sql2 += " and thread_param like '%" + value + "%'"
    sql += " order by status asc"
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_auto()
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
        table_list.append({'id':row[0],'thread_name':row[1],'thread_id':row[2],'status':row[3],'thread_param':row[4],'thread_type':row[5],'group_id':row[6],'app_name':row[7]})
    return render_to_response('ASCselect.html',locals())

def option(req):
    option_file='/hskj/Deliver32Send/deliver.properties'
    if req.method == 'POST':
        sp_number=req.REQUEST.get('sp_number',0)
        yw_code=req.REQUEST.get('yw_code',0)
        msg_content=req.REQUEST.get('msg_content',0)
        f=open(option_file,'w+')
        f.write('table_name=deliver_sms_info\nsp_number='+sp_number+'\nyw_code='+yw_code+'\nmsg_content='+msg_content+'\n')
        return render_to_response('ASCoption.html',locals())
    else:
        f=open(option_file)
        line=f.readlines()
        f.close()
        print(line)
        line0=line[0].split('=')
        line1=line[1].split('=')
        line2=line[2].split('=')
        line3=line[3].split('=')
        return render_to_response('ASCoption.html',{'yw_code':line2[1],'sp_number':line1[1],'msg_content':line3[1],'table_name':line0[1]})
