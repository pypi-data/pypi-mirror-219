# coding: utf-8

"""
    Algocash API

    This is a Algocash API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: loganph.work@gmail.com
    
"""

from __future__ import absolute_import

import unittest

import algocash_sdk
from algocash_sdk.api.payout_api import PayoutApi  # noqa: E501
from algocash_sdk.rest import ApiException
from pprint import pprint
import json


class TestPayoutApi(unittest.TestCase):
    """PayoutApi unit test stubs"""

    def setUp(self):
        self.api = PayoutApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_payout(self):
        """Test case for create_payout

        create payout  # noqa: E501
        """
        configuration = algocash_sdk.Configuration()
        # configuration.host = 'https://dd1e-5-31-3-154.ngrok-free.app'
        configuration.merchant_key = 'sWBYGvzA61ITU4Vh'
        configuration.merchant_secret = 'OfeR3xi59rLAM9c1'
        configuration.api_access_token = '4q4epHrbUHykQwnc'
        configuration.devmode = True

        # create an instance of the API class
        api_instance = algocash_sdk.PayoutApi(algocash_sdk.ApiClient(configuration))
        invoice_id = '100003438351' # str | 
        amount = '100' # str | 
        payer = algocash_sdk.Payer('test@gmail.com', '+918885916123') # Payer 
        payment_method = 'UPI' # str | 
        bank_account = algocash_sdk.Bank('712442638', '84932568207', 'first name last name') # Bank | 
        url = algocash_sdk.Url('https://localhost:8080/callback') # Url | 

        try:
            # create payout
            api_response = api_instance.create_payout(invoice_id, amount, payer, bank_account, url, payment_method)
            pprint(api_response)
        except ValueError as e:
            print("ValueError Exception when calling PayoutApi->create_payout: %s\n" % e)
        except ApiException as e:
            print("Exception when calling PayoutApi->create_payout: %s\n" % e)
            pprint(json.loads(e.body))
        pass


if __name__ == '__main__':
    unittest.main()
