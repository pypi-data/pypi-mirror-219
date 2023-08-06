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
from algocash_sdk.configuration import Configuration
from algocash_sdk.api_client import ApiClient
from pprint import pprint
import json


class TestPayoutStatusApi(unittest.TestCase):
    """TestPayoutStatusApi unit test stubs"""

    def setUp(self):
        self.api = PayoutApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_request_payout_status(self):
        """Test case for request_payout_status

        create a payout  # noqa: E501
        """

        configuration = Configuration()
        configuration.merchant_key = 'sWBYGvzA61ITU4Vh'
        configuration.merchant_secret = 'OfeR3xi59rLAM9c1'
        configuration.api_access_token = '4q4epHrbUHykQwnc'
        configuration.devmode = True

        client = ApiClient(configuration)

        # create an instance of the API class
        api_instance = PayoutApi(client)
        invoice_id = '100003438351' # str | 

        try:
            # create a payout
            api_response = api_instance.request_payout_status(invoice_id)
            pprint(api_response)
        except ValueError as e:
            print("ValueError Exception when calling TestPayoutStatusApi->request_payout_status: %s\n" % e)
        except ApiException as e:
            print("Exception when calling TestPayoutStatusApi->request_payout_status: %s\n" % e)
            pprint(json.loads(e.body))
        pass


if __name__ == '__main__':
    unittest.main()
