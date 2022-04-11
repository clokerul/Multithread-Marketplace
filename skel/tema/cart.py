from dataclasses import dataclass
from product import Product

@dataclass(init=True, repr=True, order=False, frozen=True)
class Cart(object):
    id: str
    products: list[Product]
    
    def add(self, product, producer_id):
        products.append((product, producer_id));

    def remove(self, target_product):
        for (product, prod_id) in products:
            if product == target_product:
                products.remove((product, prod_id));
                return prod_id;
    
    def place_order(self):
        products_only = [];

        for (product, prod_id) in products:
            products_only.append(product);

        return products_only;