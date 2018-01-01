from functools import wraps

from flask import jsonify, request, make_response

import leancloud
from leancloud.errors import LeanCloudError


def lc_dump(obj):
    '''把Leancloud 获取的对象转成字典。
    注意：如果使用了 include 获取对象的 pointer 字典，需要 pointer 单独进行一次转字典的处理。'''
    # 获取所有 pointer 的字段名。
    pointer_keys = []
    for k, v in obj.dump().items():
        if isinstance(v, dict) and v.get('__type') == 'Pointer':
            pointer_keys.append(k)
    # 重点：处理 pointer。把所有的 pointer dump 一次。
    pointers = {key: obj.get(key).dump() for key in pointer_keys}
    # 处理 object。
    obj = obj.dump()
    # 前段模板经常需要对象的 id 字段进行选择。
    obj['id']  = obj.get('objectId')
    # 替换已经处理好的 pointer。
    for k, v in pointers.items():
        obj[k] = v
    return obj


def lc_dumps(objs):
    return [lc_dump(obj) for obj in objs]


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        # 处理用户登录状态
        # 如果用户不是用户，会抛出 leancloud.erros.LeanCloudError:
        # [1] Please provide username/password,mobilePhoneNumber/password or mobilePhoneNumber/smsCode.
        # 而前端则产生 500 (INTERNAL SERVER ERROR)。
        # 使用 leancloud.User.become() 之后，在本次请求中就可以用 leancloud.User.get_current()
        # 获取当前的登录用户。因此不用把 user 传到后面的请求中。
        session_token = request.headers.get('sessionToken')
        try:
            user = leancloud.User.become(session_token=session_token)
            return func(*args, **kwargs)
        except LeanCloudError as e:
            print(e.code)
            print(e.error)
            data = {
                'code': e.code,
                'error': e.error
            }
            return make_response(jsonify({'data': data}), 505)
    return wrap
