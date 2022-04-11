from dataclasses import dataclass
from tema.product import Product

class Cart:
    def __init__(self, id, products):
        self.id = id;
        self.products = products;

    def add(self, product, producer_id):
        self.products.append((product, producer_id));

    def remove(self, target_product):
        for (product, prod_id) in self.products:
            if product == target_product:
                self.products.remove((product, prod_id));
                return prod_id;
    
    def place_order(self):
        products_only = [];

        for (product, prod_id) in self.products:
            products_only.append(product);

        return products_only;