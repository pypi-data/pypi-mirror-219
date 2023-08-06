# coding: utf-8

"""
    Algocash API

    This is a Algocash API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: loganph.work@gmail.com
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from algocash_sdk.api_client import ApiClient


class PayoutApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    """create payout  # noqa: E501

        create a payout  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_payout(invoice_id, amount, payer, payment_method, bank_account, url, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str invoice_id: (required)
        :param str amount: (required)
        :param Payer payer: (required)
        :param str payment_method: (required)
        :param Bank bank_account: (required)
        :param Url url: (required)
        :return: PayoutSuccess
                 If the method is called asynchronously,
                 returns the request thread.
        """
    def create_payout(self, invoice_id, amount, payer, bank_account, url, payment_method=None, async_req=False):  # noqa: E501

        # verify the required parameter 'invoice_id' is set
        if (invoice_id == '' or invoice_id is None):
            raise ValueError("Missing the required parameter `invoice_id` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'amount' is set
        if (amount == '' or amount is None):
            raise ValueError("Missing the required parameter `amount` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'payer' is set
        if (payer is None):
            raise ValueError("Missing the required parameter `payer` when calling `create_deposit`")  # noqa: E501
        if (bank_account is None):
            raise ValueError("Missing the required parameter `bank_account` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'url' is set
        if (url is None):
            raise ValueError("Missing the required parameter `url` when calling `create_deposit`")  # noqa: E501

        body_params = []
        body_params.append(('invoice_id', invoice_id))  # noqa: E501
        body_params.append(('amount', amount))  # noqa: E501
        body_params.append(('payer', payer))  # noqa: E501
        body_params.append(('bank_account', bank_account))  # noqa: E501
        body_params.append(('payment_method', payment_method))  # noqa: E501
        body_params.append(('url', url))  # noqa: E501

        return self.api_client.call_api(
            '/payout', 'POST',
            body=body_params,
            response_type='PayoutSuccess',  # noqa: E501
            async_req=async_req
            )
        
    def request_payout_status(self, invoice_id, async_req=False):
        if (invoice_id == '' or invoice_id is None):
            raise ValueError("Missing the required parameter `invoice_id`")  # noqa: E501
        
        path_params = {}
        path_params['invoice_id'] = invoice_id
        
        return self.api_client.call_api(
            '/payout/status/{invoice_id}', 'GET',
            path_params=path_params,
            response_type='PayoutStatusResponse',  # noqa: E501
            async_req=async_req
            )