"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock
from cart import Cart
from producer import Producer


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = [];
        self.new_producer = 0;
        self.producers_lock = Lock();

        self.carts = [];
        self.new_cart = 0;
        self.carts_lock = Lock();
        pass

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers_lock.acquire();

        producer_id = self.new_producer;
        producers.append(([], Lock()));
        self.new_producer = self.new_producer + 1;

        self.producers_lock.release();
        return producer_id;

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        (product_list, list_lock) = self.producers[producer_id];

        added_product = False;
        list_lock.acquire();

        if (len(product_list) < self.queue_size_per_producer):
            product_list.append(product);
            added_product = True;
        else:
            added_product = False;

        list_lock.release();
        return added_product;

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_lock.acquire()
        cart_id = self.new_cart;
        self.new_cart = self.new_cart + 1
        self.carts_lock.release();

        self.carts.append(Cart(cart_id, []));
        return cart_id;

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.producers_lock.acquire();
        producers_no = self.new_producer;
        self.producers_lock.release();

        cart = self.carts[cart_id];
        for producer_id in range(0, producers_no):
            for (product_list, list_lock) in producers[producer_id]:
                list_lock.acquire();

                # if consumer found the desired product add it to list and remove it from producer
                if product in product_list:
                    product_list.remove(product);
                    cart.add(product, producer_id);
                    list_lock.release();
                    return True;
                list_lock.release();

        return False;

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id];
        producer_id = cart.remove(product);

        # Re-add the product
        (product_list, list_lock) = self.producers[producer_id];

        list_lock.acquire();
        product_list.append(product);
        list_lock.release();

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id].place_order();
