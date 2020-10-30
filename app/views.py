from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from .models import Thread,Response
from .forms import Thread_create,Response_create,FindThread
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
#from twoch_project.urls import res
#version Django            3.0.4  Python 3.8.1
def paginate_queryset(request, queryset, count):#ページネーション関数(request,分けたいオブジェクト,何個ずつに分けるか)

    paginator = Paginator(queryset, count)
    page = request.GET.get("page")
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def index(request):
    thread = Thread.objects.order_by('-id')
    page_obj = paginate_queryset(request,thread, 8)
    context = {
        'threads': page_obj.object_list,
        'page_obj':page_obj,
        'form':FindThread(),
        'thread_tag':"指定なし",
    }
    if (request.method=='POST'):#タグ検索をされたときの処理
        ch=request.POST.get('choice')
        thread=Thread.objects.filter(tag=ch).order_by('-id')
        page_obj = paginate_queryset(request, thread, 8)
        params={
            'threads': page_obj.object_list,
            'thread_tag':ch,
            'form':FindThread(),
            'page_obj':page_obj,
        }
        return render(request, 'app/index.html', params)

    else:#普通にきどうしたときのホーム画面
        return render(request, 'app/index.html', context)


def create_thread(request):#スレッド作成画

    if (request.method=='POST'):
        title=request.POST.get('title')#ここから55までスレッド作成の処理
        tag=request.POST.get('tag')
        time=datetime.datetime.now()
        threads = Thread(title=title,tag=tag,date=time)
        threads.save()
        thread_count = Thread.objects.count()

        if thread_count>49:#スレッドの数が50以上なら最も古いものを消す
            old=Thread.objects.earliest('id')
            old.delete()

        new= Thread.objects.latest('id')#ここからスレッドを立てた際そのスレッドのレスポンス作成画面へ飛ぶ処理
        thread_new_id=new.id
        redirect_url = reverse('res', kwargs={'thread_id':thread_new_id})
        return redirect (redirect_url)#スレッドを立てた際そのスレッドのレスポンス作成画面へ飛ぶ処理

        
    else:
        form=Thread_create
        return render(request,'app/thread_create.html',{'form':form}) 

def thread_detail(request,thread_id):#実際のスレッドの画面
    
    thread = get_object_or_404(Thread, id=thread_id)
    responses = Response.objects.filter(thread=thread)#レスポンスとスレッドを結び付け
    page_obj = paginate_queryset(request, responses, 50)
    
    return render(request,'app/thread_detail.html',{'responses':page_obj.object_list, 'page_obj':page_obj,'thread':thread}) 


def response_create(request,thread_id):#レスポンス作成画面
    
    thread = get_object_or_404(Thread, id=thread_id)
    form=Response_create(request.POST)
    
    if (request.method=='POST'):#レスポンス投稿時の処理
      #ここからレスポンス内容を保存
        sentence=request.POST.get('sentence')
        thread=request.POST.get('thread_id')
        name=request.POST.get('name')
        if name=="":
            name="名無し"
        time=datetime.datetime.now()
        num=int(Response.objects.filter(thread=Thread(id=thread_id)).count())+1 #スレッド内でのレスポンスの番号を割り振る
        responses = Response(name=name,sentence=sentence,thread=Thread(id=thread_id),date=time,num=num)
        responses.save()
        redirect_url = reverse('detail', kwargs={'thread_id':thread_id})#書き込んだスレッドのdetailまで返す処理
        return redirect (redirect_url)

    else:
        return render(request,'app/response_create.html',{'form':form,'thread':thread}) 



# Create your views here.

# Create your views here.
