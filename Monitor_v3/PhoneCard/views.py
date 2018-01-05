from django.template.loader import get_template
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import ShareMethod.views

def select(req,conn,cur,conn2,cur2,html):
    role = req.session.get('role',1)
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    sql= "select * from phone_card where 1 =1 "
    sql2="select count(*) from phone_card where 1=1 "
    if(search=='province'):
        sql += " and province like '%" + value + "%'"
        sql2 += " and province like '%" + value + "%'"
    if(search=='mobile'):
        sql += " and mobile like '%" + value + "%'"
        sql2 += " and mobile like '%" + value + "%'"
    if(search=='commport'):
        sql += " and commport = '" + value + "'"
        sql2 += " and commport = '" + value + "'"
    sql += " order by commport "  
    if allPostCounts == 0:
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
        table_list.append({'id':row[0],'province':row[1],'mobile':row[2],'commport':row[3],'card_type':row[4]})
    return render_to_response(html,locals())

def select_un(req):
    html='PCselect_un.html'
    conn,cur=ShareMethod.views.connDB_un()
    conn2,cur2=ShareMethod.views.connDB_un()
    return select(req,conn,cur,conn2,cur2,html)
    
def select_cm(req):
    html='PCselect_cm.html'
    conn,cur=ShareMethod.views.connDB_cm()
    conn2,cur2=ShareMethod.views.connDB_cm()
    return select(req,conn,cur,conn2,cur2,html)

def select_cdma(req):
    html='PCselect_cdma.html'
    conn,cur=ShareMethod.views.connDB_cdma()
    conn2,cur2=ShareMethod.views.connDB_cdma()
    return select(req,conn,cur,conn2,cur2,html)
#def select_cdma1(req):
#    html='PCselect_cdma1.html'
#    conn,cur=ShareMethod.views.connDB_cdma1()
#    conn2,cur2=ShareMethod.views.connDB_cdma1()
#    return select(req,conn,cur,conn2,cur2,html)

def update_un(req):
    html='update_un.html'
    conn,cur=ShareMethod.views.connDB_un()
    return update(req,conn,cur,html)
def update_cm(req):
    html='update_cm.html'
    conn,cur=ShareMethod.views.connDB_cm()
    return update(req,conn,cur,html)
def update_cdma(req):
    html='update_cdma.html'
    conn,cur=ShareMethod.views.connDB_cdma()
    return update(req,conn,cur,html)
def update_cdma1(req):
    html='update_cdma1.html'
    conn,cur=ShareMethod.views.connDB_cdma1()
    return update(req,conn,cur,html)

def update(req,conn,cur,html):
    id=req.REQUEST.get('id',0)
    if req.method == 'POST':
        operatorName=req.session.get('username')
        mobile=req.REQUEST.get('mobile','')
        card_type=req.REQUEST.get('card_type','')
        sql1="update phone_card set mobile='"+mobile+"',card_type='"+card_type+"' where id="+id
        try:
            ShareMethod.views.exeUpdate(cur,sql1)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=PhoneCard/select_un')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        ShareMethod.views.connClose(conn,cur)
        return HttpResponseRedirect('../SuccessMessage.do?message=PhoneCard/select_un')
    else:
        sql= "select * from phone_card where id="+id
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'id':row[0],'province':row[1],'mobile':row[2],'commport':row[3],'card_type':row[4]})
        return render_to_response(html,locals())
