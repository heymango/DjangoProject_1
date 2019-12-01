from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection
import pymysql

# Create your views here.
@login_required
def home(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    orders = "SELECT *FROM orders WHERE isFinished = '0' ORDER BY order_time ASC"
    orders2 = "SELECT *FROM orders2 WHERE isFinished = '0' ORDER BY order_time ASC"
    cursor.execute(orders)
    orders = cursor.fetchall()
    order_info = []
    for obj in orders:
        data_dic = {
            'index': obj[7],
            'store_name': obj[2],
            'menu_name': obj[1],
            'location': obj[4],
            'time': str(obj[6]),
            'color': (obj[7]%3)
        }
        order_info.append(data_dic)
    cursor.execute(orders2)
    orders2 = cursor.fetchall()
    print(orders2)
    order_info2 = []

    for obj in orders2:
        data_dic = {
            'index': obj[6],
            'store_name': obj[1],
            'numdrink' : obj[10],
            'location': obj[3],
            'time': str(obj[5]),
            'color': (obj[6] % 3)
        }
        order_info2.append(data_dic)
    cursor.close()

    return render(request, 'home/index.html',{"order_info" :order_info, "order_info2" :order_info2})

@login_required
def mypage(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    user_me = request.user.username
    sql = "select @rownum:=@rownum+1 as num, t.* from orders t, (SELECT @rownum:=0) r WHERE accept_user = %s"
    cursor.execute(sql, user_me)
    sql=cursor.fetchall()
    myorder_info = []
    for obj in sql:
        data_dic = {
            'index': int(obj[0]),
            'order_user': obj[1],
            'menu_name': obj[2],
            'store_name': obj[3],
            'order_phone': obj[4],
            'location': obj[5],
            'ifFinished': obj[6],
            'time': str(obj[7]),
            'no': obj[8]
        }
        myorder_info.append(data_dic)
    sql = "select @rownum:=@rownum+1 as num, orders2.*, acceptuser.* from orders2 inner join acceptuser on orders2.no=acceptuser.order_id , (SELECT @rownum:=0) r WHERE no in(SELECT order_id FROM acceptuser WHERE username = %s)"
    cursor.execute(sql, user_me)
    sql = cursor.fetchall()
    print(sql)
    myorder_info2 = []
    for obj in sql:
        data_dic = {
            'index': int(obj[0]),
            'order_user': obj[1],
            'store_name': obj[2],
            'order_phone': obj[3],
            'location': obj[4],
            'ifFinished': obj[5],
            'time': str(obj[6]),
            'no': obj[7],
            'menu_name' : obj[15],
            'price' : obj[16]
        }
    return render(request, 'home/mypage.html',{"myorder_info":myorder_info, "myname":user_me})


