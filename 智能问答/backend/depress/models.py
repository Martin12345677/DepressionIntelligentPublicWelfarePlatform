from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    sex = models.BooleanField(blank=True, null=True)
    address = models.TextField(max_length=50)
    tel = models.CharField(max_length=15)


class Label(models.Model):
    lid = models.IntegerField()
    name = models.CharField(max_length=50)


class LabelRecord(models.Model):
    lid = models.IntegerField()
    email = models.EmailField()
    weight = models.IntegerField()
    times = models.IntegerField()


# 问答记录
class History(models.Model):
    email = models.EmailField()
    text = models.CharField(max_length=500)
    time = models.DateTimeField()
    send = models.BooleanField()


class Record(models.Model):
    tid = models.IntegerField()
    email = models.EmailField()
    time = models.DateTimeField()
    score = models.IntegerField()
    comment = models.CharField(max_length=2000)
    level = models.FloatField()
    same_num = models.IntegerField(blank=True)


class Answers(models.Model):
    tid = models.IntegerField()
    email = models.EmailField()
    pid = models.IntegerField()  # 题的编号
    answer = models.CharField(max_length=100)  # 以;分开
    same_num = models.IntegerField(blank=True)
    score = models.IntegerField(blank=True)


class Test(models.Model):
    tid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    intro = models.CharField(max_length=1000)
    num = models.IntegerField()  # 测试人数
    price = models.IntegerField(blank=True, null=True)
    rule = models.CharField(max_length=2000)
    lid = models.CharField(max_length=100, blank=True, null=True)


class Problem(models.Model):
    tid = models.IntegerField()
    pid = models.IntegerField(primary_key=True)
    nov = models.IntegerField()
    type = models.IntegerField(blank=True, default=0)  # 0表示单选题，1表示多选题
    description = models.TextField(max_length=200)
    choice = models.TextField(max_length=500)  # 选项，以;分割
    answer = models.TextField(max_length=100)  # 答案，以选项权重以;分割
    explanation = models.TextField(max_length=2000)  # 解说，以;分割
