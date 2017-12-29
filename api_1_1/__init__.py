from flask import Blueprint

api = Blueprint('api_1_1', __name__)

from . import goods, shop, coupon, order