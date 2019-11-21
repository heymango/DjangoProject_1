from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
import pymysql

# Create your views here.
@login_required
def home(request):
    return render(request, 'home/index.html')
