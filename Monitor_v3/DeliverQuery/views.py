from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views

def select_auto(req,sql,sql2,conn3,cur3,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    conn,cur=ShareMethod.views.connDB_auto()
#    sql= "select * from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_un.phone_card)  "
#    sql2="select count(*) from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_un.phone_card)  "
    if(search=='src_terminal_id'):
        sql += " and src_terminal_id like '%" + value + "%'"
        sql2 += " and src_terminal_id like '%" + value + "%'"
    if(search=='dest_mobile'):
        sql += " and dest_mobile like '%" + value + "%'"
        sql2 += " and dest_mobile like '%" + value + "%'"
    if(search=='msg_content'):
        sql += " and msg_content like '%" + value + "%'"
        sql2 += " and msg_content like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
            
    sql += " order by insert_time desc "  
    
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
    province=""
    for row in cur:
        sql = "select province from phone_card where mobile='"+row[2]+"'"
        ShareMethod.views.exeQuery(cur3,sql) 
        for row3 in cur3:
            province = row3[0]
        table_list.append({'id':row[0],'dest_mobile':row[3],'src_terminal_id':row[2],'province':province,'msg_content':row[9],'insert_time':row[7]})
    ShareMethod.views.connClose(conn3,cur3) 
    return render_to_response(html,locals())

def select_auto_un(req):
    html="DQselect_auto_un.html"
    sql= "select * from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_un.phone_card) "
    sql2="select count(*) from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_un.phone_card) "
    conn3,cur3=ShareMethod.views.connDB_un()
    return select_auto(req,sql,sql2,conn3,cur3,html)

def select_auto_cm(req):
    html="DQselect_auto_cm.html"
    sql= "select * from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_cm.phone_card) "
    sql2="select count(*) from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_cm.phone_card) "
    conn3,cur3=ShareMethod.views.connDB_cm()
    return select_auto(req,sql,sql2,conn3,cur3,html)

#def select_auto_cdma(req):
#    html="DQselect_auto_cdma.html"
#    sql= "select * from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_cdma.phone_card) "
#    sql2="select count(*) from deliver_sms_info where src_terminal_id in (select mobile from provinces_test_cdma.phone_card) "
#    conn3,cur3=ShareMethod.views.connDB_cdma()
#    return select_auto(req,sql,sql2,conn3,cur3,html)

def select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    sql_1= "select ID,ReceiverMobileNo,Sender,Msg,SendTime,'上行成功' as status  from sendedoutbox where 1=1 "
    sql_2= "select ID,ReceiverMobileNo,Sender,Msg,SendTime,'未上行' as status  from outbox where 1=1 "
    sql_3="select  ID,ReceiverMobileNo,Sender,Msg,SendTime,'上行失败'  as status from badoutbox  where 1=1 "
    sql2="select count(*) from sendedoutbox where 1=1 "
    sql3="select count(*) from outbox where 1=1 "
    sql4="select count(*) from badoutbox where 1=1 "
    if(search=='ReceiverMobileNo'):
        sql_1 += " and ReceiverMobileNo like '%" + value + "%' "
        sql_2 += " and ReceiverMobileNo like '%" + value + "%' "
        sql_3 += " and ReceiverMobileNo like '%" + value + "%' "
        sql2 += " and ReceiverMobileNo like '%" + value + "%' "
        sql3 += " and ReceiverMobileNo like '%" + value + "%' "
        sql4 += " and ReceiverMobileNo like '%" + value + "%' "
    if(search=='Sender'):
        sql_1 += " and Sender like '%" + value + "%' "
        sql_2 += " and Sender like '%" + value + "%' "
        sql_3 += " and Sender like '%" + value + "%' "
        sql2 += " and Sender like '%" + value + "%' "
        sql3 += " and Sender like '%" + value + "%' "
        sql4 += " and Sender like '%" + value + "%' "
    if(search=='Msg'):
        sql_1 += " and Msg like '%" + value + "%' "
        sql_2 += " and Msg like '%" + value + "%' "
        sql_3 += " and Msg like '%" + value + "%' "
        sql2 += " and Msg like '%" + value + "%' "
        sql3 += " and Msg like '%" + value + "%' "
        sql4 += " and Msg like '%" + value + "%' "
    if startTime!=endTime:
        if startTime!='':
            sql_1 +=" and SendTime >='"+startTime+"'"
            sql_2 +=" and SendTime >='"+startTime+"'"
            sql_3 +=" and SendTime >='"+startTime+"'"
            sql2 +=" and SendTime >='"+startTime+"'"
            sql3 +=" and SendTime >='"+startTime+"'"
            sql4 +=" and SendTime >='"+startTime+"'"
        if endTime!='':
            sql_1 +=" and SendTime <='"+endTime+"'"
            sql_2 +=" and SendTime <='"+endTime+"'"
            sql_3 +=" and SendTime <='"+endTime+"'"
            sql2 +=" and SendTime <='"+endTime+"'"
            sql3 +=" and SendTime <='"+endTime+"'"
            sql4 +=" and SendTime <='"+endTime+"'"
    else:
        if startTime!='':
            sql_1 +=" and SendTime like '%"+startTime+"%'"
            sql_2 +=" and SendTime like '%"+startTime+"%'"
            sql_3 +=" and SendTime like '%"+startTime+"%'"
            sql2 +=" and SendTime like '%"+startTime+"%'"
            sql3 +=" and SendTime like '%"+startTime+"%'"
            sql4 +=" and SendTime like '%"+startTime+"%'"
            
    sql=sql_1+" union "+sql_2+" union "+sql_3
    sql += " order by SendTime desc "  
    
    if allPostCounts == 0:
        ShareMethod.views.exeQuery(cur2,sql2)
        ShareMethod.views.exeQuery(cur3,sql3)
        ShareMethod.views.exeQuery(cur4,sql4)
        for row2 in cur2:
            allPostCount1 = row2[0]
        for row3 in cur3:
            allPostCount2 = row3[0]
        for row4 in cur4:
            allPostCount3 = row4[0]
        allPostCounts=int(allPostCount1)+int(allPostCount2)+int(allPostCount3)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'ReceiverMobileNo':row[1],'Sender':row[2],'Msg':row[3],'SendTime':row[4],'status':row[5]})
    ShareMethod.views.connClose(conn,cur) 
    ShareMethod.views.connClose(conn2,cur2) 
    ShareMethod.views.connClose(conn3,cur3) 
    ShareMethod.views.connClose(conn4,cur4) 
    return render_to_response(html,locals())

def select_un(req):
    html='DQselect_un.html'
    conn,cur=ShareMethod.views.connDB_un()
    conn2,cur2=ShareMethod.views.connDB_un()
    conn3,cur3=ShareMethod.views.connDB_un()
    conn4,cur4=ShareMethod.views.connDB_un()
    return select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html)
    
def select_cm(req):
    html='DQselect_cm.html'
    conn,cur=ShareMethod.views.connDB_cm()
    conn2,cur2=ShareMethod.views.connDB_cm()
    conn3,cur3=ShareMethod.views.connDB_cm()
    conn4,cur4=ShareMethod.views.connDB_cm()
    return select(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,html)    

#def select_cdma(req):
#    htmldx='DQselect_cdma.html'
#    conn,cur=ShareMethod.views.connDB_cdma()
#    conn2,cur2=ShareMethod.views.connDB_cdma()
#    conn3,cur3=ShareMethod.views.connDB_cdma()
#    conn4,cur4=ShareMethod.views.connDB_cdma()
#    return selectdx(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,htmldx)

#def select_cdma1(req):
#    htmldx='DQselect_cdma1.html'
#    conn,cur=ShareMethod.views.connDB_cdma1()
#    conn2,cur2=ShareMethod.views.connDB_cdma1()
#    conn3,cur3=ShareMethod.views.connDB_cdma1()
#    conn4,cur4=ShareMethod.views.connDB_cdma1()
#    return selectdx(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,htmldx)

def selectdx(req,conn,cur,conn2,cur2,conn3,cur3,conn4,cur4,htmldx):
    print ("============")
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))

    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    sql= "select SmsIndex,PhoneNumber,SmsContent,RM1,SentSetIndex,status from sentsmstable  where 1 =1 "
    sql2="select count(*) from sentsmstable where 1=1 "
    if(search=='PhoneNumber'):#接入号
        sql += " and PhoneNumber like '%" + value + "%'"
        sql2 += " and PhoneNumber like '%" + value + "%'"
    if(search=='SmsContent'):#内容
        sql += " and SmsContent like '%" + value + "%'"
        sql2 += " and SmsContent like '%" + value + "%'"
    if(search=='SentSetIndex'):#手机号码
        sql3="select commport  from phone_card where mobile="+"'"+str(value)+"'"
        #print(sql3+"\n34343434")
        ShareMethod.views.exeQuery(cur3,sql3)
        SentSetIndex=''
        for commport in cur3:
            SentSetIndex=commport[0]
            sql += " and SentSetIndex = " + str(SentSetIndex)
        #print(sql+"\n1111111")
            sql2 += " and SentSetIndex = " + str(SentSetIndex)
        #print(sql2+"\n222222")
        ShareMethod.views.connClose(conn3,cur3)

    if startTime!=endTime:
        if startTime!='':
            sql +=" and RM1 >='"+startTime+"'"
            sql2 +=" and RM1 >='"+startTime+"'"
        if endTime!='':
            sql +=" and RM1 <='"+endTime+"'"
            sql2 +=" and RM1 <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and RM1 like '%"+startTime+"%'"
            sql2 +=" and RM1 like '%"+startTime+"%'"

    sql += " order by RM1 desc "

    if allPostCounts == 0:
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        #print(sql2+"\n33333333333333")
        ShareMethod.views.connClose(conn2,cur2)

    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)

    ShareMethod.views.exeQuery(cur,sql)
    table_list = []
    for row in cur:
        mobile=""
        province = ""
        commport = int(row[4])+2
        #print(row)
        sql4="select mobile,province from phone_card where commport="+str(commport)
        print (sql4)
        ShareMethod.views.exeQuery(cur4,sql4)
        for row4 in cur4:
            mobile=row4[0]
            province = row4[1]
            print(province)
        table_list.append({'SmsIndex':row[0],'PhoneNumber':row[1],'SentSetIndex':mobile,'province':province,'SmsContent':row[2],'SendTime':row[3],'status':row[5]})
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn4,cur4)
    return render_to_response(htmldx,locals())
