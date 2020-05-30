#import schwifty
from baangt.base.Faker import Faker
import random


class IBAN:
    def __init__(self, bankLeitZahl='20151', bankLand='AT'):
        """
        Class to generate random IBAN-Numbers. Mainly used in test data generation either on-the-fly or upfront
        during creation of a testdata XLSX.

        @param bankLeitZahl: Valid Bankcode (old format)
        @param bankLand: Valid Bank country in ISO-Format
        """
        self.bankLeitZahl = bankLeitZahl
        self.bankLand = bankLand

    def getRandomIBAN(self):
        """
        Generates a random IBAN based on bankLand and bankLeitzahl as well as a random account number

        @return: gives a String of IBAN
        """
        laenge = random.randrange(6, 10)
        digits = []
        for n in range(laenge):
            digits.append(random.randrange(0, 10))
        digits = "".join(str(x) for x in digits)
        #return str(schwifty.IBAN.generate(country_code=self.bankLand,
        #                                  bank_code=self.bankLeitZahl,
        #                                  account_code=digits))
        return Faker().fakerProxy(fakerMethod="iban")


if __name__ == '__main__':
    l = IBAN()
    print(l.getRandomIBAN())
