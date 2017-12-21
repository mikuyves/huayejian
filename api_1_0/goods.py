from . import api
from flask import jsonify, request

import leancloud

from utils import obj_to_dict


Prod = leancloud.Object.extend('Prod')
Cate = leancloud.Object.extend('Cate')


@api.route('/goods/')
def get_goods():
    # 分页参数。
    start = int(request.args.get('from', 0))
    count = int(request.args.get('limit', 10))
    print(request.args)

    # 分页获取对象。
    tasks = Prod.query.skip(start).limit(count).find()
    # 将 Leancloud Object 转为字典格式。
    goods = [obj_to_dict(task) for task in tasks]

    # 按前端格式打包数据，成功响应的 code 为 0。
    # 对照: 小程序项目 'src/utils/Http.js' 的 `isSuccess` 方法。
    data = {
        'data': goods,
        'code': 0
    }
    return jsonify(data)


@api.route('/goods/inner_category')
def get_cates():
    cates = Cate.query.find()
    categories = [obj_to_dict(cate) for cate in cates]
    data = {
        'data': categories,
        'code': 0
    }
    return jsonify(data)
