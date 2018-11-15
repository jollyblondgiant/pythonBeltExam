
from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    request.session['servercheck'] = "Success!"
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registrator_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        user = User.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email': user.email
        }
        request.session['quotes'] = []
        for quote in Quote.objects.all():
            quoteToAdd = {
                'id': quote.id,
                'likes':quote.liked_by_user.count(),
                "text": quote.text,
                "author":quote.author,
                "user_id": quote.added_by_id.id,
                "user_firstname":quote.added_by_id.first_name,
                "user_lastname":quote.added_by_id.last_name

            }
            request.session['quotes'].append(quoteToAdd)

    return render(request,'dashboard.html', context)
    
        

def editUser(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id=id)
        context = {
            'id' : user.id,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
        }
        return render(request,"editUser.html", context)
    else:
        return redirect('/')

def updateUser(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = id)
        user_id = user.id
        request.session['user_id'] = user_id
        errors = User.objects.updator_validator(request.POST)
        if len(errors):
            
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect('../edit')
        else:
            print('/'*50)
            user = User.objects.get(id = id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.password = password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user.save()
            request.session['user_id'] = user.id
            return redirect('/dashboard')

def post(request, id):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect('/dashboard')
    else:        
        Quote.objects.create(author=request.POST['quoteauthor'], text=request.POST['quoteText'], added_by_id=User.objects.get(id=id))#
        return redirect('/dashboard')

def showUser(request, id):
    user = User.objects.get(id=id)
    viewer = request.session['user_id']
    print("user",viewer)
    print("uploader", id)
    
    context = {
        'id': id,
        'user_id': request.session['user_id']
    }
    request.session['userquotes'] = []
    for quote in Quote.objects.filter(added_by_id = id):
        quoteToAdd = {
        'id':quote.id,
        'likes': quote.liked_by_user.count(),
        "text": quote.text,
        "author":quote.author,
        "user_id": quote.added_by_id.id,
        "user_firstname":quote.added_by_id.first_name,
        "user_lastname":quote.added_by_id.last_name

        }
        request.session['userquotes'].append(quoteToAdd)
        
    return render(request, 'userQuotes.html', context)
            
def logout(request):
    del request.session['user_id']
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['loginEmail']).id
        return redirect('/dashboard')

def deletepost(request, id):
    quote = Quote.objects.get(id=id)
    quote.delete()
    return redirect ('/dashboard') 

def addLike(request, id):
    quoteToUpdate = Quote.objects.get(id=id)
    current_user = User.objects.get(id = request.session['user_id'])
    quoteToUpdate.liked_by_user.add(current_user)
    quoteToUpdate.save()
    return redirect('/dashboard')