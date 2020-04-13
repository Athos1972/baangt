import logging
from faker import Faker as FakerBase
from random import randint

logger = logging.getLogger("pyC")

class Faker:
    def __init__(self, locale="en-US"):
        self.faker = FakerBase()
        # Start with a random number
        self.faker.seed_instance(randint(10,1000))

    def fakerProxy(self, fakerMethod="email", **kwargs):
        """
        Dynamically call Faker's method and return the value back to the caller

        :param fakerMethod: Default "email"
        :param kwargs: Any arguments needed to execute a specific functionality
        :return: the value, that was delivered by Faker.
        """
        lValue = None
        try:
            lCallFakerMethod = getattr(self.faker, fakerMethod)
            lValue = lCallFakerMethod(**kwargs)
        except Exception as e:
            logging.error(f"Error during Faker-Call. Method was: {fakerMethod}, kwargs were: {kwargs}, Exception: {e}")

        return lValue
