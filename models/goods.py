import leancloud


class Prod(leancloud.Object):
    """SPU of products."""
    @property
    def pid(self):
        return self.get('pid')

    @pid.setter
    def pid(self, value):
        self.set('pid', value)

    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)

    @property
    def feat(self):
        return self.get('feat')

    @feat.setter
    def feat(self, value):
        self.set('feat', value)

    @property
    def price(self):
        return self.get('retailPrice')

    @price.setter
    def price(self, value):
        self.set('retailPrice', value)

    @property
    def is_same_price(self):
        return self.get('isSamePrice')

    @is_same_price.setter
    def is_same_price(self, value):
        self.set('isSamePrice', value)

    @property
    def is_one_price(self):
        return self.get('isOnePrice')

    @is_one_price.setter
    def is_one_price(self, value):
        self.set('isOnePrice', value)

    @property
    def is_all_sold_out(self):
        return self.get('isAllSoldOut')

    @is_all_sold_out.setter
    def is_all_sold_out(self, value):
        self.set('isAllSoldOut', value)

    @property
    def cate(self):
        return self.get('cate')

    @cate.setter
    def cate(self, id):
        self.set('cate', Cate.create_without_data(id))

    @property
    def brand(self):
        return self.get('brand')

    @brand.setter
    def brand(self, id):
        self.set('brand', Brand.create_without_data(id))

    @property
    def supplier(self):
        return self.get('supplier')

    @supplier.setter
    def supplier(self, id):
        self.set('supplier', Supplier.create_without_data(id))

    @property
    def main_pic_url(self):
        return self.get('mainPicUrl')

    @main_pic_url.setter
    def main_pic_url(self, value):
        self.set('mainPicUrl', value)

    @property
    def thumbnail_url(self):
        return self.get('thumbnailUrl')

    @thumbnail_url.setter
    def thumbnail_url(self, value):
        self.set('thumbnailUrl', value)

    @classmethod
    def get_skus(cls, id):
        return Sku.query.equal_to('prod', cls.create_without_data(id)).find()


class Sku(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)

    @property
    def full_name(self):
        return self.get('fullName')

    @full_name.setter
    def full_name(self, value):
        self.set('fullName', value)

    @property
    def price4(self):
        return self.get('price4')

    @price4.setter
    def price4(self, value):
        self.set('price4', value)

    @property
    def stock(self):
        return self.get('stock')

    @stock.setter
    def stock(self, value):
        self.set('stock', value)

    @property
    def size2(self):
        return self.get('size2')

    @size2.setter
    def size2(self, value):
        self.set('size2', value)

    @property
    def is_sold_out(self):
        return self.get('isSoldOut')

    @is_sold_out.setter
    def is_sold_out(self, value):
        self.set('isSoldOut', value)

    @property
    def size1(self):
        return self.get('size1')

    @size1.setter
    def size1(self, id):
        self.set('size1', Size.create_without_data(id))

    @property
    def color(self):
        return self.get('color')

    @color.setter
    def color(self, id):
        self.set('color', Color.create_without_data(id))

    @property
    def prod(self):
        return self.get('prod')

    @prod.setter
    def prod(self, id):
        self.set('prod', Prod.create_without_data(id))


class Cate(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)


class Brand(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)


class Color(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)

    @property
    def order(self):
        return self.get('order')

    @order.setter
    def order(self, value):
        self.set('order', value)


class Size(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)

    @property
    def order(self):
        return self.get('order')

    @order.setter
    def order(self, value):
        self.set('order', value)


class Supplier(leancloud.Object):
    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self.set('name', value)

    @property
    def phone(self):
        return self.get('phone')

    @phone.setter
    def phone(self, value):
        self.set('phone', value)

    @property
    def wxid(self):
        return self.get('wxid')

    @wxid.setter
    def wxid(self, value):
        self.set('wxid', value)
