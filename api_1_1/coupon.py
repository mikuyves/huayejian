import json

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dump, lc_dumps
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color


@api.route('/coupons/list')
def get_coupon_list():
    data = {
        'test': 'ok'
    }
    return jsonify({'data': data})
