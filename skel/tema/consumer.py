"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a consumer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self);
        self.ops = carts;
        self.marketplace = marketplace;
        self.retry_wait_time = retry_wait_time;
        self.name = kwargs["name"];

    def run(self):
        cart_id = self.marketplace.new_cart();
        market = self.marketplace;

        # Take operation by operation and emulate the consumer
        for op in self.ops:
            op_type = op["type"];
            op_prod = op["prod"];
            op_quantity = op["quantity"];

            # Do it from 0 to quantity - 1 times
            for i in range(0, op_quantity):
                # Add operation
                if (op_type == "add"):
                    added_to_cart = False

                    while not added_to_cart:
                        added_to_cart = market.add_to_cart(cart_id, op_prod);
                        if not added_to_cart:
                            time.sleep(self.retry_wait_time)
                # Remove operation
                elif (op_type == "remove"):
                    market.remove_cart(cart_id, op_prod);
                else:
                    print("ERROR OPPERATION NOT KNOWN");

        for product in self.marketplace.place_order(cart_id):
            print(self.name + " bought " + product);