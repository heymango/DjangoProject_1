from django.db import models
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='cafe', charset='utf8')
#cursor = db.cursor()
sql = '''
            CREATE TABLE menu (
                   menu_name VARCHAR(100),
                   store_name VARCHAR(100),
                   price INTEGER NOT NULL
            );
        '''
#cursor.execute(sql)
#db.commit()
cursor = db.cursor()
sql2 = '''
            CREATE TABLE store (
                   store_name VARCHAR(100) NOT NULL,
                   menu VARCHAR(100),
                   location VARCHAR(200) DEFAULT ''
            );
        '''
#cursor.execute(sql2)
#db.commit()

sql3 = '''
            CREATE TABLE orders (
                   name VARCHAR(10),
                   menu_name VARCHAR(100),
                   store_name VARCHAR(100),
                   tel VARCHAR(20),
                   location VARCHAR(200),
                   time DATETIME DEFAULT CURRENT_TIMESTAMP,
                   isFinished BOOLEAN DEFAULT '0'
            );
        '''
#cursor.execute(sql3)
#db.commit()
sql3 = '''
            CREATE TABLE orders_2 (
                   name VARCHAR(10),
                   store_name VARCHAR(100),
                   tel VARCHAR(20),
                   location VARCHAR(200),
                   time DATETIME DEFAULT CURRENT_TIMESTAMP,
                   isFinished BOOLEAN DEFAULT '0'
            );
        '''
