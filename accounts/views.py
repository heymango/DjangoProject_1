from django.contrib.auth.hashers import get_hasher
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import redirect
from django.db import connection
import pymysql


def hashpassword(password):
    hasher = get_hasher('default')
    salt = hasher.salt()
    return hasher.encode(password, salt)
# Create your views here.
def signup(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            my_user = get_user_model()
            user_name = request.POST['username']
            password = request.POST['password1']
            student_id = request.POST['student_id']
            tel = request.POST['phone']
            if any(not char.isdigit() for char in student_id):
                messages.error(request, 'Check student_id')
                return render(request, 'accounts/signup.html')
            elif any(not char.isdigit() for char in tel):
                messages.error(request, 'Check phone number(only number)')
                return render(request, 'accounts/signup.html')
            cursor = db.cursor()
            sql = "SELECT user_name FROM user WHERE user_name=%s "
            cursor.execute(sql, user_name)
            result1 = cursor.fetchone()
            sql = "SELECT student_id FROM user WHERE student_id=%s "
            cursor.execute(sql, student_id)
            result2 = cursor.fetchone()
            if result1:
                messages.error(request, 'Already have same user name')
                return render(request, 'accounts/signup.html')
            if result2:
                messages.error(request, 'Already have same user ID')
                return render(request, 'accounts/signup.html')
            print(hashpassword(password))
            user = my_user.objects.create_user(
                username=user_name, password=password, student_id = student_id
            )
            cursor.close()
            cursor = db.cursor()
            sql = "INSERT INTO user(user_name, student_id, is_active, user_tel) VALUES(%s, %s, %s, %s)"
            cursor.execute(sql, (user_name, student_id, 0, tel))
            db.commit()
            db.close()
            cursor.close()
            # auth.login(request, user)
            return redirect('/accounts/login/')
        else:
            messages.error(request, 'Check password')
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')


def login(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    if request.POST.get('signup') == "signup":
        return redirect('/accounts/signup/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            cursor = db.cursor()
            sql = "UPDATE user SET is_active = '1' WHERE user_name=%s"
            cursor.execute(sql, username)
            db.commit()
            cursor.close()
            db.close()
            auth.login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, 'Login failed')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    user = getattr(request, 'user', None)
    name = user.username
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE user SET is_active = '0' WHERE user_name = %s"
    cursor.execute(sql, name)
    db.commit()
    cursor.close()
    db.close()
    auth.logout(request)
    return render(request, 'accounts/login.html')


def profile(request):
    if not request.user.is_authenticated:
        data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
    else:
        data = {'last_login': request.user.last_login, 'username': request.user.username,
                'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
    return render(request, 'accounts/profile.html', context={'data': data})


