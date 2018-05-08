#!/user/bin/env python3
# -*-coding: utf-8 -*-

"""Models of user, blog, comment."""

__author__ = 'Zachary Zhang'


import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
	__table__ = 'USERS'

	id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
	email = StringField(ddl='varchar(50)')
	pwd = StringField(ddl='varchar(50)')
	admin = BooleanField()
	name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'BLOGS'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'COMMENTS'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)