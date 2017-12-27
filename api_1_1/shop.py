import json

from . import api
from flask import jsonify, request

import leancloud

from utils import lc_dump, lc_dumps
from models.goods import Prod, Sku, Cate, Brand, Supplier, Size, Color


@api.route('/shops')
def get_info():
    data = {
        'type': '1'
    }
    return jsonify({'data': data})


@api.route('/shops/status')
def get_status():
    status = 'NORMAL'
    begin_time = '00:00'
    end_time = '23:59'
    open = True

    data =  {
        'status': status,
        'beginTime': begin_time,
        'endTime': end_time,
        'open': open,
    }
    return jsonify({'data': data})

