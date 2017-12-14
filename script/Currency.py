from decimal import *

class Currency:
    @property
    def bank(self):
        return self.__bank

    @property
    def usd(self):
        return self.__usd_sell

    @property
    def time(self):
        return self.__time

    def __init__(self, bank, buy, sell):
        self.__bank = bank
        self.__usd_sell = Decimal(sell)
        self.__time = None

    def __str__(self):
        return '' + self.__bank + ' ' + str(self.__buy) + ' ' + str(self.__sell)