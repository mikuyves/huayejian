import json

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dump, lc_dumps
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color


@api.route('/goods/')
def get_goods():
    # 分页参数。
    start = int(request.args.get('from', 0))
    count = int(request.args.get('limit', 20))
    category_id = request.args.get('category_id')
    status = request.args.get('goods_status')
    # 搜索关键字是 JSON 字符串，需要转换格式。
    keywords = request.args.get('search_keywords')
    print(request.args)

    # 分页获取对象。
    prod_query = Prod.query\
        .descending('createdAt')\
        .skip(start)\
        .limit(count)\
        .include('supplier')\
        .include('images')

    # 搜索
    if keywords:
        keywords = json.loads(keywords)
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
    # 处理 SKU 及前端需求字段。
    for good in goods:
        # TODO: SKU 规格总汇计算太慢，有待处理。
        prod_id = good.get('objectId')
        skus = Prod.get_skus(prod_id)
        print(skus)
        total_stock = sum([sku.get('stock') for sku in skus])

        # 小程序前端需求字段。
        good['totalStock'] = total_stock
        good['priceText'] = '¥ ' + str(good.get('retailPrice'))
        good['skuCount'] = len(skus)
        good['imageUrl'] = good.get('thumbnailUrl', '/images/icons/broken.png')

    print(goods)

    return jsonify({'data': goods})


@api.route('/goods', methods=['POST', 'PUT'])
def create_goods():
    """新建商品。"""
    leancloud.use_master_key(True)

    data = request.json
    print(data)
    # SPU
    prod_id = request.args.get('id') if request.method == 'PUT' else None
    if prod_id: # Update
        prod = Prod.create_without_data(prod_id)
    else: # Create
        prod = Prod()
        prod.pid = data.get('pid')

    prod.brand = data.get('brand').get('id')
    prod.cate = data.get('cate').get('id')
    prod.supplier = data.get('supplier').get('id')
    prod.price = data.get('retailPrice')
    prod.name = data.get('name')
    prod.feat = data.get('feat')
    prod.is_all_sold_out = data.get('isAllSoldOut')
    prod.is_same_price = data.get('isSamePrice')
    prod.is_one_price = data.get('isOnePrice')

    # Images
    leancloud.use_master_key(True)
    image_data = data.get('images')
    # images = [
    #     leancloud.File.create_without_data(i.get('objectId')) for i in image_data
    # ]
    images = []
    for i in image_data:
        id_ = i.get('id') if i.get('id') else i.get('objectId')
        image = leancloud.File.create_without_data(id_)
        images.append(image)

    print(images)

    prod.images = images
    main_pic = images[0]
    prod.main_pic = main_pic
    main_pic.fetch()
    prod.main_pic_url = main_pic.url
    prod.thumbnail_url = main_pic.get_thumbnail_url(100, 100)

    prod.save()

    # SKU
    sku_data = data.get('skuList')
    skus = []
    for s in sku_data:
        sku_id = s.get('objectId')
        if sku_id:  # Update
            sku = Sku.create_without_data(sku_id)
        else:  # Create
            sku = Sku()
        # 前端传过来的 size1，color 的数据类型是 Object，不能直接存。
        # 之前在小程序端，直接用 sdk 传对象的方法行不通。要用 create_without_data 包装。
        sku.size1 = s.get('size1').get('id')
        sku.color = s.get('color').get('id')
        sku.full_name = s.get('fullName')
        sku.name = s.get('name')
        sku.price4 = s.get('price4')
        sku.size2 = s.get('size2')
        sku.stock = s.get('stock')
        sku.is_sold_out = s.get('isSoldOut')
        sku.prod = prod.id
        sku.save()

    # 从数据库中删除图片。
    deleted_pics = data.get('deletedPics')
    for id_ in deleted_pics:
        p = leancloud.File.create_without_data(id_)
        p.destroy()
    # 删除 SKU。
    deleted_skus_ids = data.get('deletedSkuIds')
    for id_ in deleted_skus_ids:
        s = Sku.create_without_data(id_)
        s.destroy()

    leancloud.use_master_key(False)
    return jsonify({'msg': 'saved'})


@api.route('/goods/detail')
def get_detail():
    args = request.args
    print(args)
    _id = args.get('id')

    prod = Prod.create_without_data(_id)

    prod.fetch(
        # fetch: 从云端数据库获取数据到本地（服务器），使用后会覆盖本地数据。
        # select: 选择字段，可节省流浪。
        # include: 获取 Pointer 的数据。
        include=['brand', 'cate', 'supplier', 'images']
    )
    skus = prod.get_skus_with_detail()

    data = {
        'prod': lc_dump(prod),
        'skus': lc_dumps(skus)
    }
    print(data)

    return jsonify({'data': data})



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


@api.route('/goods/home_discover')
def home_discover():
    prods = Prod.query.descending('createdAt').limit(10).find()

    prods = lc_dumps(prods)

    data = {
        'list': prods,
        'code': 0
    }
    print(data)
    return jsonify({'data': data})

