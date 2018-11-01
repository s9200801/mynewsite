# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect

from myapp import models,forms
from django.template.loader import get_template
from datetime import datetime
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

def index(request,pid=None,del_pass=None):
    if request.user.is_authenticated:
        username=request.user.username
        useremail=request.user.email
        try:
            user=models.User.objects.get(usernamer=username)
            diaries=models.Diary.objects.filter(user=user).order_by('-ddate')
        except:
            pass
    messages.get_messages(request)
    """
    if 'username' in request.session and 'useremail' in request.session:
        username=request.session['username']
        useremail=request.session['useremail']
    """

    polls=models.Poll.objects.all()
    template=get_template('index.html')
    html=template.render(context=locals(),request=request)

    return HttpResponse(html)

def listing(request):
    template=get_template('list.html')
    posts=models.Post.objects.filter(enable=True).order_by('-pub_time')[:150]
    moods=models.Mood.objects.all()
    html=template.render(locals())
    return HttpResponse(html)

def posting(request):
    template=get_template('posting.html')
    moods=models.Mood.objects.all()

    try:
        usid=request.POST['user_id']
        uspass=request.POST['user_pass']
        uspost=request.POST['user_post']
        usmood=request.POST['mood']
    except:
        usid=None
        message='每個欄位都要填寫'
    if usid !=None:
        mood=models.Mood.objects.get(status=usmood)
        post=models.Post.objects.create(mood=mood,nickname=usid,del_pass=uspass,message=uspost)
        post.save()
        message='儲存成功 請記得你的密碼.'
    request_context=RequestContext(request)
    request_context.push(locals())
    html=template.render(context=locals(),request=request)
    return HttpResponse(html)

def contact(request):
    if request.user.is_authenticated:
        username=request.user.username
    if request.method=='POST':
        form=forms.ContactForm(request.POST)
        if form.is_valid():
            message="感謝你的來信"
            user_name=form.cleaned_data['user_name']
            user_city=form.cleaned_data['user_city']
            user_school=form.cleaned_data['user_school']
            user_email=form.cleaned_data['user_email']
            user_message=form.cleaned_data['user_message']

            mail_body=u'''
            網友姓名:{}
            居住城市:{}
            是否在學:{}
            反應意見:{}'''.format(user_name,user_city,user_school,user_message)

            email=EmailMessage('網友意見',mail_body,user_email,['ffkk9200801@gmail.com'])
            email.send()
        else:
            message="請檢查輸入的資訊是否正確"
    else:
        form=forms.ContactForm()
    template=get_template('contact.html')
    html=template.render(context=locals(),request=request)
    return HttpResponse(html)

def post2db(request):
    if request.user.is_authenticated:
        username=request.user.username
        useremail=request.user.email
    messages.get_messages(request)
    if request.method=='POST':
        user=User.objects.get(username=username)
        diary=models.Diary(user=user)
        post_form=forms.DiaryForm(request.POST,instance=diary)
        if post_form.is_valid():
            messages.add_message(request,messages.INFO,"儲存成功")
            post_form.save()
            return HttpResponseRedirect('/')
        else:

            messages.add_message(request,messages.INFO,"每個欄位都要填寫")
    else:
        post_form=forms.DiaryForm()
        messages.add_message(request,messages.INFO,"每個欄位都要填寫")

    template=get_template('post2db.html')

    html=template.render(context=locals(),request=request)

    return HttpResponse(html)

def login(request):
    if request.method=='POST':
        login_form=forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['user_name'].strip()
            login_password=request.POST['password']
            user=authenticate(username=login_name,password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    print("success")
                    messages.add_message(request,messages.SUCCESS,"登入成功")
                    return redirect('/')
                else:
                    messages.add_message(request,messages.WARNING,"帳號未啟用")
            else:
                messages.add_message(request,messages.WARNING,"登入失敗")
            """
            在上面else裡
            try:
                user=models.User.objects.get(name=login_name)
                if user.password==login_password:
                    response=redirect('/')
                    request.session['username']=user.name
                    request.session['useremail']=user.email
                    messages.add_message(request,messages.SUCCESS,"登入成功")
                    return redirect('/')
                else:
                    messages.add_message(request,messages.WARNING,"密碼錯誤")
            except:
                messages.add_message(request,messages.WARNING,"帳號或密碼錯誤")
            """

        else:
            messages.add_message(request,messages.WARNING,'請檢查輸入欄位')
    else:
        login_form=forms.LoginForm()

    template=get_template('login.html')

    html=template.render(context=locals(),request=request)


    return HttpResponse(html)

def logout(request):
    auth.logout(request)
    messages.add_message(request,messages.INFO,"成功登出")
    """
    del request.session['username']
    del request.session['useremail']
    """
    return redirect('/')

@login_required(login_url='/login')
def userinfo(request):
    if request.user.is_authenticated:
        username=request.user.username
        user=User.objects.get(username=username)
        try:
            profile=models.Profile.objects.get(user=user)
        except:
            profile=models.Profile(user=user)
    if request.method=='POST':
        profile_form=forms.ProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            messages.add_message(request,messages.INFO,"個人資料已儲存")
            profile_form.save()
            return HttpResponseRedirect('/userinfo')
        else:
            messages.add_message(request,messages.INFO,"每個欄位都要填寫")
    else:
        profile_form=forms.ProfileForm()
    """
    if 'username' in request.session:
        username=request.session['username']
    else:
        return redirect('/')
    try:
        userinfo=modles.User.objects.get(name=username)
    except:
        pass
        """
    template=get_template('userinfo.html')
    html=template.render(locals())
    return HttpResponse(html)

def poll(request,pollid):
    try:
        poll=models.Poll.objects.get(id=pollid)
    except:
        poll=None
    if poll is not None:
        pollitems=models.PollItem.objects.filter(poll=poll).order_by('-vote')
    template=get_template('poll.html')
    html=template.render(context=locals(),request=request)
    return HttpResponse(html)

def vote(request,pollid,pollitemid):
    try:
        pollitem=models.PollItem.objects.get(id=pollitemid)
    except:
        pollitem=None
    if pollitem is not None:
        pollitem.vote+=1
        pollitem.save()
    target_url='/poll/'+pollid
    return redirect(target_url)

