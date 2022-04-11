"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock
from tema.cart import Cart
from tema.product import *
import logging
import unittest

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
        logging.basicConfig(filename='marketplace.log', level=logging.INFO)
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = []
        self.new_producer = 0
        self.producers_lock = Lock()

        self.carts = []
        self.new_cart_id = 0
        self.carts_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers_lock.acquire()

        producer_id = self.new_producer
        self.producers.append(([], Lock()))
        self.new_producer = self.new_producer + 1
        self.producers_lock.release()
        logging.info("Registered producer " + str(producer_id))
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        (product_list, list_lock) = self.producers[producer_id]

        added_product = False
        logging.info("Trying to publish product " + str(product))
        list_lock.acquire()

        if (len(product_list) < self.queue_size_per_producer):
            product_list.append(product)
            added_product = True
        else:
            added_product = False

        list_lock.release()
        logging.info("Published product " + str(product))
        return added_product

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_lock.acquire()
        cart_id = self.new_cart_id
        self.new_cart_id = self.new_cart_id + 1
        self.carts_lock.release()

        self.carts.append(Cart(cart_id, []))
        logging.info("New cart number " + str(cart_id))
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.producers_lock.acquire()
        logging.info("Producers lock aquired by cart " + str(cart_id))
        producers_no = self.new_producer
        self.producers_lock.release()
        logging.info("Producers released aquired by cart " + str(cart_id))

        cart = self.carts[cart_id]
        for producer_id in range(0, producers_no):
            (product_list, list_lock) = self.producers[producer_id]
            list_lock.acquire()
            logging.info("List lock acquired on producer " + str(producer_id))

            # if consumer found the desired product add it to list and remove it from producer
            if product in product_list:
                product_list.remove(product)
                cart.add(product, producer_id)
                list_lock.release()
                logging.info("List lock released on producer " + str(producer_id))
                logging.info("Product " + str(product) + " added to cart " + str(cart_id))
                return True

            logging.info("List lock released on producer " + str(producer_id))
            list_lock.release()

        logging.info("Product " + str(product) + " failed to add to cart " + str(cart_id))
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id]
        producer_id = cart.remove(product)

        # Re-add the product
        (product_list, list_lock) = self.producers[producer_id]

        list_lock.acquire()
        product_list.append(product)
        list_lock.release()
        logging.info("Product " + str(product) + " removed from cart " + str(cart_id))

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id].place_order()

class TestMarketPlace(unittest.TestCase):

    def setUp(self):
        self.marketplace = Marketplace(3)
    
    def test_register_producer(self):
        self.assertEqual(self.marketplace.register_producer(), 0)
        self.assertEqual(self.marketplace.register_producer(), 1)
    
    def test_publish(self):
        self.marketplace.register_producer()
        self.assertEqual(self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun")), False)

    def test_new_cart(self):
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.new_cart(), 1)

    def test_add_to_cart(self):
        self.marketplace.register_producer()
        self.marketplace.new_cart()
        self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun"))
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), False)

    def test_remove_from_cart(self):
        self.marketplace.register_producer()
        self.marketplace.new_cart()
        self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun"))
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.marketplace.remove_from_cart(0, Tea("Ceai", 15, "d-ala bun"))
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), False)

    def test_place_order(self):
        self.marketplace.register_producer()
        self.marketplace.new_cart()
        self.marketplace.publish(0, Tea("Ceai", 15, "d-ala bun"))
        self.assertEqual(self.marketplace.add_to_cart(0, Tea("Ceai", 15, "d-ala bun")), True)
        self.assertEqual(self.marketplace.place_order(0), [Tea(name='Ceai', price=15, type='d-ala bun')])