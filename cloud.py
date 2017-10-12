# coding: utf-8
import json
from datetime import datetime, timedelta

from leancloud import Engine
from leancloud import LeanEngineError
import leancloud
from utils import obj_to_dict
from send_gmail import Email


engine = Engine()


Prod = leancloud.Object.extend('Prod')


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')


@engine.define
def test():
    prod_objs = Prod.query.find()
    prods = [obj_to_dict(obj) for obj in prod_objs]
    return json.dumps(prods)


@engine.define
def clear_empty_record():
    check_empty_record('Prod', 'pid')
    check_empty_record('Sku', 'name')


def check_empty_record(clsname, attr):
    """检查并删除一天内意外生成的空数据。用于定时云函数。"""
    Cls = leancloud.Object.extend(clsname)
    objs = Cls.query\
        .greater_than_or_equal_to('createdAt', datetime.now() - timedelta(days=1))\
        .find()

    # 重要：一定要确保没有 pid 的对象！
    empty_objs = [obj for obj in objs if not obj.get(attr)]
    obj_dicts = [obj_to_dict(obj) for obj in empty_objs]
    obj_cnt = len(obj_dicts)
    obj_json = json.dumps(obj_dicts)

    if obj_cnt == 0:
        print('Checked {}. No empty record found.'.format(clsname))

    # 少于5行，直接删除。
    elif obj_cnt > 0 and obj_cnt < 5:
        # leancloud.Object.destroy_all(empty_objs)

        title = 'LC-APP <huayejian>: DELETED {0} EMPTY RECORD(s) of {1}.'.format(obj_cnt, clsname)
        text = ''' There is {0} empty record(s) of {1}.
I have delete it/them.
Please the records deleted as follow:
{2}'''.format(obj_cnt, clsname, obj_json)

        email = Email(title=title, text=text)
        email.send()
        print(text)

    # 大于等于5行， 手动删除。
    else:
        title = 'IMPORTANT! LC-APP <huayejian>: FOUND {0} EMPTY RECORDS of {1}!'.format(obj_cnt, clsname)
        text = '''I have found {0} empty record in {1} table of the database.
Please check up the database immediately!
Delete the empty lines manually as soon as possible.
Records found as follow:
{2}'''.format(obj_cnt, clsname, obj_json)

        email = Email(title=title, text=text)
        email.send()
        print(text)
