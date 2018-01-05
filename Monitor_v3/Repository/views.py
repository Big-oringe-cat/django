from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect

import ShareMethod.views

def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts', '0'))
    pageType = req.REQUEST.get('pageType', '0')
    curPage = int(req.REQUEST.get('curPage', '1'))
    allPage = int(req.REQUEST.get('allPage', '1'))
    sql='select * from yunwei'
    sql2='select count(*) from yunwei'
    if allPostCounts == 0:
        conn2, cur2 = ShareMethod.views.connDB_RS()
        ShareMethod.views.exeQuery(cur2, sql2)
        for row in cur2:
            allPostCounts = row[0]
            ShareMethod.views.connClose(conn2, cur2)
    table_list, allPage, curPage, allPostCounts, pageList, sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    conn,cur = ShareMethod.views.connDB_RS()
    ShareMethod.views.exeQuery(cur, sql)
    table_list=[]
    for row in cur:
        table_list.append({'sn':row[0],'yw_type':row[1],'type':row[2],'Question':row[3],'Answer':row[4],'update_time':str(row[5]),'status':row[6]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('select.html',locals())

def insert(req):
    if req.method == 'POST':
        operatorName=req.session.get('username')
        yw_type=req.REQUEST.get('yw_type','')
        type=req.REQUEST.get('type','')
        Question=req.REQUEST.get('Question','')
        Answer=req.REQUEST.get('Answer','')
        status=req.REQUEST.get('status','')
        sql="insert into yunwei(yw_type,type,Question,Answer,update_time,status)values('"+yw_type+"','"+type+"','"+Question+"','"+Answer+"',now(),"+status+")"
        try:
            conn,cur=ShareMethod.views.connDB_RS()
            SqlResult=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Repository/select')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Repository/select')
    else:
        return render_to_response('insert.html',locals())

def delete(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn',0)
    try:
        conn,cur=ShareMethod.views.connDB_RS()
        sql="delete from yunwei where id="+str(sn)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur)
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=Repository/select')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=Repository/select')

def update(req):
    operatorName=req.session.get('username')
    sn=req.REQUEST.get('sn','')
    if req.method=='POST':
        yw_type=req.REQUEST.get('yw_type','')
        type=req.REQUEST.get('type','')
        Question=req.REQUEST.get('Question','')
        Answer=req.REQUEST.get('Answer','')
        status=req.REQUEST.get('status','')
        sql1="update yunwei set yw_type='"+yw_type+"',type='"+type+"',Question='"+Question+"',Answer='"+Answer+"',update_time=now(),status="+status+" where id="+str(sn)
        try:
            conn1,cur1=ShareMethod.views.connDB_RS()
            SqlResult=ShareMethod.views.exeUpdate(cur1,sql1)
            ShareMethod.views.connClose(conn1,cur1)
        except Exception as e:
            print(e)
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=Repository/select')
        ShareMethod.views.InfoLog(sql1+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=Repository/select')
    else:
        conn,cur=ShareMethod.views.connDB_RS()
        ShareMethod.views.exeQuery(cur,"select * from yunwei  where id="+str(sn))
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            table_list.append({'sn':row[0],'yw_type':row[1],'type':row[2],'Question':row[3],'Answer':row[4],'status':row[6]})
        return render_to_response('update.html',{'table_list':table_list})
