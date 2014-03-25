import os
from uliweb import manage
from uliweb.orm import *
from uliweb.manage import make_simple_application

os.chdir('test_multidb')

manage.call('uliweb syncdb -v')
manage.call('uliweb syncdb -v --engine=b')

def test_1():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> print '__models__', orm.__models__
    __models__ {'blog': {'config': {}, 'model_path': 'blog.models.Blog', 'engines': ['default', 'b'], 'appname': 'blog'}, 'category': {'config': {}, 'model_path': 'blog.models.Category', 'engines': ['b'], 'appname': 'blog'}}
    >>> print engine_manager['default'].models
    {'blog': {'model': <class 'blog.models.Blog'>, 'created': None, 'model_path': 'blog.models.Blog', 'appname': 'blog'}}
    >>> print engine_manager['b'].models
    {'blog': {'model': <class 'uliweb.orm.ConnectModel'>, 'created': None, 'model_path': 'blog.models.Blog', 'appname': 'blog'}, 'category': {'model': <class 'blog.models.Category'>, 'created': None, 'model_path': 'blog.models.Category', 'appname': 'blog'}}
    >>> Blog1 = get_model('blog')
    >>> Blog2 = get_model('blog', 'b')
    >>> print 'blog2', Blog2, Blog2.table, Blog2.tablename, Blog2.get_engine_name(), Blog2.get_connection()
    blog2 <class 'uliweb.orm.ConnectModel'> blog blog b b
    >>> print 'blog1', Blog1, Blog1.table, Blog1.tablename, Blog1.get_engine_name(), Blog1.get_connection()
    blog1 <class 'blog.models.Blog'> blog blog default default
    >>> r = Blog2.all().remove()
    >>> r = Blog1.all().remove()
    >>> b2 = Blog2(title='1', content='1')
    >>> b2.save()
    True
    >>> b1 = Blog1(title='2', content='2')
    >>> b1.save()
    True
    >>> print 'blog2 all', list(Blog2.all())
    blog2 all [<Blog {'title':u'1','content':u'1','id':1}>]
    >>> print 'blog1 all', list(Blog1.all())
    blog1 all [<Blog {'title':u'2','content':u'2','id':1}>]
    >>> b3 = Blog2(title='3', content='3')
    >>> b3.save()
    True
    >>> print 'blog2 all', list(Blog2.all())
    blog2 all [<Blog {'title':u'1','content':u'1','id':1}>, <Blog {'title':u'3','content':u'3','id':2}>]
    """

def test_2():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> C = get_model('category')
    >>> r = C.all().remove()
    >>> a = C(name='python')
    >>> a.save()
    True
    >>> C.get(1)
    <Category {'name':u'python','id':1}>
    """

def test_3():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> B = get_model('blog')
    >>> r = B.all().remove()
    >>> a = B(title='1', content='1')
    >>> a.save()
    True
    >>> B1 = get_model('blog', 'b')
    >>> B2 = B.use('b')
    >>> id(B1) == id(B2)
    True
    >>> b = B.use('b')(title='2', content='2')
    >>> b.save()
    True
    >>> B.get(1)
    <Blog {'title':u'1','content':u'1','id':1}>
    """

def test_4():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> B = get_model('blog')
    >>> r = B.all().remove()
    >>> a = B(title='1', content='1')
    >>> a.save()
    True
    >>> r = B.use('b').remove()
    >>> b = B.use('b')(title='2', content='2')
    >>> b.save()
    True
    >>> print list(B.all().use('b'))
    [<Blog {'title':u'2','content':u'2','id':1}>]
    >>> print list(B.use('b').all())
    [<Blog {'title':u'2','content':u'2','id':1}>]
    """

def test_5():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> session = Session()
    >>> B = get_model('blog')
    >>> r = B.all().remove()
    >>> Commit()
    >>> B1 = B.use(session)
    >>> print session.in_transaction()
    False
    >>> r = B1.all().remove()
    >>> print session.in_transaction()
    True
    >>> a = B1(title='1', content='1')
    >>> a.save()
    True
    >>> session.commit()
    >>> B.get(1)
    <Blog {'title':u'1','content':u'1','id':1}>
    >>> from sqlalchemy.sql import select
    >>> print list(session.do_(select([B.table])))
    [(u'1', u'1', 1)]
    >>> r = B.get(1)
    """

def test_local_cache():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> session = Session()
    >>> session.get_local_cache('111')
    >>> session.get_local_cache('111', '222')
    '222'
    >>> B = get_model('blog')
    >>> r = B.all().remove()
    >>> Commit()
    >>> a = B(title='1', content='1')
    >>> a.save()
    True
    >>> Commit()
    >>> set_echo(True)
    >>> get_cached_object('blog', 1) # doctest:+ELLIPSIS, +NORMALIZE_WHITESPACE
    <BLANKLINE>
    ===>>>>> [default] (...)
    SELECT blog.title, blog.content, blog.id FROM blog WHERE blog.id = 1 AND 1 LIMIT 1 OFFSET 0;
    ===<<<<< time used ...s
    <BLANKLINE>
    <Blog {'title':u'1','content':u'1','id':1}>
    >>> s = get_session()
    >>> s.local_cache
    {'OC:default:blog:1': <Blog {'title':u'1','content':u'1','id':1}>}
    >>> get_cached_object('blog', 1)
    <Blog {'title':u'1','content':u'1','id':1}>
    >>> s.close()
    >>> s.local_cache
    {}
    >>> set_echo(False)
    """


def test_rollback():
    """
    >>> app = make_simple_application(project_dir='.')
    >>> import uliweb.orm as orm
    >>> session = Session()
    >>> B = get_model('blog')
    >>> r = B.all().remove()
    >>> Commit()
    >>> B1 = B.use(session)
    >>> print session.in_transaction()
    False
    >>> r = B1.all().remove()
    >>> print session.in_transaction()
    True
    >>> a = B1(title='1', content='1')
    >>> a.save()
    True
    >>> session.rollback()
    >>> B.count()
    0
    """
    
#del session
#del a
#del B1

#import objgraph
#objgraph.show_backrefs(objgraph.by_type('ConnectModel'),
#                       filename='session.png') 

#app = make_simple_application(project_dir='.')
#import uliweb.orm as orm
#db = get_connection()
#db.echo = True
#session = Session()
#B = get_model('blog')
#r = B.all().remove()
#Commit()
#B1 = B.use(session)
#print session.in_transaction()
#r = B1.all().remove()
#print session.in_transaction()
#
#a = B1(title='1', content='1')
#a.save()
#session.commit()
#B.get(1)
