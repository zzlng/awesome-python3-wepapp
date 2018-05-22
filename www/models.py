#!/user/bin/env python3
# -*-coding: utf-8 -*-

"""Models of user, blog, comment."""

__author__ = 'Zachary Zhang'


import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField


next_id = lambda : '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class Awsmian(Model):
    __table__ = 'awsmian'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    pwd = StringField(ddl='varchar(50)')
    is_admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blog'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    awsmian_id = StringField(ddl='varchar(50)')
    awsmian_name = StringField(ddl='varchar(50)')
    awsmian_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comment'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    blog_name = StringField(ddl='varchar(50)')
    awsmian_id = StringField(ddl='varchar(50)')
    awsmian_name = StringField(ddl='varchar(50)')
    awsmian_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)