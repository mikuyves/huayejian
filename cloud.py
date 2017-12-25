# coding: utf-8
import json
from datetime import datetime, timedelta

from leancloud import Engine
from leancloud import LeanEngineError
import leancloud
from utils import lc_dump
from send_gmail import Email
from models.goods import Prod, Sku


engine = Engine()


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
    prods = [lc_dump(obj) for obj in prod_objs]
    return json.dumps(prods)


@engine.define
def clear_empty_record():
    leancloud.use_master_key(True)
    empty_prods = check_empty_record('Prod', 'pid')
    empty_skus = check_empty_record('Sku', 'name')
    leancloud.use_master_key(False)
    return json.dumps([empty_prods, empty_skus])


def check_empty_record(clsname, attr):
    """检查并删除一天内意外生成的空数据。用于定时云函数。"""
    Cls = leancloud.Object.extend(clsname)
    objs = Cls.query\
        .greater_than_or_equal_to('createdAt', datetime.now() - timedelta(days=1))\
        .find()

    # 重要：一定要确保没有 pid 的对象！
    empty_objs = [obj for obj in objs if not obj.get(attr)]
    obj_dicts = [lc_dump(obj) for obj in empty_objs]
    obj_cnt = len(obj_dicts)
    obj_json = json.dumps(obj_dicts)

    if obj_cnt == 0:
        print('Checked {}. No empty record found.'.format(clsname))

    # 少于5行，直接删除。
    elif obj_cnt > 0 and obj_cnt < 5:
        leancloud.Object.destroy_all(empty_objs)

        title = 'LC-APP <huayejian>: DELETED {0} EMPTY RECORD(s) of {1}.'.format(obj_cnt, clsname)
        text = ''' There is {0} empty record(s) of {1}.
Records were deleted, as follow:
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

    return obj_json


# 生成主图缩略图
@engine.define
def make_thumbnail():
    leancloud.use_master_key(True)
    File = leancloud.Object.extend('_File')
    prods = Prod.query.limit(1)\
        .descending('CreatedAt')\
        .find()
    for num, p in enumerate(prods):
        url = p.get('mainPicUrl')
        results = File.query.equal_to('url', url).find()
        if results:
            f = results[0]
            image = leancloud.File.create_without_data(f.id)
            p.main_pic = image
            image.fetch()
            thumnail_url = image.get_thumbnail_url(100, 100)
            p.thumbnail_url = thumnail_url
            p.save()
            print(f'Update thumbnail. {num:d}')
        else:
            print(f'No main picture. {num:d}')
    leancloud.use_master_key(True)


# 生成SPU图像对象关系。
@engine.define
def make_image_relations():
    leancloud.use_master_key(True)
    File = leancloud.Object.extend('_File')
    prods = Prod.query.limit(1000) \
        .ascending('CreatedAt') \
        .find()
    for num, p in enumerate(prods):
        urls = p.get('picUrls')
        for url in urls:
            results = File.query.equal_to('url', url).find()
            if results:
                for image in results:
                    relation = p.relation('images')
                    relation.add(image)
                p.save()
                print(f'Relation saved. {num:d} {p}')

