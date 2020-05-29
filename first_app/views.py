from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from django.utils import timezone
from datetime import timedelta
from .models import *


def index(request):
    if 'total_spent' not in request.session:
        request.session['total_spent'] = 0
    if 'products_ordered' not in request.session:
        request.session['products_ordered'] = 0
    return render(request, 'index.html')
    context = {
        "register": Register.objects.all()
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def adduser(request):
    errors = Register.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newuser = Register.objects.create(
            fname=request.POST['fname'], email=request.POST['email'], password=pw_hash)
        request.session['loggedinID'] = newuser.id
        messages.success(request, "Successfully Registered!")
        return redirect('/')


def login(request):
    errors = Register.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = Register.objects.filter(email=request.POST['email'])
    logged_user = user[0]
    request.session['loggedinID'] = logged_user.id
    return redirect('/blog')


def blog(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    context = {
        "loggedinuser": loggedinuser,
        "post": Post.objects.all(),
        "comment": Comments.objects.all()
    }
    return render(request, "blog.html", context)


def post_message(request):
    user = Register.objects.get(id=request.session['loggedinID'])
    message = Post.objects.create(
        message=request.POST["message"], register=user)
    return redirect('/blog')


def post_comment(request, messageid):
    onemessage = Post.objects.get(id=messageid)
    user = Register.objects.get(id=request.session['loggedinID'])
    comment = Comments.objects.create(
        comment=request.POST["comment"], register=user, post=onemessage)
    print(request.POST['comment'])
    return redirect('/blog')


def shop(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    context = {
        "loggedinuser": loggedinuser,
        "myitems": Product.objects.filter(Q(uploader=loggedinuser)),
    }
    return render(request, "shop.html", context)


def additem(request):
    print(request.POST)
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    newitem = Product.objects.create(
        item=request.POST['item'], itemprice=request.POST['itemprice'], uploader=loggedinuser)
    return redirect("/shop")


def deleteMessage(request, messageid):
    message = Post.objects.get(id=messageid)
    message.delete()
    return redirect("/blog")


def deleteItem(request, itemId):
    item = Product.objects.get(id=itemId)
    item.delete()
    return redirect('/shop')


def deleteComment(request, postid):
    comment = Comments.objects.get(id=postid)
    comment.delete()
    return redirect("/blog")


def checkout(request):
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    ready_time = timezone.now() + timedelta(hours=1)
    items = Product.objects.filter(Q(uploader=loggedinuser))
    sum = 0
    for item in items:
        sum = sum + item.itemprice
        print(sum)
    context = {
        "loggedinuser": loggedinuser,
        "Product": Product.objects.filter(Q(uploader=loggedinuser)),
        "time": ready_time,
        "price" : sum
    }
    return render(request, "checkout.html", context)


def check(request):
    return render(request, "checkout.html")


def destroy(request):
    request.session.clear()
    return redirect("/")
