import json
from pprint import pprint

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dump, lc_dumps
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color


Order = leancloud.Object.extend('Order')


@api.route('/orders', methods=['POST'])
def create_order():
    args = request.args if request.method == 'GET' else request.json
    pprint(args)
    print(type(args))
    order = Order()
    order.set(args)
    order.save()
    return jsonify({'data': 'Order saved.'})


@api.route('/orders')
def get_orders():
    orders = Order.query.find()
    response = lc_dumps(orders)
    return jsonify({'data': response})
