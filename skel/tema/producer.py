"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs);
        self.ops = products;
        self.marketplace = marketplace;
        self.republish_wait_time = republish_wait_time;
        self.name = kwargs["name"];

    def run(self):
        self.id = self.marketplace.register_producer();
        
        while True:
            for op in self.ops:
                op_prodid = op[0];
                op_quantity = op[1];
                op_produce_time = op[2];
                
                # Do it from 0 to quantity - 1 times
                for i in range(0, op_quantity):
                    added_product = False

                    # Try to add product
                    while not added_product:
                        time.sleep(op_produce_time);
                        added_product = self.marketplace.publish(self.id, op_prodid);
                        if not added_product:
                            time.sleep(self.republish_wait_time)