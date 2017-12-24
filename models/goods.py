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
        self.set(value)

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
        Cate = leancloud.Object.extend('Cate')
        self.set('cate', Cate.create_without_data(id))

    @property
    def brand(self):
        return self.get('brand')

    @brand.setter
    def brand(self, id):
        Brand = leancloud.Object.extend('Brand')
        self.set('brand', Brand.create_without_data(id))

    @property
    def supplier(self):
        return self.get('supplier')

    @supplier.setter
    def supplier(self, id):
        Supplier = leancloud.Object.extend('Supplier')
        self.set('supplier', Supplier.create_without_data(id))

