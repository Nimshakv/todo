from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ListForm
from .models import ListNew
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/todolist/index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.error(request, ('Invalid login details given!'))
            # return HttpResponse("Invalid login details given")
            return HttpResponseRedirect(request.path_info)

    else:
        return render(request, 'todolist/login.html', {})


@login_required
def logout(request):
    print("logout")
    auth_logout(request)
    return HttpResponseRedirect('/todolist/login')


@login_required(login_url="/todolist/login/")
def index(request):
    user = request.user
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['owner'] = user.id
        form = ListForm(post_values or None)

        if form.is_valid():
            form.save()
            all_items = ListNew.objects.all()
            messages.success(request, ('Item has been added to list!'))
            # return render(request, 'todolist/index.html', {'all_items': all_items})
            return HttpResponseRedirect(request.path_info)
    else:
        all_items = ListNew.objects.filter(owner=user)
        return render(request, 'todolist/index.html', {'all_items': all_items})


@login_required(login_url="/todolist/login/")
def delete(request, list_id):
    item = ListNew.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ('Item has been deleted!'))
    return redirect('/todolist/index')


@login_required(login_url="/todolist/login/")
def edit(request, list_id):
    if request.method == 'POST':
        item = ListNew.objects.get(pk=list_id)

        user = request.user
        post_values = request.POST.copy()

        post_values['owner'] = user.id

        form = ListForm(post_values or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, ('Item has been edited!'))
        return HttpResponseRedirect('/todolist/index')

    else:
        item = ListNew.objects.get(pk=list_id)
        return render(request, 'todolist/edit.html', {"item": item})


@login_required(login_url="/todolist/login/")
def cross_off(request, list_id):
    item = ListNew.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('/todolist/index')


@login_required(login_url="/todolist/login/")
def uncross(request, list_id):
    item = ListNew.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('/todolist/index')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            _user_name = form.cleaned_data.get('username')
            _raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=_user_name, password=_raw_password)
            auth_login(request, user)
        return redirect('/todolist/login')
    else:
        form = UserCreationForm()
    return render(request, 'todolist/signup.html', {'form': form})



