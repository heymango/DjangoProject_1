from django.core.checks import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import *
from django.views.generic import View
from .forms import *
from datetime import datetime

store_name=''
menu_name=''
def Order(request):
    global store_name, menu_name
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    if request.POST.get('submit_order') is not None:
        if request.user.is_authenticated:
            username = request.user.username
            db2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='accounts',
                                  charset='utf8')
            cursor = db2.cursor()
            sql = "SELECT phone FROM student_user WHERE name = %s"
            cursor.execute(sql, username)
            userphone = cursor.fetchone()
            cursor.close()
            db2.close()
            cursor = db.cursor()
            sql = "INSERT INTO orders(name, menu_name, store_name, tel, location, order_time) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(username, menu_name, store_name, userphone, request.POST['place'], request.POST['time'],))
            db.commit()
            cursor.close()
            return redirect('/home/')

    if request.POST.get('menu') is not None:
        menuname = request.POST.get('menu')
        cursor = db.cursor()
        menu = "SELECT *FROM menu WHERE menu_name = %s"
        cursor.execute(menu, menuname)
        menu = cursor.fetchall()
        selected_menu_info = []
        for obj in menu:
            data_dic = {
                'menu': obj[0],
                'price': obj[2],
                'store': obj[1]
            }
            menu_name = obj[0]
            selected_menu_info.append(data_dic)
            cursor.close()
            return render(request, 'menu/order/order.html', {"menu": obj[0], "storename": obj[1], "price": obj[2]})
    if request.POST.get('store') is not None:
        print(1)
        store = request.POST.get('store')
        cursor = db.cursor()
        menu = "SELECT *FROM menu WHERE store_name = %s"
        cursor.execute(menu, store)
        menu = cursor.fetchall()
        menu_list = []
        for obj in menu:
            data_dic = {
                'menu': obj[0],
                'price': obj[2],
                'store': store
            }
            menu_list.append(data_dic)
        store_name = store
        cursor.close()
        return render(request, 'menu/order/order.html', {"menulist": menu_list, "storename": store})
    cursor = db.cursor()
    store = "select *from store"
    cursor.execute(store)
    store = cursor.fetchall()
    data_list = []
    for obj in store:
        data_dic = {
            'store': obj[0],
            'location': obj[2]
        }
        data_list.append(data_dic)
    cursor.close()
    # result = get_list_or_404(Menu, menu_name=menu_name)
    return render(request, 'menu/order/order.html', {"datalist": data_list})


def order_detail(request, pk):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT *FROM orders WHERE no=%s"
    cursor.execute(sql,pk)
    sql = cursor.fetchall()
    detail_list = []
    for obj in sql:
        data_dic = {
            'user_name': obj[0],
            'menu_name': obj[1],
            'store_name': obj[2],
            'user_phone': obj[3],
            'location': obj[4],
            'time': str(obj[5])
        }
        detail_list.append(data_dic)
    return render(request, 'menu/order/order_detail.html',{"detail" : detail_list})