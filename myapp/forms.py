# -*- coding: utf-8 -*-
from django import forms
from myapp import models
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    CITY=[
        ['TP','Taipei'],
        ['TY','Taoyuang'],
        ['TC','Taichung'],
        ['TN','Tainan'],
        ['KS','Kaohsiung'],
        ['NA','Others'],
    ]
    user_name=forms.CharField(label='姓名',max_length=50,initial='')
    user_city=forms.ChoiceField(label='居住城市',choices=CITY)
    user_school=forms.BooleanField(label='是否在學(勾選為是)',required=False)
    user_email=forms.EmailField(label='電子信箱')
    user_message=forms.CharField(label='意見',widget=forms.Textarea)
    
class PostForm(forms.ModelForm):
    captcha=CaptchaField(label='確定你不是機器人')
    class Meta:
        model=models.Post
        fields=['mood','nickname','message','del_pass']
        labels={
            'mood':'現在心情',
            'nickname':'你的暱稱',
            'message':'心情留言',
            'del_pass':'設定密碼',
        }
        
class LoginForm(forms.Form):
    user_name=forms.CharField(label='姓名',max_length=10)
    password=forms.CharField(label='密碼',widget=forms.PasswordInput())
    
class DateInput(forms.DateInput):
    input_type='date'
    
class DiaryForm(forms.ModelForm):
    
    class Meta:
        model=models.Diary
        fields=['budget','weight','note','ddate']
        widgets={
            'ddate':DateInput()
        }
        labels={
            'budget':'今日花費',
            'weight':'今日體重',
            'note':'心情留言',
            'ddate':'日期',
        }
        
        
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model=models.Profile
        fields=['height','male','website']
        labels={
            'height':'身高',
            'male':'是男',
            'website':'個人網站',
        }
        
