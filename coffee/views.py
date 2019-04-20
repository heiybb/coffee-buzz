
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from coffee.models import Article
from django.core.paginator import Paginator
from coffee.models import Product
from coffee.models import OrderItem
from django import forms
from coffee.models import Staff
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.contrib.auth.hashers import make_password, check_password
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate



# Create your views here.


def hello_world(request):
    return HttpResponse("hello clara")


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title:%s, brief_content:%s,content:%s, ' \
                 'article_id:%s, publish_date:%s' % (title, brief_content, content, article_id, publish_date)

    return HttpResponse(return_str)


def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1

    #all_article = Article.objects.all()
    #top5_article_list = Article.objects.order_by('-publish_date')[:5]

    # change above like this
    all_article = Article.objects.get_queryset().order_by('article_id')
    top5_article_list = Article.objects.get_queryset().order_by('-publish_date')[:5]

    paginator = Paginator(all_article, 3)
    page_article_list = paginator.page(page)
    page_num = paginator.num_pages

    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page

    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'index.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num+1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top5_article_list': top5_article_list
                  })


def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_article = None
    next_article = None
    previous_index = 0
    next_index = 0
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1

        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    return render(request, 'detail.html',
                  {
                      'curr_article': curr_article,
                      'previous_article': previous_article,
                      'next_article': next_article
                  })


def products_display(request):
    all_products = Product.objects.all()
    return render(request, 'products_display.html',
                  {
                      'all_products': all_products
                  })


def barista_page(request):
    all_order_item = OrderItem.objects.get_queryset().order_by('-created_at')
    return render(request, "barista.html",
                  {
                      "all_order_item": all_order_item
                  })


def register(request):
    """
    receive data
    check data
    register processing
    return response

    :param request:
    :return:
    """

    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        allow = request.POST.get('allow')
        email = request.POST.get('email')

        if not all([username,password,password2]):
            return render(request, 'register.html', {'errmsg': 'data not complete'})

        if password != password2:
            return render(request, 'register.html', {'errmsg': 'password is not the same'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': 'should be agree'})

        if Staff.objects.filter(staff_username=username).exists():
            return render(request, 'register.html', {'errmsg': 'user name is exist'})

        if Staff.objects.filter(staff_email=email).exists():
            return render(request, 'register.html', {'errmsg': 'email is exist'})

        staff = Staff()
        staff.staff_username = username
        staff.staff_password = make_password(password)
        staff.staff_email = email
        staff.is_active = False
        staff.save()

        # active account via email, it should contain user token
        # should contain user info, and should encode info
        # generate active token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': staff.staff_id}
        token = serializer.dumps(info)
        token = token.decode('utf8')

        # send the email,
        # subject = "welcome"
        # message = ""
        # html_message = "<a href='http://127.0.0.1:8000/blog/active/%s'>
        # http://127.0.0.1:8000/blog/active/%s</a>"%(token, token)
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # send_mail(subject, message, sender, receiver,html_message=html_message)

        # return redirect('/coffee/index')
        return redirect('/coffee/login')


def active(request, token):
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        staff_id = info['confirm']

        staff = Staff.objects.get(staff_id=staff_id)
        staff.is_active = True
        staff.save()

        return redirect('/coffee/login')

    except SignatureExpired as e:
        return HttpResponse('active link has expired')


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # password = make_password(password)

        if not all([password, email]):
            return render(request, 'login.html', {'errmsg':'data not complete'})

        if Staff.objects.filter(staff_email=email).exists():
            staff = Staff.objects.get(staff_email=email)
            if check_password(password, staff.staff_password):
                return redirect('/coffee/barista')
            else:
                return render(request, 'login.html', {'errmsg': 'email or password is wrong'})
        else:
            return render(request, 'login.html', {'errmsg':'email or password is wrong'})



def get_staff(request):
    return render(request, 'staff.html')





















