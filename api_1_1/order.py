import json
from pprint import pprint

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dump, lc_dumps
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color
from utils import login_required


Order = leancloud.Object.extend('Order')


@api.route('/orders', methods=['POST'])
@login_required
def create_order():
    user = leancloud.User.get_current()
    args = request.args if request.method == 'GET' else request.json
    pprint(args)
    print(type(args))
    order = Order()
    salesman = args.pop('salesman')
    salesman = leancloud.User.create_without_data(salesman.get('id'))
    order.set(args)
    order.set('customer', user)
    order.set('salesman', salesman)
    order.save()
    return jsonify({'data': 'Order saved.'})


@api.route('/orders')
@login_required
def get_orders():
    user = leancloud.User.get_current()
    orders = Order.query\
        .equal_to('customer', user)\
        .find()
    response = lc_dumps(orders)
    return jsonify({'data': response})


@api.route('/orders/staffs')
@login_required
def get_salesman():
    leancloud.use_master_key(True)
    role_query = leancloud.Query(leancloud.Role)
    role = role_query.equal_to('name', 'staff').first()
    user_relation = role.get_users()

    users = user_relation.query.select('nickName').find()
    leancloud.use_master_key(False)

    users = lc_dumps(users)
    return jsonify({'data': users})

