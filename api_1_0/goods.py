import json

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dumps
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
    goods = lc_dumps(prods)
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

    return jsonify({'data': goods})


@api.route('/goods', methods=['POST'])
def create_goods():
    data = request.json
    print(data)
    # SPU
    prod = Prod()
    prod.brand = data.get('brand').get('id')
    prod.cate = data.get('cate').get('id')
    prod.supplier = data.get('supplier').get('id')
    prod.pid = data.get('pid')
    prod.price = data.get('retailPrice')
    prod.name = data.get('name')
    prod.feat = data.get('feat')
    prod.is_all_sold_out = data.get('isAllSoldOut')
    prod.is_same_price = data.get('isSamePrice')
    prod.is_one_price = data.get('isOnePrice')
    prod.main_pic_url = data.get('images')[0].get('url')
    main_pic_id = data.get('images')[0].get('objectId')
    # 生成缩略图。
    image = leancloud.File.create_without_data(main_pic_id)
    image.fetch()
    prod.thumbnail_url = image.get_thumbnail_url(100, 100)
    prod.save()

    return jsonify({'msg': 'saved'})


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
    cates = lc_dumps(cates)

    return jsonify({'data': cates})


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
    brands = lc_dumps(brands)

    return jsonify({'data': brands})


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
    suppliers = lc_dumps(suppliers)

    return jsonify({'data': suppliers})


@api.route('/goods/sizes')
def get_sizes():
    sizes = Size.query.ascending('order').find()
    sizes = lc_dumps(sizes)

    return jsonify({'data': sizes})


@api.route('/goods/colors')
def get_colors():
    colors = Color.query.ascending('order').find()
    colors = lc_dumps(colors)

    return jsonify({'data': colors})
