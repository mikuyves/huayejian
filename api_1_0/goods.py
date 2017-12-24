import json

from . import api
from flask import jsonify, request

import leancloud

from utils import obj_to_dict
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color


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
        skus = Prod.get_skus(prod_id)
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


@api.route('/goods', methods=['POST'])
def create_goods():
    data = request.json
    print(data)
    brand = data.get('brannd')
    brand_id = brand.get('id')
    cate = data.get('cate')
    cate_id = cate.get('id')
    feat = data.get('feat')
    is_all_sold_out = data.get('isAllSoldOut')
    is_same_price = data.get('isSamePrice')
    print(type(is_same_price))
    return jsonify({'test': 200, 'code': 0})


@api.route('/goods/inner_category', methods=['GET', 'POST'])
def get_cates():
    args = request.args if request.method == 'GET' else request.json
    print(args)
    name = args.get('name')
    if name:
        new_cate = Cate()
        new_cate.name = name
        new_cate.save()

    cates = Cate.query.ascending('createdAt').find()
    categories = [obj_to_dict(cate) for cate in cates]

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for cate in categories:
        cate['id'] = cate.get('objectId')

    data = {
        'data': categories,
        'code': 0
    }
    return jsonify(data)


@api.route('/goods/brands', methods=['GET', 'POST'])
def get_brands():
    args = request.args if request.method == 'GET' else request.json
    print(args)
    name = args.get('name')
    if name:
        new_brand = Brand()
        new_brand.name = name
        new_brand.save()

    brands = Brand.query.limit(300).ascending('name').find()
    brands = [obj_to_dict(b) for b in brands]

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for brand in brands:
        brand['id'] = brand.get('objectId')

    data = {
        'data': brands,
        'code': 0
    }
    return jsonify(data)


@api.route('/goods/suppliers', methods=['GET', 'POST'])
def get_suppliers():
    args = request.args if request.method == 'GET' else request.json
    print(args)
    name = args.get('name')
    if name:
        new_supplier = Supplier()
        new_supplier.name = name
        new_supplier.save()

    suppliers = Supplier.query.ascending('name').limit(300).find()
    suppliers = [obj_to_dict(s) for s in suppliers]

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for supplier in suppliers:
        supplier['id'] = supplier.get('objectId')

    data = {
        'data': suppliers,
        'code': 0
    }
    return jsonify(data)


@api.route('/goods/sizes')
def get_sizes():
    sizes = Size.query.ascending('order').find()
    sizes = [obj_to_dict(s) for s in sizes]

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for size in sizes:
        size['id'] = size.get('objectId')

    data = {
        'data': sizes,
        'code': 0
    }
    return jsonify(data)


@api.route('/goods/colors')
def get_colors():
    colors = Color.query.ascending('order').find()
    colors = [obj_to_dict(c) for c in colors]

    # 前段 slider_selector 模板需要对象的 id 字段进行选择。
    for color in colors:
        color['id'] = color.get('objectId')

    data = {
        'data': colors,
        'code': 0
    }
    return jsonify(data)
