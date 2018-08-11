from django.shortcuts import render, redirect
from facebook.models import Article,Page, Comment
# Create your views here.

def play(request):
    return render(request,'play.html')

def layout(request):
    return render(request,'layout.html')

count=0
def play2(request):
    ryujaehyun = '유재현'
    global count
    count=count+1
    age=20
    if  age>19 :
        status = '성인'
    else:
        status = '청소년'
    diary = ['오늘은 날씨가 맑았다. - 4월 3일', '미세머지가 너무 심하다. (4월 2일)', '비가 온다. 4월 1일에 작성']

    return render(request,'play2.html',{'name':ryujaehyun, 'cnt':count,'stat':status,'diary':diary})

def profile(request):
    return render(request,'profile.html')

def event(request):
    ryujaehyun = '유재현'
    age=21
    if age >= 20:
        status = '성인'
    else:
        status = '청소년'
    global count
    count = count + 1

    if count is 7:
        result = '당첨!입니다'
    else:
        result = '꽝...입니다'



    return render(request,'event.html',{'name':ryujaehyun,'stat':status, 'cnt':count,'res':result})

def newsfeed(request):
    articles=  Article.objects.all()
    return render(request,'newsfeed.html',{'articles':articles})

def detail_feed(request,pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        Comment.objects.create(
            article=article,
            author=request.POST["nickname"],
            text=request.POST["reply"],
            password=request.POST["password"]
        )
    return render(request,'detail_feed.html',{'feed':article})

def pages(request):
    pages = Page.objects.all()
    return render(request,'pages.html',{'pages':pages})

def new_feed(request):
    if request.method == 'POST':
        if request.POST['author']!='' and request.POST['title']!='' and request.POST['content']!='' and request.POST['password']!='':
            new_article = Article.objects.create (
                author=request.POST['author'],
                title=request.POST['title'],
                text=request.POST['content']+ ' - 추신: 감사합니다',
                password=request.POST['password']
            )
        return redirect(f'/feed/{new_article.pk}')
    return render(request,'new_feed.html')

def remove_feed(request, pk):
    article=Article.objects.get(pk=pk)

    if request.method == 'POST' :
        if request.POST['password'] == article.password :
            article.delete()
            return redirect('/')
        else:
            return redirect('/fail/')
    return render(request,'remove_feed.html',{'feed':article})

def edit_feed(request, pk):
    article= Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password :
            article.author = request.POST['author']
            article.title = request.POST['title']
            article.text = request.POST['content']
            article.save()
            return redirect(f'/feed/{article.pk}')

    else :
        return redirect('/fail/')
    return render(request,'edit_feed.html',{'feed':article})