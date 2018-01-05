from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views
from django.http.response import HttpResponseRedirect


def login(req):
        if req.method == 'POST':
            admin_id=req.REQUEST.get('admin_id','0')
            admin_pwd=req.REQUEST.get('admin_pwd','0')
            print(admin_id)
            print(admin_pwd)
            sql="select admin_id,admin_pwd,admin_name from admin_user where admin_id='"+admin_id+"' and status=0"
            print(sql)

            conn,cur=ShareMethod.views.connDB1()
            ShareMethod.views.exeQuery(cur,sql) 
            ShareMethod.views.connClose(conn,cur) 
            user={}
            for row in cur:
                user = {'admin_id':row[0],'admin_pwd':row[1],'admin_name':row[2]}
            if  user:
                if admin_pwd == user['admin_pwd']:
                    admin_name = user['admin_name']
                    user_name = admin_name
                    admin_id = user['admin_id']
                    req.session['username'] = admin_name 
                    req.session['admin_id'] = admin_id
                    username = req.session.get('username','未登录')
                    return HttpResponseRedirect('index.do')
                else:
                    return render_to_response('login.html',{'passwordMsg':"密码输入错误!"})
            else:
                return render_to_response('login.html',{'usernameMsg':"账号输入错误!"})
        else:
            return render_to_response('login.html')

def logout(req):
    try:
        del req.session['username']
        return render_to_response('login.html',{})   
    except Exception as e:
        return render_to_response('login.html',{})


def login2(req):
        user_id=req.REQUEST.get('user_id','0')
        print(user_id)
        sql="select user_id,user_name from user_info where user_id='"+user_id+"' and  status=0"
        print(sql)
        conn,cur=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur,sql) 
        ShareMethod.views.connClose(conn,cur) 
        user={}
        for row in cur:
            user = {'user_id':row[0],'user_name':row[1]}
        print(user)
        if  user:
            return HttpResponse(user['user_name'])
                     
        else:
            return HttpResponse("1")
