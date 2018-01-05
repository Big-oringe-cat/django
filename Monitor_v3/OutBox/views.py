from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time

def insert(req,conn,cur,conn2,cur2,html,f_redirect,s_redirect):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            sp_number=req.REQUEST.get('ReceiverMobileNo','0')
            msg_content=req.REQUEST.get('Msg','0')
            commport = req.POST.getlist('CommPort','0')
            try:

                for cport in commport:
                    sql2="select mobile,province from phone_card where commport="+str(cport)
                    print(sql2)
                    ShareMethod.views.exeQuery(cur2,sql2)
                    for mobile in cur2:
                        phone=mobile[0]
                        province=mobile[1]
                    sender=phone+"("+province+") com"+cport
                    print(sender)
                    sql="insert into outbox(Sender,ReceiverMobileNo,Msg,SendTime,CommPort) values ('"+sender+"','" + sp_number +"','"+msg_content+"','"+NowTime+"',"+str(cport)+")"
                    SqlResult=ShareMethod.views.exeInsert(cur,sql)
                    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect(f_redirect)
            return HttpResponseRedirect(s_redirect)
        else:
                        
            sql="select province,mobile,commport from phone_card order by commport"  
            ShareMethod.views.exeQuery(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            provinceNames=[]
            for row in cur:
                provinceNames.append({'province':row[0],'mobile':row[1],'commport':row[2]})
            print(provinceNames)
            return render_to_response(html,{'provinceNames':provinceNames})
        
def insert_un(req):
    html='OBinsert_un.html'
    s_redirect='../SuccessMessage.do?message=OutBox/insert_un.do'
    f_redirect='../FailureMessage.do?message=OutBox/insert_un.do'
    conn,cur=ShareMethod.views.connDB_un()
    conn2,cur2=ShareMethod.views.connDB_un()
    return insert(req,conn,cur,conn2,cur2,html,f_redirect,s_redirect)

def insert_cm(req):
    html='OBinsert_cm.html'
    s_redirect='../SuccessMessage.do?message=OutBox/insert_cm.do'
    f_redirect='../FailureMessage.do?message=OutBox/insert_cm.do'
    conn,cur=ShareMethod.views.connDB_cm()
    conn2,cur2=ShareMethod.views.connDB_cm()
    return insert(req,conn,cur,conn2,cur2,html,f_redirect,s_redirect)

def insert_cdma(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        conn,cur=ShareMethod.views.connDB_cdma()
        if req.method == 'POST':
            sp_number=req.REQUEST.get('smsNumber','0')
            msg_content=req.REQUEST.get('smsContent','0')
            commport = req.POST.getlist('commPort','0')
            conn2,cur2=ShareMethod.views.connDB_cdma()
            try:

                for cport in commport:
                    sql2="select mobile,province from phone_card where commport="+str(cport)
                    print(sql2)
                    ShareMethod.views.exeQuery(cur2,sql2)
                    for mobile in cur2:
                        phone=mobile[0]
                        province=mobile[1]
                    #sender=phone+"("+province+")"
                    indexport=int(cport)-2
                    sql="insert into sms_send (smsNumber,smsContent) values ('"+sp_number+"','" + msg_content +"')"
                    result=ShareMethod.views.exeInsert(cur,sql)
                    print(sql)
                    print(result)
                    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=OutBox/insert_cdma.do')
            return HttpResponseRedirect('../SuccessMessage.do?message=OutBox/insert_cdma.do')
        else:
                        
            sql="select province,mobile,commport from phone_card order by commport"  
            ShareMethod.views.exeQuery(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            provinceNames=[]
            for row in cur:
                provinceNames.append({'province':row[0],'mobile':row[1],'commport':row[2]})
            print(provinceNames)
            return render_to_response('OBinsert_cdma.html',{'provinceNames':provinceNames})
        
def insert1_cdma(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        conn,cur=ShareMethod.views.connDB_cdma1()
        if req.method == 'POST':
            sp_number=req.REQUEST.get('PhoneNumber','0')
            msg_content=req.REQUEST.get('SmsContent','0')
            commport = req.POST.getlist('CommPort','0')
            conn2,cur2=ShareMethod.views.connDB_cdma1()
            try:

                for cport in commport:
                    sql2="select mobile,province from phone_card where commport="+str(cport)
                    print(sql2)
                    ShareMethod.views.exeQuery(cur2,sql2)
                    for mobile in cur2:
                        phone=mobile[0]
                        province=mobile[1]
                    sender=phone+"("+province+")"
                    indexport=int(cport)-2
                    sql="insert into sendingsmstable (PhoneNumber,SmsContent,RM1,RM2,SendModem) values ('"+sp_number+"','" + msg_content +"','"+NowTime+"','"+sender+"',"+str(indexport)+")"
                    result=ShareMethod.views.exeInsert(cur,sql)
                    print(sql)
                    print(result)
                    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=OutBox/insert_cdma1.do')
            return HttpResponseRedirect('../SuccessMessage.do?message=OutBox/insert_cdma1.do')
        else:
                        
            sql="select province,mobile,commport from phone_card order by commport"  
            ShareMethod.views.exeQuery(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            provinceNames=[]
            for row in cur:
                provinceNames.append({'province':row[0],'mobile':row[1],'commport':row[2]})
            print(provinceNames)
            return render_to_response('OBinsert_cdma1.html',{'provinceNames':provinceNames})
