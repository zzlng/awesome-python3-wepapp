#!/user/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the Model of orm
python -m unittest orm_test
"""

__author__ = 'Zachary Zhang'


import unittest, asyncio

import orm

from models import Awsmian, Blog, Comment


class TestModel(unittest.TestCase):

    def test_p(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.package(loop))
        loop.close()

    async def package(self, loop):
        await orm.create_pool(loop=loop, user='zachary', password='password', database='awesome')
        a, b, c = await self.save_trial()
        await self.select_test(a, b, c)
        await self.update_test(a, b, c)
        await self.remove_trial()
        await orm.destroy_pool()

    async def save_trial(self):
        a = Awsmian(name='AwsmianTest', email='test0@example.com', pwd='1234567890')
        b = Blog(name='BlogTest', awsmian_id=a.id, awsmian_name=a.name, awsmian_image=a.image, summary='this is summary')
        c = Comment(blog_id=b.id, blog_name=b.name, awsmian_id=a.id, awsmian_name=a.name, awsmian_image=a.image)
        await a.save(), await b.save(), await c.save()
        a1 = Awsmian(name='Awsmian1', email='test1@example.com', pwd='1234567890', image='about:blank')
        a2 = Awsmian(name='Awsmian2', email='test2@example.com', pwd='1234567890', image='about:blank')
        b1 = Blog(name='Blog1', awsmian_id=a1.id, awsmian_name=a1.name, awsmian_image=a1.image, summary='summary1', content='blog1')
        b2 = Blog(name='Blog2', awsmian_id=a2.id, awsmian_name=a2.name, awsmian_image=a2.image, summary='summary2', content='blog2')
        await a1.save(), await a2.save()
        await b1.save(), await b2.save()
        await Comment(blog_id=b1.id, blog_name=b1.name, awsmian_id=a1.id, awsmian_name=a1.name, awsmian_image=a1.image, content='content1').save()
        await Comment(blog_id=b2.id, blog_name=b2.name, awsmian_id=a2.id, awsmian_name=a2.name, awsmian_image=a2.image, content='content2').save()
        return a, b ,c

    async def select_test(self, a, b, c):
        a1, b1, c1 = await Awsmian.find(a.id), await Blog.find(b.id), await Comment.find(c.id)
        a2 = (await Awsmian.findAll("`id`='%s'" % a.id))[0]
        b2 = (await Blog.findAll("`id`='%s'" % b.id))[0]
        c2 = (await Comment.findAll("`id`='%s'" % c.id))[0]
        a3 = (await Awsmian.findAll(orderBy='created_at'))[0]
        b3 = (await Blog.findAll(orderBy='created_at'))[0]
        c3 = (await Comment.findAll(orderBy='created_at'))[0]
        self.assertTrue(a.__dict__ == a1.__dict__ == a2.__dict__ == a3.__dict__)
        self.assertTrue(b.__dict__ == b1.__dict__ == b2.__dict__ == b3.__dict__)
        self.assertTrue(c.__dict__ == c1.__dict__ == c2.__dict__ == c3.__dict__)
        a_name = await Awsmian.findField('name', "`id`='%s'" % a.id)
        b_name = await Blog.findField('name', "`id`='%s'" % b.id)
        c_blog_name = await Comment.findField('blog_name', "`id`='%s'" % c.id)
        self.assertEqual(a.name, a_name)
        self.assertEqual(b.name, b_name)
        self.assertEqual(c.blog_name, c_blog_name)
        self.assertEqual(len(await Awsmian.findAll(**{'limit':(0)})), len(await Awsmian.findAll(**{'limit':0})))
        self.assertEqual(len(await Blog.findAll(**{'limit':(0)})), len(await Blog.findAll(**{'limit':0})))
        self.assertEqual(len(await Comment.findAll(**{'limit':(0)})), len(await Comment.findAll(**{'limit':0})))
        self.assertEqual(len(await Awsmian.findAll(**{'limit':(0, 2)})), 2)
        self.assertEqual(len(await Blog.findAll(**{'limit':(0, 2)})), 2)
        self.assertEqual(len(await Comment.findAll(**{'limit':(0, 2)})), 2)

    async def update_test(self, a, b, c):
        # a = (await Awsmian.findAll(**{'orderBy':'created_at'}))[0]
        # b = (await Blog.findAll(**{'orderBy':'created_at'}))[0]
        # c = (await Comment.findAll(**{'orderBy':'created_at'}))[0]
        a.image = '../image/awsmian_%s.png' % a.id[15:24]
        b.content = 'this is a blog'
        b.awsmian_image = a.image
        c.content = 'this is a content'
        c.awsmian_image = a.image
        await a.update(), await b.update(), await c.update()
        self.assertEqual(a.image, await Awsmian.findField('image', "`id`='%s'" % a.id))
        self.assertEqual(b.content, await Blog.findField('content', "`id`='%s'" % b.id))
        self.assertEqual(c.content, await Comment.findField('content', "`id`='%s'" % c.id))

    async def remove_trial(self):
        a = (await Awsmian.findAll(**{'orderBy':'created_at'}))[-1]
        b = (await Blog.findAll(**{'orderBy':'created_at'}))[-1]
        c = (await Comment.findAll(**{'orderBy':'created_at'}))[-1]
        await a.remove()
        await b.remove()
        await c.remove()