from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
import pymysql

# Create your views here.
@login_required
def home(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    orders = "SELECT *FROM orders WHERE isFinished = 0"
    cursor.execute(orders)
    orders = cursor.fetchall()
    order_info = []
    for obj in orders:
        data_dic = {
            'index': obj[7],
            'store_name': obj[2],
            'menu_name': obj[1],
            'location': obj[4],
            'time': obj[6]
        }
        order_info.append(data_dic)
    return render(request, 'home/index.html',{"order_info" :order_info})
