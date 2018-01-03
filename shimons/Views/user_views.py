import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from shimons import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.base_user import check_password
from shimons.models import UserProfile


def signup(request):
    if request.method == "POST":
        if request.method == "POST":
            form = forms.UserForm(request.POST)
            if form.is_valid():
                print("signup:" + form.cleaned_data['email'] + form.cleaned_data['password'] + "okay")
                post = form.save()
                post.date = datetime.datetime.now()
                post.save()
                user = get_user_model().objects.get(email=form.cleaned_data['email'])
                new_user = authenticate(email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'],
                                        )
                print('new_user:', user)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/index')
                else:
                    return HttpResponse('ridi')
            else:
                print(form.errors.items())
                return render(request, 'sqlab/signup.html', {'form': form, 'error': form.errors})
        pass
    else:
        form = forms.UserForm()
        return render(request, 'sqlab/signup.html', {'form': form, 'error': ''})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/index')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(email, password)
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")
