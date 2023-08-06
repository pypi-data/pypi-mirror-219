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
from algocash_sdk.api.deposit_api import DepositApi  # noqa: E501
from algocash_sdk.rest import ApiException
from algocash_sdk.configuration import Configuration
from algocash_sdk.api_client import ApiClient
from pprint import pprint
import json


class TestDepositApi(unittest.TestCase):
    """DepositApi unit test stubs"""

    def setUp(self):
        self.api = DepositApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_deposit(self):
        """Test case for create_deposit

        create a deposit  # noqa: E501
        """

        configuration = Configuration()
        # configuration.host = 'https://dd1e-5-31-3-154.ngrok-free.app'
        configuration.merchant_key = 'sWBYGvzA61ITU4Vh'
        configuration.merchant_secret = 'OfeR3xi59rLAM9c1'
        configuration.api_access_token = '4q4epHrbUHykQwnc'
        configuration.devmode = True

        client = ApiClient(configuration)

        # create an instance of the API class
        api_instance = DepositApi(client)
        invoice_id = '47602' # str | 
        amount = '100' # str | 
        payer = algocash_sdk.Payer('test@gmail.com', '+918885916123') # Payer 
        payment_method = 'UPI' # str | 
        base = 'https://1836-204-188-232-195.ngrok-free.app'
        url = algocash_sdk.Url(base, 'https://localhost:8080/pending', 'https://localhost:8080/success', 'https://localhost:8080/error') # Url | 

        try:
            # create a deposit
            api_response = api_instance.create_deposit(invoice_id, amount, payer, url, payment_method)
            pprint(api_response)
        except ValueError as e:
            print("ValueError Exception when calling DepositApi->create_deposit: %s\n" % e)
        except ApiException as e:
            print("Exception when calling DepositApi->create_deposit: %s\n" % e)
            pprint(json.loads(e.body))
        pass


if __name__ == '__main__':
    unittest.main()
