from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection
import pymysql
import datetime


# Create your views here.
@login_required
def home(request):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie',
                         charset='utf8')
    cursor = db.cursor()
    cursor2 = db.cursor()
    orders = "SELECT * FROM orders, orders_status, store ,  menu WHERE orders.orderS_id = orders_status.orderS_id and orders.menu_id= menu.menu_id and orders.store_id=store.store_id ORDER BY FIELD(orders_status.is_finished, 1, 0) DESC, orders.deadline ASC"
    orders2 = "SELECT * FROM ordert, ordert_status, store WHERE ordert.orderT_id = ordert_status.orderT_id AND ordert.store_id = store.store_id order BY FIELD(ordert_status.is_finished, 1, 0) DESC, ordert.deadline ASC"
    numOrder = "SELECT COUNT(*) FROM orders"
    numOrder2 = "SELECT COUNT(*) FROM ordert"
    cursor.execute(numOrder)
    cursor2.execute(numOrder2)
    numOrder = cursor.fetchone()
    numOrder2 = cursor2.fetchone()
    num = 1
    time = "REPLACE INTO timediff_orders (orderS_id,timediff) SELECT orderS_id, time_to_sec(TIMEDIFF((SELECT deadline FROM orders where orderS_id = %s),curtime())) from orders where orderS_id = %s"
    time2 = "REPLACE INTO timediff_ordert (orderT_id,timediff) SELECT orderT_id, time_to_sec(TIMEDIFF((SELECT deadline FROM ordert where orderT_id = %s),curtime())) from ordert where orderT_id = %s"
    for num in range(numOrder[0]):
        cursor.execute(time, (int(num + 1), int(num + 1)))
        db.commit()

    for num in range(numOrder2[0]):
        cursor.execute(time2, (int(num + 1), int(num + 1)))
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
            'store_name': obj[13],
            'menu_name': obj[17],
            'location': obj[4],
            'isFinished': obj[10],
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
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='mango_smoothie',
                         charset='utf8')
    cursor = db.cursor()
    user_me = request.user.username
    cursor_info = db.cursor()
    point = "SELECT user_point FROM user where user_name = %s"
    cursor_info.execute(point, user_me)
    point = cursor_info.fetchone()[0]
    cursor_info.close()
    sql = '''select @rownum:=@rownum+1 as num, t.orderS_id, t.location, t.orderS_point, t.deadline, s.*, u.user_name,u.user_tel, m.menu_name, r.store_name
                from orders AS t JOIN orders_status AS s JOIN user AS u JOIN menu AS m JOIN store AS r, (SELECT @rownum:=0) r 
                WHERE s.orderS_id = t.orderS_id AND s.user_id =(select user_id from user where user_name=%s) AND t.user_id = u.user_id AND t.menu_id = m.menu_id AND t.store_id = r.store_id'''
    cursor.execute(sql, user_me)
    sql = cursor.fetchall()
    accepted_order_info = []
    for obj in sql:
        data_dic = {
            'index': int(obj[0]),
            'order_user': obj[9],
            'menu_name': obj[11],
            'store_name': obj[12],
            'order_phone': obj[10],
            'location': obj[2],
            'isFinished': obj[7],
            'time': str(obj[4]),
            'no': obj[1]
        }
        accepted_order_info.append(data_dic)
    print(accepted_order_info)
    '''
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
    '''
    sql2 = '''
           select @rownum:=@rownum+1 as num, ordert.*, ordert_acceptuser.*,ordert_status.*, user.*, store.store_name, menu.menu_name
from ordert join ordert_acceptuser on ordert.orderT_id=ordert_acceptuser.orderT_id
join ordert_status on ordert.orderT_id = ordert_status.orderT_id
join menu on menu.menu_id = ordert_acceptuser.menu_id
join store on store.store_id = ordert.store_id
join user on user.user_id = ordert.user_id ,(SELECT @rownum:=0) r 
WHERE ordert.orderT_id in(SELECT orderT_id FROM ordert_acceptuser WHERE user_id =(select user_id from user where user_name= %s))'''
    cursor.execute(sql2, user_me)
    sql2 = cursor.fetchall()
    register_order_info2 = []
    print(sql2)
    for obj in sql2:
        data_dic = {
            'index': int(obj[0]),
            'order_user': obj[15],
            'store_name': obj[20],
            'order_phone': obj[16],
            'location': obj[4],
            'isFinished': obj[13],
            'time': str(obj[5]),
            'no': obj[1],
            'menu_name': obj[21],
        }
        register_order_info2.append(data_dic)
    print(register_order_info2)

    sql3 = '''select @rownum:=@rownum+1 as num, orders.*, orders_status.*, menu.menu_name, store.store_name, user.user_name, user.user_tel
                from orders join orders_status on orders.orderS_id = orders_status.orderS_id 
                join menu on orders.menu_id =menu.menu_id
                join store on orders.store_id = store.store_id
                join user on user.user_id = orders.user_id,(SELECT @rownum:=0) r 
                WHERE orders.user_id= (select user_id from user where user_name = %s)'''
    cursor.execute(sql3, user_me)
    sql3 = cursor.fetchall()
    myorder_info = []
    for obj in sql3:
        data_dic = {
            'index': int(obj[0]),
            'accept_user': obj[11],
            'menu_name': obj[13],
            'store_name': obj[14],
            'order_phone': obj[16],
            'location': obj[5],
            'isFinished': obj[10],
            'time': str(obj[6]),
            'no': obj[1],
            'isDelivered' : obj[12]
        }
        myorder_info.append(data_dic)

    sql4 = '''
             select @rownum:=@rownum+1 as num, ordert.*, ordert_status.*,store.store_name
            from ordert join ordert_status on ordert.orderT_id = orderT_status.orderT_id 
            join store on ordert.store_id = store.store_id
            WHERE ordert.user_id= (select user_id from user where user_name =%s)'''
    cursor.execute(sql4, user_me)
    sql4 = cursor.fetchall()
    myorder_info4 = []
    for obj in sql4:
        data_dic = {
            'index': int(obj[0]),
            'store_name': obj[11],
            'location': obj[4],
            'isFinished': obj[10],
            'time': str(obj[5]),
            'maxorder':obj[6],
            'no': obj[1]
        }
        myorder_info4.append(data_dic)

    return render(request, 'home/mypage.html',
                  {"myorder_info": accepted_order_info, "myorder_info2": register_order_info2,
                   "myorder_info3": myorder_info, "myname": user_me, "mypoint": point, "myorder_info4": myorder_info4})
