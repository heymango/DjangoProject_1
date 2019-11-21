# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models
import pymysql


class MyUser(AbstractUser):
    student_id = models.CharField(max_length=8, blank=True, null=True)


#db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yongyong19', db='accounts', charset='utf8')
#cursor = db.cursor()
sql = '''
            CREATE TABLE student_user (
                   name VARCHAR(20) NOT NULL,
                   student_id VARCHAR(10) NOT NULL,
                   phone VARCHAR(10) NOT NULL,
                   PRIMARY KEY(student_id)
            );
        '''

# 실행하기

#cursor.execute(sql)
#db.commit()
#db.close()
