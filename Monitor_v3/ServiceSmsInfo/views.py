from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
    
def insert(req,conn,cur,conn2,cur2,html,redirect):
        operatorName=req.session.get('username')
        if req.method == 'POST':
            td_code=req.REQUEST.get('td_code','0')
            code=req.REQUEST.get('code','0')
            msg_content=req.REQUEST.get('msg_content','0')
            commport = req.POST.getlist('CommPort','0')
            dest_terminal_id=""
            try:

                for cport in commport:
                    sql2="select mobile,province from phone_card where commport="+str(cport)
                    print(sql2)
                    ShareMethod.views.exeQuery(cur2,sql2)
                    for mobile in cur2:
                        dest_terminal_id=mobile[0]
                        #province=mobile[1]
                    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
                    sql="insert into service_sms_info (td_code,dest_terminal_id,msg_content,insert_time,update_time,code)  values ('"+td_code+"','"+dest_terminal_id+"','"+msg_content+"','"+NowTime+"','"+NowTime+"','"+code+"')"
                    print(sql)
                    SqlResult=ShareMethod.views.exeInsert(cur,sql)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message='+redirect)
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message='+redirect)
        else:
            conn_auto,cur_auto=ShareMethod.views.connDB_auto()
            sql_td="select substring_index(thread_param,'#',1)  from thread_controller where status=3 "
            ShareMethod.views.exeQuery(cur_auto,sql_td)
            ShareMethod.views.connClose(conn_auto,cur_auto)
            tdList=[]
            for row1 in cur_auto:
                print (row1)
                tdList.append({'td_code':row1[0]})            
            sql="select province,mobile,commport from phone_card order by commport"  
            ShareMethod.views.exeQuery(cur2,sql)
            provinceNames=[]
            for row in cur2:
                provinceNames.append({'province':row[0],'mobile':row[1],'commport':row[2]})
            print(provinceNames)
            ShareMethod.views.connClose(conn2,cur2)
            return render_to_response(html,locals())
        
def insert_un(req):
    html='SSIinsert_un.html'
    redirect = 'ServiceSmsInfo/insert_un.do'
    conn,cur=ShareMethod.views.connDB_auto()
    conn2,cur2=ShareMethod.views.connDB_un()
    return insert(req,conn,cur,conn2,cur2,html,redirect)

def insert_cm(req):
    html='SSIinsert_cm.html'
    redirect = 'ServiceSmsInfo/insert_cm.do'
    conn,cur=ShareMethod.views.connDB_auto()
    conn2,cur2=ShareMethod.views.connDB_cm()
    return insert(req,conn,cur,conn2,cur2,html,redirect)

def insert_cdma(req):
    html='SSIinsert_cdma.html'
    redirect = 'ServiceSmsInfo/insert_cdma.do'
    conn,cur=ShareMethod.views.connDB_auto()
    conn2,cur2=ShareMethod.views.connDB_cdma()
    return insert(req,conn,cur,conn2,cur2,html,redirect)
