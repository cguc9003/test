from django.test import TestCase,Client
from .models import Thread,Response
import datetime
from django.urls import reverse
class Thread_Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (thread1,thread2)=cls.create_thread()
        cls.create_response(thread1,thread2)


    @classmethod
    def create_thread(cls):
        #スレッドを4つ作成
        Thread(tag="プログラミング",date=datetime.datetime.now(),title="test").save()
        Thread(tag="麻雀",date=datetime.datetime.now(),title="test2").save()
        Thread(tag="麻雀",date=datetime.datetime.now(),title="test3").save()
        Thread(tag="映画",date=datetime.datetime.now(),title="test4").save()
        thread1=Thread.objects.filter(tag='麻雀').first()
        thread2=Thread.objects.filter(tag='映画').first()
        return (thread1,thread2)

    @classmethod
    def create_response(cls,thread1,thread2):
        #test2にpost1 test4にpost2
        num=int(Response.objects.filter(thread=thread1).count())+1
        Response(sentence="test2_body",thread=thread1,name="base",date=datetime.datetime.now(),num=num).save()

        num=int(Response.objects.filter(thread=thread2).count())+1
        Response(sentence="test4_body",thread=thread2,name="base4",date=datetime.datetime.now(),num=num).save()

        num=int(Response.objects.filter(thread=thread2).count())+1
        Response(sentence="test4_body",thread=thread2,name="base4.1",date=datetime.datetime.now(),num=num).save()
        
        
   

    def test_thread_check(self):
        cnt=Thread.objects.all().count()
        
        self.assertEqual(cnt,4)
        self.assertEqual(Thread.objects.filter(tag='麻雀').count(),2)
        self.assertEqual(Thread.objects.filter(tag='麻雀').first().title,"test2")
        self.assertEqual((Response.objects.get(thread=Thread.objects.filter(tag='麻雀').first())).sentence,"test2_body")
        self.assertEqual(Response.objects.all().count(),3)
        
        reaction=self.client.get(reverse('index'))
        self.assertIs(reaction.status_code,200)
        self.assertContains(reaction,'test4')
        thread_1=self.client.get(reverse('detail',kwargs={'thread_id':2}))
        self.assertIs(thread_1.status_code,200)
        self.assertContains(thread_1,'test2_body')
        create=self.client.get(reverse('create'))
        self.assertIs(create.status_code,200)
        response_thread_1=self.client.get(reverse('res',kwargs={'thread_id':2}))
        self.assertIs(response_thread_1.status_code,200)
        

        
