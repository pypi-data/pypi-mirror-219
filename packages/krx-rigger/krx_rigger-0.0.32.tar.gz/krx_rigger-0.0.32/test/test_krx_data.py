import logging

import unittest

from krx import KrxDataWeb

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestKrxData(unittest.TestCase):
    def test_call_parties(self):
        krx_data = KrxDataWeb()
        r = krx_data.get_trading_info_each_participant()
        logger.debug(r)

    def test_fetch_stock_info_df(self):
        krx_data = KrxDataWeb()
        text = krx_data.fetch_stock_info()
        print(text)
