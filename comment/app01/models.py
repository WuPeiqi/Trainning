from django.db import models

# Create your models here.

class SendMsg(models.Model):

    nid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=32, db_index=True)
    times = models.IntegerField(default=0)
    ctime = models.DateTimeField()


class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField()

class NewsType(models.Model):
    nid = models.AutoField(primary_key=True)

    caption = models.CharField(max_length=32)


class News(models.Model):
    nid = models.AutoField(primary_key=True)
    user_info = models.ForeignKey('UserInfo')
    news_type = models.ForeignKey('NewsType')
    title = models.CharField(max_length=32, db_index=True)
    url = models.CharField(max_length=128)
    content = models.CharField(max_length=50)
    favor_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    ctime = models.DateTimeField()


class Favor(models.Model):


    nid = models.AutoField(primary_key=True)

    user_info = models.ForeignKey('UserInfo')
    news = models.ForeignKey('News')

    ctime = models.DateTimeField()

    class Meta:
        unique_together = (("user_info", "news"),)


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)

    user_info = models.ForeignKey('UserInfo')
    news = models.ForeignKey('News')

    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    ctime = models.DateTimeField()


    device = models.CharField(max_length=16)
    content = models.CharField(max_length=150)

    reply_id = models.ForeignKey('Comment', related_name='b', null=True, blank=True)
