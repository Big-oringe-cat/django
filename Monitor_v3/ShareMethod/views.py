from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger ,InvalidPage
import pymysql
import logging
import socket

if  socket.gethostname() == 'alarm-kvm.zhaowei':
    filename_info="/hskj/web/apache/htdocs/Monitor_v3_doc/Monitor_v3/info.log"
    filename_error="/hskj/web/apache/htdocs/Monitor_v3_doc/Monitor_v3/error.log"
else:
    filename_info="E:\workspace\Monitor_v3_doc\Monitor_v3\info.log"
    filename_error="E:\workspace\Monitor_v3_dco\Monitor_v3\error.log"
   
def InfoLog(message):
    format='%(asctime)s - %(levelname)s - %(message)s'
    #curDate = datetime.date.today() - datetime.timedelta(days=0)
    ##dateTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logging.basicConfig(filename=filename_info, level=logging.INFO , format=format)
    logging.info(message)
    
def ErrorLog(message):
    format='%(asctime)s - %(pathname)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    #curDate = datetime.date.today() - datetime.timedelta(days=0)
    logging.basicConfig(filename=filename_error, level=logging.ERROR , format=format)
    logging.error(message)
    
def connDB():
    if socket.gethostname() == 'alarm-kvm.zhaowei':
        conn=  pymysql.connect(host='172.17.140.9',port=3306,user='notice_plate',passwd='hskj&U*I(O1207',db='monitor_v3',charset='utf8')
    else:
        conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='monitor_server',charset='utf8')
    try:
        conn.ping()
    except:
        conn.close()
        conn=  pymysql.connect(host='172.17.140.9',port=3306,user='notice_plate',passwd='hskj&U*I(O1207',db='monitor_v3',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_12():
    conn=  pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='z1f7r3',db='monitor',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_13():
    conn=  pymysql.connect(host='192.168.130.11',port=3306,user='root',passwd='z1f7r3',db='duty',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_14():
    conn=  pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='z1f7r3',db='monitor_ping',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)

def connDB1():
    if socket.gethostname() == 'alarm-kvm.zhaowei':
        conn=  pymysql.connect(host='172.17.140.9',port=3306,user='notice_plate',passwd='hskj&U*I(O1207',db='super_plate',charset='utf8')
    else:
        conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='monitor_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB2():
    if socket.gethostname() == 'alarm-kvm.zhaowei':
        conn=  pymysql.connect(host='172.17.140.9',port=3306,user='notice_plate',passwd='hskj&U*I(O1207',db='remote_bak_server',charset='utf8')
    else:
        conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='monitor_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_cm():
    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='provinces_test_cm',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_un():
    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='provinces_test_un',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_cdma():
    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='spcard',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
#def connDB_cdma1():
#    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='provinces_test_cdma1',charset='utf8')
#    cur = conn.cursor()
#    return (conn,cur)
def connDB_auto():
    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='sms_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_yw(server,dbname,port):
    conn=  pymysql.connect(host=server,port=port,user='remote_query',passwd='20141024',db=dbname,charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB_RS():
    conn=  pymysql.connect(host='127.0.0.1',user='root',passwd='z1f7r3',db='repository',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)

def exeQuery(cur,sql):
    cur.execute(sql)
    return(cur)
def exeUpdate(cur,sql):
    sta=cur.execute(sql)
    return (sta)
def exeDelete(cur,sql):
    sta = cur.execute(sql)
    return(sta)
def exeInsert(cur,sql):
    cur.execute(sql)
    return(cur)
def connClose(conn,cur):
    cur.close()
    conn.close()   
      
def pagination(sql,pageType,curPage,allPostCounts):  
    
    ONE_PAGE_OF_DATA = 10
    after_range_num = 5   
    befor_range_num = 4
    allPage = int(allPostCounts / ONE_PAGE_OF_DATA) #页数
    remainPost = allPostCounts % ONE_PAGE_OF_DATA   #最后一页的数据
    if remainPost > 0:
        allPage += 1
    print(allPage)  
    if allPage <= 9:
        pageList = range(1,allPage+1)
    else:
        if curPage >= after_range_num:
            if curPage+after_range_num+1 > allPage:
                pageList = range(curPage-befor_range_num,allPage+1)
            else:
                pageList = range(curPage-befor_range_num,curPage+after_range_num+1)
        else:
            if after_range_num+1 > allPage:
                pageList = range(1,allPage+1)
            else:
                pageList = range(1,curPage+after_range_num+1)
            
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
        
    startPos = (curPage-1)*ONE_PAGE_OF_DATA
    print(startPos)
    table_list = [] 
    sql += " limit "+str(startPos)+","+str(ONE_PAGE_OF_DATA)
    print(sql)
    return table_list,allPage,curPage,allPostCounts,pageList,sql
    
def pagination1(sql,pageType,curPage,allPostCounts):  
    
    ONE_PAGE_OF_DATA = 15
    after_range_num = 5   
    befor_range_num = 4
    allPage = int(allPostCounts / ONE_PAGE_OF_DATA)
    remainPost = allPostCounts % ONE_PAGE_OF_DATA
    if remainPost > 0:
        allPage += 1
    print(allPage)  
    if curPage >= after_range_num:
        if curPage+after_range_num+1 > allPage:
            pageList = range(curPage-befor_range_num,allPage+1)
        else:
            pageList = range(curPage-befor_range_num,curPage+after_range_num+1)
    else:
        if after_range_num+1 > allPage:
            pageList = range(1,allPage+1)
        else:
            pageList = range(1,curPage+after_range_num+1)
            
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
        
    startPos = (curPage-1)*ONE_PAGE_OF_DATA
    print(startPos)
    table_list = [] 
    sql += " limit "+str(startPos)+","+str(ONE_PAGE_OF_DATA)
    print(sql)
    return table_list,allPage,curPage,allPostCounts,pageList,sql

def pagination2(sql,pageType,curPage,allPostCounts):  
    
    ONE_PAGE_OF_DATA = 2000
    after_range_num = 5   
    befor_range_num = 4
    allPage = int(allPostCounts / ONE_PAGE_OF_DATA)
    remainPost = allPostCounts % ONE_PAGE_OF_DATA
    if remainPost > 0:
        allPage += 1
    print(allPage)  
    if curPage >= after_range_num:
        if curPage+after_range_num+1 > allPage:
            pageList = range(curPage-befor_range_num,allPage+1)
        else:
            pageList = range(curPage-befor_range_num,curPage+after_range_num+1)
    else:
        if after_range_num+1 > allPage:
            pageList = range(1,allPage+1)
        else:
            pageList = range(1,curPage+after_range_num+1)
            
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
        
    startPos = (curPage-1)*ONE_PAGE_OF_DATA
    print(startPos)
    table_list = [] 
    sql += " limit "+str(startPos)+","+str(ONE_PAGE_OF_DATA)
    print(sql)
    return table_list,allPage,curPage,allPostCounts,pageList,sql

def role_sn(username):
    sql="select a.permission_role_sn from permission_user_role a, admin_user b where a.admin_id=b.admin_id and (a.permission_role_sn=6 or  a.permission_role_sn=8 or a.permission_role_sn=4) and b.admin_name='"+username+"'"
    conn,cur=connDB1()
    exeQuery(cur,sql)
    connClose(conn,cur)
    role='1'
    for row in cur:
        role=row[0]
    if username == '吴伟杰' or username == '吴云' or username == '仉晓甜' or username == '郭小蕾' or username == '黄振根' or username == '叶军跃' or username == '张阿明':
        role = 4
    return role
def index(req):
    username = req.session.get('username','未登录')
    if username == "未登录":
        return HttpResponseRedirect('login')       
    role=role_sn(username)
    req.session['role'] = role
    if role == 6 or role ==8:
        return render_to_response('index1.html',locals())
    elif role == 4:
        return render_to_response('index.html',locals())
    else:
        return render_to_response('test1.html',locals())
#    return render_to_response('index.html',{'username':username})

def SuccessMessage(req):
    message=req.REQUEST.get("message")
    return render_to_response('SuccessMessage.html',{'message':message})
def FailureMessage(req):
    message=req.REQUEST.get("message")
    return render_to_response('FailureMessage.html',{'message':message})
