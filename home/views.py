from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection
import pymysql
import datetime


# Create your views here.
@login_required
def home(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    cursor = db.cursor()
    cursor2 = db.cursor()
    orders = "SELECT * FROM orders, orders_status, store ,  menu WHERE orders.orderS_id = orders_status.orderS_id and orders.menu_id= menu.menu_id and orders.store_id=store.store_id ORDER BY FIELD(orders_status.is_finished, 1, 0) DESC, orders.deadline ASC"
    orders2 = "SELECT * FROM ordert, ordert_status, store WHERE ordert.orderT_id = ordert_status.orderT_id AND ordert.store_id = store.store_id order BY FIELD(ordert_status.is_finished, 1, 0) DESC, ordert.deadline ASC"
    numOrder = "SELECT COUNT(*) FROM orders"
    numOrder2 = "SELECT COUNT(*) FROM ordert"
    cursor.execute(numOrder)
    cursor2.execute(numOrder2)
    numOrder  = cursor.fetchone()
    numOrder2 = cursor2.fetchone()
    num = 1
    time= "REPLACE INTO timediff_orders (orderS_id,timediff) SELECT orderS_id, time_to_sec(TIMEDIFF((SELECT deadline FROM orders where orderS_id = %s),curtime())) from orders where orderS_id = %s"
    time2= "REPLACE INTO timediff_ordert (orderT_id,timediff) SELECT orderT_id, time_to_sec(TIMEDIFF((SELECT deadline FROM ordert where orderT_id = %s),curtime())) from ordert where orderT_id = %s"
    for num in range(numOrder[0]):
        cursor.execute(time, (int(num+1),int(num+1)))
        db.commit()

    for num in range(numOrder2[0]):
        cursor.execute(time2, (int(num+1),int(num+1)))
        db.commit()

    timeUpdate = "UPDATE orders_status SET is_finished=1 WHERE orderS_id IN(SELECT orderS_id FROM timediff_orders WHERE timediff<=0)"
    cursor.execute(timeUpdate)
    db.commit()
    timeUpdate2 = "UPDATE ordert_status SET is_finished=1 WHERE orderT_id IN(SELECT orderT_id FROM timediff_ordert WHERE timediff<=0)"
    cursor2.execute(timeUpdate2)
    db.commit()
    cursor2.close()

    cursor.execute(orders)
    orders = cursor.fetchall()
    print("info", orders)
    order_info = []
    for obj in orders:
        data_dic = {
            'index': obj[0],
            'store_name': obj[12],
            'menu_name': obj[16],
            'location': obj[4],
            'isFinished' : obj[9],
            'time': str(obj[5]),
            'color': (obj[0] % 3)
        }
        order_info.append(data_dic)
    cursor.execute(orders2)
    orders2 = cursor.fetchall()
    order_info2 = []

    for obj in orders2:
        data_dic = {
            'index': obj[0],
            'store_name': obj[11],
            'numdrink': obj[5],
            'isFinished': obj[9],
            'location': obj[3],
            'time': str(obj[4]),
            'color': (obj[0] % 3)
        }
        order_info2.append(data_dic)
    cursor.close()

    return render(request, 'home/index.html', {"order_info": order_info, "order_info2": order_info2})


@login_required
def mypage(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie', charset='utf8')
    cursor = db.cursor()
    user_me = request.user.username
    cursor_info = db.cursor()
    point = "SELECT point FROM user where user_name = %s"
    cursor_info.execute(point, user_me)
    point = cursor_info.fetchone()[0]
    cursor_info.close()
    sql = "select @rownum:=@rownum+1 as num, t.* from orders t, (SELECT @rownum:=0) r WHERE accept_user = %s"
    cursor.execute(sql, user_me)
    sql = cursor.fetchall()
    accepted_order_info = []
    for obj in sql:
        if obj[6] == 0:
            data_dic = {
                'index': int(obj[0]),
                'order_user': obj[1],
                'menu_name': obj[2],
                'store_name': obj[3],
                'order_phone': obj[4],
                'location': obj[5],
                'isFinished': 'No',
                'time': str(obj[7]),
                'no': obj[8]
            }
            accepted_order_info.append(data_dic)
        if obj[6] == 1:
            data_dic = {
                'index': int(obj[0]),
                'order_user': obj[1],
                'menu_name': obj[2],
                'store_name': obj[3],
                'order_phone': obj[4],
                'location': obj[5],
                'isFinished': 'Yes',
                'time': str(obj[7]),
                'no': obj[8]
            }
            accepted_order_info.append(data_dic)

    sql2 = "select @rownum:=@rownum+1 as num, orders2.*, acceptuser.* from orders2 inner join acceptuser on orders2.no=acceptuser.order_id , (SELECT @rownum:=0) r WHERE no in(SELECT order_id FROM acceptuser WHERE username = %s)"
    cursor.execute(sql2, user_me)
    sql2 = cursor.fetchall()
    register_order_info2 = []
    for obj in sql2:
        if (obj[5] == 0):
            data_dic = {
                'index': int(obj[0]),
                'order_user': obj[1],
                'store_name': obj[2],
                'order_phone': obj[3],
                'location': obj[4],
                'isFinished': "No",
                'time': str(obj[6]),
                'no': obj[7],
                'menu_name': obj[15],
                'price': obj[16]
            }
            register_order_info2.append(data_dic)

        if (obj[5] == 1):
            data_dic = {
                'index': int(obj[0]),
                'order_user': obj[1],
                'store_name': obj[2],
                'order_phone': obj[3],
                'location': obj[4],
                'isFinished': "Yes",
                'time': str(obj[6]),
                'no': obj[7],
                'menu_name': obj[15],
                'price': obj[16]
            }
            register_order_info2.append(data_dic)

    sql3 = "select @rownum:=@rownum+1 as num, t.* from orders t, (SELECT @rownum:=0) r WHERE name = %s"
    cursor.execute(sql3, user_me)
    sql3 = cursor.fetchall()
    myorder_info = []
    for obj in sql3:
        if obj[6] == 0:
            data_dic = {
                'index': int(obj[0]),
                'accept_user': obj[9],
                'menu_name': obj[2],
                'store_name': obj[3],
                'order_phone': obj[4],
                'location': obj[5],
                'isFinished': 'No',
                'time': str(obj[7]),
                'no': obj[8]
            }
            myorder_info.append(data_dic)
        if obj[6] == 1:
            data_dic = {
                'index': int(obj[0]),
                'accept_user': obj[9],
                'menu_name': obj[2],
                'store_name': obj[3],
                'order_phone': obj[4],
                'location': obj[5],
                'isFinished': 'Yes',
                'time': str(obj[7]),
                'no': obj[8]
            }
            myorder_info.append(data_dic)

    return render(request, 'home/mypage.html',
                  {"myorder_info": accepted_order_info, "myorder_info2": register_order_info2, "myorder_info3": myorder_info, "myname": user_me, "mypoint":point})
