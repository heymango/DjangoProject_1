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
    orders = "SELECT * FROM orders, orders_status WHERE orders.orderS_id = orders_status.orderS_id ORDER BY FIELD(orders_status.is_finished, 1, 0) DESC, orders.deadline ASC"
    orders2 = "SELECT * FROM ordert, ordert_status WHERE ordert.orderT_id = ordert_status.orderT_id ORDER BY FIELD(ordert_status.is_finished, 1, 0) DESC, ordert.deadline ASC"
    numOrder = "SELECT COUNT(*) FROM orders"
    numOrder2 = "SELECT COUNT(*) FROM ordert"
    cursor.execute(numOrder)
    cursor2.execute(numOrder2)
    numOrder  = cursor.fetchone()
    numOrder2 = cursor2.fetchone()
    num = 1
    time= "REPLACE INTO time (no,timediff) SELECT no, time_to_sec(TIMEDIFF((SELECT order_time FROM orders where no = %s),curtime())) from orders where no = %s"
    time2= "REPLACE INTO time (no,timediff) SELECT no, time_to_sec(TIMEDIFF((SELECT order_time FROM orders2 where no = %s),curtime())) from orders2 where no = %s"
    for num in range(numOrder[0]):
        cursor.execute(time, (int(num+1),int(num+1)))
        db.commit()

    for num in range(numOrder2[0]):
        cursor.execute(time2, (int(num+1),int(num+1)))
        db.commit()

    timeUpdate = "UPDATE orders SET isFinished=1 WHERE no IN(SELECT no FROM time WHERE timediff<=0)"
    cursor.execute(timeUpdate)
    db.commit()
    timeUpdate2 = "UPDATE orders2 SET isFinished=1 WHERE no IN(SELECT no FROM time WHERE timediff<=0)"
    cursor2.execute(timeUpdate2)
    db.commit()
    cursor2.close()

    cursor.execute(orders)
    orders = cursor.fetchall()
    print("info", orders)
    order_info = []
    for obj in orders:
        data_dic = {
            'index': obj[7],
            'store_name': obj[2],
            'menu_name': obj[1],
            'location': obj[4],
            'isFinished' : obj[5],
            'time': str(obj[6]),
            'color': (obj[7] % 3)
        }
        order_info.append(data_dic)
    cursor.execute(orders2)
    orders2 = cursor.fetchall()
    order_info2 = []

    for obj in orders2:
        data_dic = {
            'index': obj[6],
            'store_name': obj[1],
            'numdrink': obj[10],
            'isFinished': obj[4],
            'location': obj[3],
            'time': str(obj[5]),
            'color': (obj[6] % 3)
        }
        order_info2.append(data_dic)
    cursor.close()

    return render(request, 'home/index.html', {"order_info": order_info, "order_info2": order_info2})


@login_required
def mypage(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
    cursor = db.cursor()
    user_me = request.user.username
    db_user = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='accounts', charset='utf8')
    cursor_info = db_user.cursor()
    point = "SELECT point FROM student_user where name = %s"
    cursor_info.execute(point, user_me)
    point = cursor_info.fetchone()[0]
    cursor_info.close()
    db_user.close()
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
