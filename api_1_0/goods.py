import json

from . import api
from flask import jsonify, request

import leancloud

from utils import obj_to_dict


Prod = leancloud.Object.extend('Prod')
Sku = leancloud.Object.extend('Sku')
Cate = leancloud.Object.extend('Cate')


@api.route('/goods/')
def get_goods():
    # 分页参数。
    start = int(request.args.get('from', 0))
    count = int(request.args.get('limit', 20))
    category_id = request.args.get('category_id')
    status = request.args.get('goods_status')
    # 搜索关键字是 JSON 字符串，需要转换格式。
    keywords = json.loads(request.args.get('search_keywords'))
    print(request.args)

    # 分页获取对象。
    prod_query = Prod.query\
        .descending('createdAt')\
        .skip(start)\
        .limit(count)\
        .include('supplier')

    # 搜索
    if keywords:
        for kw in keywords:
            prod_query.contains('name', kw.upper())
    # 状态
    if status and status != 'search':
        prod_query.equal_to(status, True)
    # 分类
    if category_id:
        cate = Prod.create_without_data(category_id)
        prod_query.equal_to('cate', cate)

    prods = prod_query.find()

    # 将 Leancloud Object 转为字典格式。
    goods = [obj_to_dict(prod) for prod in prods]
    for good in goods:
        # TODO: SKU 规格总汇计算太慢，有待处理。
        prod_id = good.get('objectId')
        # 查找 Pointer 对象，需要用 create_without_data。
        prod = Prod.create_without_data(prod_id)
        skus = Sku.query.equal_to('prod', prod).find()
        print(skus)
        total_stock = sum([sku.get('stock') for sku in skus])

        good['totalStock'] = total_stock
        good['imageUrl'] = good.get('mainPicUrl')
        good['priceText'] = '¥ ' + str(good.get('retailPrice'))
        good['skuCount'] = len(skus)

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

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for cate in categories:
        cate['id'] = cate.get('objectId')

    data = {
        'data': categories,
        'code': 0
    }
    return jsonify(data)
