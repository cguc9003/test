from django.forms import ModelForm,Form
from .models import Thread,Response
from django import forms
class Thread_create(forms.Form):#すれたてフォーム
    """
    class Meta:
        model=Thread
        fields=['title','tag']
        """
    data=[
       ("ゲーム", 'ゲーム'),("プログラミング", 'プログラミング'), ("麻雀", '麻雀'),("映画", '映画'),("その他の雑談", 'その他の雑談'), ("一発ネタ", '一発ネタ')
        ]
    title=forms.CharField(widget=forms.Textarea)
    tag=forms.ChoiceField(choices=data,widget=forms.widgets.Select)
class Response_create(forms.Form):#レスポンス投稿フォーム
    name=forms.CharField(required=False)  
    sentence=forms.CharField(widget=forms.Textarea)


class FindThread(forms.Form):#タグ検索フォーム
   data=[
       ("ゲーム", 'ゲーム'),("プログラミング", 'プログラミング'), ("麻雀", '麻雀'),("映画", '映画'),("その他の雑談", 'その他の雑談'), ("一発ネタ", '一発ネタ')
   ]
   choice=forms.ChoiceField( choices=data,widget=forms.widgets.Select)
