from django.db import models


class Thread(models.Model):
    tag_list = (("ゲーム", 'ゲーム'),("プログラミング", 'プログラミング'), ("麻雀", '麻雀'),("映画", '映画'),("その他の雑談", 'その他の雑談'), ("一発ネタ", '一発ネタ'))
    tag = models.TextField(choices=tag_list)#スレッドのタグ
    date = models.DateTimeField(blank=True, null=True)
    title=models.CharField(max_length=100)#スレッドタイトル
    

class Response(models.Model):
    sentence=models.TextField()#レスポンス本分
    thread=models.ForeignKey(Thread,on_delete=models.CASCADE)
    name=models.CharField(max_length=160)#書き込み者の名前　何も入力しなければ名無し
    date = models.DateTimeField(blank=True, null=True)#書き込み日時
    num=models.IntegerField()#スレッド内でのレスナンバー
