from django.core.checks import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import *
from django.views.generic import View
from .forms import *
from datetime import datetime

store_id = 0
menu_id =0
store_name =''
menu_name = ''
def Order1(request):
    global store_id, store_id, menu_name, menu_id
    print(request)
    if request.POST.get('GoHome') is not None:
        print("hi")
        return redirect('/home/')
    global store_name, menu_name
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    if request.POST.get('submit_order') is not None:
        print(0000000)
        if request.user.is_authenticated:
            username = request.user.username
            cursor = db.cursor()
            phone = "SELECT user_tel FROM user WHERE user_name = %s"
            cursor.execute(phone, username)
            phone = cursor.fetchone()
            insert = '''INSERT INTO orders (menu_id, user_id, store_id, location, deadline, orderS_point) 
                     SELECT a.menu_id, b.user_id, c.store_id, %s,%s,%s
                     from menu a, user b, store c 
                     WHERE(a.menu_name = %s and b.user_name = %s and c.store_name = %s)'''
            cursor.execute(insert,
                           (request.POST['place'],request.POST['time'],request.POST['point'],menu_name, username, store_name))
            db.commit()
            cursor.close()
            return redirect('/home/')

    if request.POST.get('menu') is not None:
        menu_name = request.POST.get('menu')
        cursor = db.cursor()
        menu = "SELECT *FROM menu WHERE menu_name = %s AND store_id = %s"
        cursor.execute(menu, (menu_name, store_id))
        menu = cursor.fetchone()
        menu_id = menu[0]
        price = menu[2]
        cursor.close()
        return render(request, 'menu/order/order_form.html', {"menu": menu_name, "storename": store_name, "price": price})
    if request.POST.get('store') is not None:
        store_name = request.POST.get('store') #save in global store_name
        cursor = db.cursor()
        get_id = "SELECT store_id FROM store WHERE store_name = %s"
        cursor.execute(get_id, store_name)
        get_id = cursor.fetchone()
        store_id = get_id[0] #save store_id
        menu = "SELECT *FROM menu WHERE store_id = %s"
        cursor.execute(menu, store_id)
        menu = cursor.fetchall()
        menu_list = []
        for obj in menu:
            data_dic = {
                'menu': obj[1],
                'price': obj[2],
                'store': store_name
            }
            menu_list.append(data_dic)
        cursor.close()
        return render(request, 'menu/order/order_form.html', {"menulist": menu_list, "storename": store_name})

    cursor = db.cursor()
    store = "select *from store"
    cursor.execute(store)
    store = cursor.fetchall()
    data_list = []
    for obj in store:
        data_dic = {
            'store': obj[1],
            'location': obj[2]
        }
        data_list.append(data_dic)
    cursor.close()
    # result = get_list_or_404(Menu, menu_name=menu_name)
    return render(request, 'menu/order/order_form.html', {"datalist": data_list})


def Order2(request):
    print(request)
    if request.POST.get('GoHome') is not None:
        print("hi")
        return redirect('/home/')
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
            sql = "INSERT INTO orders2(name, store_name, tel, location, order_time, point, numDrink) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,
                           (username, request.POST['store'], userphone, request.POST['place'], request.POST['time'],
                            request.POST['point'], request.POST['drinknum']))
            db.commit()
            cursor.close()
            return redirect('/home/')

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
    return render(request, 'menu/order/order_form2.html', {"datalist": data_list})


user_order = ''


def order_detail(request, pk):
    global user_order
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    if request.method == 'POST':
        user_me = request.user.username
        if user_order == user_me:
            messages = " Cannot accept my order"
            return render(request, 'home/index.html', {"message": messages})
        cursor_order = db.cursor()
        sql2 = "UPDATE orders  SET isAccepted = 1, accept_user = %s WHERE no = %s"
        cursor_order.execute(sql2, (user_me, pk))
        db.commit()
        point = "SELECT point FROM orders WHERE no = %s"
        cursor_order.execute(point, pk)
        point = cursor_order.fetchone()
        print(point[0])
        cursor_order.close()
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='accounts', charset='utf8')
        cursor_point = db.cursor()
        update_point = "UPDATE student_user SET point = point - %s WHERE name = %s"
        cursor_point.execute(update_point,(point[0],user_me))
        db.commit()
        cursor_point.close()
        messages = "Accept Order!"
        return render(request, 'home/index.html', {"message": messages})

    cursor = db.cursor()
    sql = "SELECT *FROM orders WHERE no=%s"
    cursor.execute(sql, pk)
    sql = cursor.fetchall()
    detail_list = []
    for obj in sql:
        data_dic = {
            'user_name': obj[0],
            'menu_name': obj[1],
            'store_name': obj[2],
            'user_phone': obj[3],
            'location': obj[4],
            'time': str(obj[6]),
        }
        user_order = obj[0]
        print(str(obj[6]))
        detail_list.append(data_dic)
    cursor.close()
    return render(request, 'menu/order/order_detail.html', {"detail": detail_list})


user_order2 = ''
store = ''
detail_list = []
menu_list = []
point = 0
menu_final = ''
totalprice =0
def order_detail2(request, pk):
    global user_order2
    global store
    global detail_list
    global menu_list
    global point
    global menu_final
    global totalprice
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT *FROM orders2 WHERE no=%s"
    cursor.execute(sql, pk)
    sql = cursor.fetchall()
    detail_list = []
    for obj in sql:
        data_dic = {
            'user_name': obj[0],
            'store_name': obj[1],
            'user_phone': obj[2],
            'location': obj[3],
            'time': str(obj[5]),
            'point': obj[9],
            'numremain': obj[10] - obj[11]
        }
        user_order2 = obj[0]
        point = obj[9]
        store = obj[1]
        detail_list.append(data_dic)

    menu = "SELECT *FROM menu WHERE store_name = %s"
    cursor.execute(menu, store)
    menu = cursor.fetchall()
    menu_list = []
    for obj in menu:
        data_dic = {
            'menu': obj[0],
            'price': obj[2]
        }
        menu_list.append(data_dic)
    cursor.close()
    if request.POST.get('menu_name') is not None:
        cursor_menu = db.cursor()
        menu_name = request.POST.get('menu')
        menu_final = request.POST.get('menu')
        menu_info = "SELECT *FROM menu WHERE store_name = %s AND menu_name = %s"
        cursor_menu.execute(menu_info,(store, menu_name))
        menu_info = cursor_menu.fetchall()
        print(menu_info)
        menu_list = []
        for obj in menu_info:
            data_dic = {
                'menu': obj[0],
                'price': obj[2],
                'totalprice' : obj[2]+point
            }
            totalprice = obj[2]+point
            menu_list.append(data_dic)
        cursor_menu.close()
        return render(request, 'menu/order/order_detail2.html', {"detail": detail_list, "menuinfo": menu_list })
    if request.POST.get('submit') is not None:
        user_me = request.user.username
        if user_order2 == user_me:
            messages = " Cannot accept my order"
            return render(request, 'home/index.html', {"message": messages})
        cursor_order = db.cursor()
        order = "UPDATE orders2 SET isFinished = IF(acceptNum == (SELECT drinkNum FROM orders2 WHERE no = %s)-1,1,0) WHERE no = %s"
        cursor_order.execute(order,(pk,pk))
        db.commit()
        order = "UPDATE orders2 SET acceptNum = acceptNum+1 WHERE no = %s"
        cursor_order.execute(order,pk)
        db.commit()
        print(totalprice)
        order = "INSERT INTO acceptuser VALUES(%s, %s, %s ,%s)"

        cursor_order.execute(order, (user_me, pk, menu_final, totalprice) )
        db.commit()
        messages = "Order success!"
        return render(request, 'home/index.html', {"message": messages})

    return render(request, 'menu/order/order_detail2.html', {"detail": detail_list, "menu": menu_list})
