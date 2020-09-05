from django.db import models

# Create your models here.
import mongoengine


class ArticleDetail(mongoengine.Document):
    _id = mongoengine.IntField(primary_key=True)
    period = mongoengine.IntField()
    title = mongoengine.StringField()
    author = mongoengine.StringField()
    desc = mongoengine.StringField()
    browse_num = mongoengine.IntField()
    comment_num = mongoengine.IntField()
    preview = mongoengine.StringField()
    link = mongoengine.StringField()
    figure = mongoengine.StringField()
    inside_title = mongoengine.StringField()
    fav_num = mongoengine.IntField()
    approve_num = mongoengine.IntField()
    content = mongoengine.StringField()
    date = mongoengine.StringField()


class ArticleIndex(mongoengine.Document):
    _id = mongoengine.IntField(primary_key=True)
    period = mongoengine.IntField()
    title = mongoengine.StringField()
    author = mongoengine.StringField()
    desc = mongoengine.StringField()
    browse_num = mongoengine.IntField()
    comment_num = mongoengine.IntField()
    preview = mongoengine.StringField()
    link = mongoengine.StringField()


class User(mongoengine.Document):
    _id = mongoengine.StringField(primary_key=True)
    username = mongoengine.StringField()
    password = mongoengine.StringField()
    avatarUrl = mongoengine.StringField(default='/static/images/base_avatar.png')
    fav_list = mongoengine.ListField()


class Comment(mongoengine.Document):
    _id = mongoengine.StringField(primary_key=True)
    author_id = mongoengine.StringField()
    author_name = mongoengine.StringField()
    content = mongoengine.StringField()
    text_content = mongoengine.StringField(default='')
    reply = mongoengine.StringField(default='0')
    created = mongoengine.StringField()
    is_main = mongoengine.BooleanField(default=False)
    approve_num = mongoengine.IntField(default=0)
    browse_num = mongoengine.IntField(default=0)
    approved_user_ids = mongoengine.ListField()
