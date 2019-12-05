from django.core.checks import messages
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import *
from django.views.generic import View
from .forms import *
from datetime import datetime

store_id = 0
menu_id = 0
store_name = ''
menu_name = ''


def Order1(request):
    global store_id, store_id, menu_name, menu_id
    if request.POST.get('GoHome') is not None:  # go home button
        return redirect('/home/')
    global store_name, menu_name
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie',
                         charset='utf8')
    # when user submit order
    if request.POST.get('submit_order') is not None:
        print(0000000)
        if request.user.is_authenticated:
            username = request.user.username
            cursor = db.cursor()
            # 쿼리문 바꿀수 있음
            insert = '''INSERT INTO orders (menu_id, user_id, store_id, location, deadline, orderS_point) 
                     SELECT a.menu_id, b.user_id, c.store_id, %s,%s,%s
                     from menu a, user b, store c 
                     WHERE(a.menu_name = %s and b.user_name = %s and c.store_name = %s)'''
            cursor.execute(insert,
                           (request.POST['place'], request.POST['time'], request.POST['point'], menu_name, username,
                            store_name))
            db.commit()
            insert_status = '''INSERT INTO orders_status(is_accepted) values(0)'''
            cursor.execute(insert_status)
            db.commit()
            cursor.close()
            return redirect('/home/')
    # when user select menu(load selected menu info)
    if request.POST.get('menu') is not None:
        menu_name = request.POST.get('menu')
        cursor = db.cursor()
        menu = "SELECT *FROM menu WHERE menu_name = %s AND store_id = %s"
        cursor.execute(menu, (menu_name, store_id))
        menu = cursor.fetchone()
        menu_id = menu[0]
        price = menu[2]
        cursor.close()
        return render(request, 'menu/order/order_form.html',
                      {"menu": menu_name, "storename": store_name, "price": price})
    # when user select store(load menu list)
    if request.POST.get('store') is not None:
        store_name = request.POST.get('store')  # save in global store_name
        cursor = db.cursor()
        get_id = "SELECT store_id FROM store WHERE store_name = %s"
        cursor.execute(get_id, store_name)
        get_id = cursor.fetchone()
        store_id = get_id[0]  # save store_id
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
    # first, load store info in db
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
    return render(request, 'menu/order/order_form.html', {"datalist": data_list})


def Order2(request):
    if request.POST.get('GoHome') is not None:
        return redirect('/home/')
    global store_name, menu_name
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie',
                         charset='utf8')
    if request.POST.get('submit_order') is not None:
        if request.user.is_authenticated:
            username = request.user.username
            time = request.POST['time']
            cursor = db.cursor()
            insert = '''INSERT INTO ordert(user_id, store_id, location, deadline,max_order,orderT_point) 
                                 SELECT user.user_id, store.store_id, %s,%s,%s,%s
                                 FROM user join store  
                                 WHERE(user.user_name = %s and store.store_name = %s)'''
            cursor.execute(insert,
                           (request.POST['place'], time, request.POST.get('drinknum'), request.POST['point'], username,
                            request.POST['store']))
            db.commit()
            insert_status = '''INSERT INTO ordert_status(orderT_num,is_finished) values(0,0)'''
            cursor.execute(insert_status)
            db.commit()
            cursor.close()
            return redirect('/home/')

    cursor = db.cursor()
    store = "SELECT *FROM store"
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
    return render(request, 'menu/order/order_form2.html', {"datalist": data_list})


user_order = ''
def order_detail(request, pk):
    global user_order
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie',
                         charset='utf8')
    if request.POST.get('GoHome') is not None:
        return redirect('/home/')
    if request.method == 'POST':
        user_me = request.user.username
        if user_order == user_me:
            messages = " Cannot accept my order"
            return render(request, 'home/index.html', {"message": messages})
        cursor = db.cursor()
        acceptorder = '''
                        UPDATE orders_status 
                        SET is_accepted=1, user_id=(SELECT user_id FROM user WHERE user_name = %s)
                        WHERE orderS_id = %s
                  '''
        cursor.execute(acceptorder, (user_me, pk))
        db.commit()
        point = "SELECT orderS_point FROM orders WHERE orderS_id = %s"
        cursor.execute(point, pk)
        point = cursor.fetchone()
        print(point[0])
        cursor.close()
        cursor_point = db.cursor()
        update_point = "UPDATE user SET user_point = user_point + %s WHERE user_name = %s"
        cursor_point.execute(update_point, (point[0], user_me))
        db.commit()
        update_point = "UPDATE user SET user_point = user_point - %s WHERE user_name = %s"
        cursor_point.execute(update_point, (point[0], user_order))
        db.commit()
        cursor_point.close()
        messages = "Accept Order!"
        return render(request, 'home/index.html', {"message": messages})

    cursor = db.cursor()
    orderinfo = '''
                    SELECT O.*, U.user_name, U.user_tel, M.menu_name , S.store_name,T.is_finished
                    FROM orders O
                    INNER JOIN user U
                    ON O.orderS_id= %s AND O.user_id = U.user_id  
                    INNER JOIN store S  
                    ON O.store_id = S.store_id 
                    INNER JOIN menu M
                    ON O.menu_id  = M.menu_id
                    INNER JOIN orders_status T
                    ON O.orderS_id  = T.orderS_id
                '''
    cursor.execute(orderinfo, pk)
    orderinfo = cursor.fetchall()
    detail_list = []
    for obj in orderinfo:
        data_dic = {
            'user_name': obj[7],
            'menu_name': obj[9],
            'store_name': obj[10],
            'user_phone': obj[8],
            'location': obj[4],
            'time': str(obj[5]),
            'finish' : obj[11]
        }
        user_order = obj[7]
        detail_list.append(data_dic)
    cursor.close()
    return render(request, 'menu/order/order_detail.html', {"detail": detail_list})


user_order2 = ''
store_id2 = 0
menu_id2 = 0
detail_list = []
menu_list = []
point = 0
menu_final = ''
totalprice = 0
maxnum = 0
def order_detail2(request, pk):
    print(request.POST)
    global user_order2
    global store_id2, menu_id2
    global detail_list, menu_list ,point, menu_final, totalprice , maxnum
    if request.POST.get('GoHome') is not None:
        return redirect('/home/')
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    cursor = db.cursor()
    orderinfo = '''
                    SELECT O.*, U.user_name, U.user_tel , S.store_name, T.orderT_num ,T.is_finished
                    FROM ordert O
                    INNER JOIN user U
                    ON O.orderT_id= %s AND O.user_id = U.user_id  
                    INNER JOIN store S  
                    ON O.store_id = S.store_id 
                    INNER JOIN ordert_status T
                    ON O.orderT_id = T.orderT_id
                '''
    cursor.execute(orderinfo, pk)
    sql = cursor.fetchall()
    detail_list = []
    for obj in sql:
        data_dic = {
            'user_name': obj[7],
            'store_name': obj[9],
            'user_phone': obj[8],
            'location': obj[3],
            'time': str(obj[4]),
            'point': obj[6],
            'numremain': obj[5] - obj[10],
            'finish': obj[11]
        }
        user_order2 = obj[7]
        point = obj[6]
        store_id2 = obj[2]
        detail_list.append(data_dic)

    menu = "SELECT *FROM menu WHERE store_id = %s"
    cursor.execute(menu, store_id2)
    menu = cursor.fetchall()
    menu_list = []
    for obj in menu:
        data_dic = {
            'menu': obj[1],
            'price': obj[2]
        }
        menu_list.append(data_dic)
    cursor.close()
    if request.POST.get('menu_name') is not None:
        cursor= db.cursor()
        menu_name = request.POST.get('menu')
        menu_info = "SELECT *FROM menu WHERE store_id = %s AND menu_name = %s"
        cursor.execute(menu_info, (store_id2, menu_name))
        menu_info = cursor.fetchall()
        menu_list = []
        for obj in menu_info:
            data_dic = {
                'menu': obj[1],
                'price': obj[2],
                'totalprice': obj[2] + point
            }
            menu_id2 = obj[0]
            totalprice = obj[2] + point
            menu_list.append(data_dic)
        print(menu_list)
        cursor.close()
        return render(request, 'menu/order/order_detail2.html', {"detail": detail_list, "menuinfo": menu_list})
    if request.POST.get('submit') is not None:
        user_me = request.user.username
        if user_order2 == user_me:
            messages = " Cannot accept my order"
            return render(request, 'home/index.html', {"message": messages})
        cursor_order = db.cursor()
        max_order = "select max_order from ordert where orderT_id = %s"
        cursor_order.execute(max_order, pk)
        max_order = (cursor_order.fetchone())[0]
        order = "UPDATE ordert_status SET is_finished = IF(orderT_num+1>=%s,1,0) WHERE orderT_id = %s"
        cursor_order.execute(order, (max_order, pk))
        db.commit()
        order = "UPDATE ordert_status SET orderT_num = orderT_num+1 WHERE orderT_id = %s"
        cursor_order.execute(order, pk)
        db.commit()
        update_point = "UPDATE user SET user_point =user_point + IF((SELECT is_finished FROM ordert_status WHERE orderT_id = %s) = 1, %s, 0) WHERE user_name = %s"
        cursor_order.execute(update_point, (pk,point*max_order, user_order2))
        db.commit()
        update_point = "UPDATE user SET user_point = user_point - %s WHERE user_name = %s"
        cursor_order.execute(update_point, (point, user_me))
        db.commit()
        order = "INSERT INTO ordert_acceptuser(user_id, orderT_id, menu_id) SELECT user_id, %s,%s FROM user WHERE user_name = %s"
        cursor_order.execute(order, (pk,menu_id2,user_me))
        db.commit()
        messages = "Order success!"
        return render(request, 'home/index.html', {"message": messages})

    return render(request, 'menu/order/order_detail2.html', {"detail": detail_list, "menu": menu_list})
