# coding: utf-8

"""
    Algocash API

    This is a Algocash API  # noqa: E501

    OpenAPI spec version: 1.0.0
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from algocash_sdk.api_client import ApiClient


class DepositApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    """create a deposit  # noqa: E501
    :param str invoice_id: (required)
    :param str amount: (required)
    :param Payer payer: (required)
    :param Url url: (required)
    :param str payment_method: (required)
    :param async_req bool
    :return: DepositSuccess
                If the method is called asynchronously,
                returns the request thread.
    """
    def create_deposit(self, invoice_id, amount, payer, url, payment_method=None, async_req=False):  # noqa: E501

        # verify the required parameter 'invoice_id' is set
        if (invoice_id == '' or invoice_id is None):
            raise ValueError("Missing the required parameter `invoice_id` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'amount' is set
        if (amount == '' or amount is None):
            raise ValueError("Missing the required parameter `amount` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'payer' is set
        if (payer is None):
            raise ValueError("Missing the required parameter `payer` when calling `create_deposit`")  # noqa: E501
        # verify the required parameter 'url' is set
        if (url is None):
            raise ValueError("Missing the required parameter `url` when calling `create_deposit`")  # noqa: E501
        
        body_params = []
        
        body_params.append(('invoice_id', invoice_id))  # noqa: E501
        body_params.append(('amount', amount))  # noqa: E501
        body_params.append(('payer', payer))  # noqa: E501
        body_params.append(('payment_method', payment_method))  # noqa: E501
        body_params.append(('url', url))  # noqa: E501

        return self.api_client.call_api(
            '/payin', 'POST',
            body=body_params,
            response_type='DepositSuccess',  # noqa: E501
            async_req=async_req
            )
        
    def request_deposit_status(self, invoice_id, async_req=False):
        if (invoice_id == '' or invoice_id is None):
            raise ValueError("Missing the required parameter `invoice_id`")  # noqa: E501
        
        path_params = {}
        path_params['invoice_id'] = invoice_id
        
        return self.api_client.call_api(
            '/payin/status/{invoice_id}', 'GET',
            path_params=path_params,
            response_type='DepositStatusResponse',  # noqa: E501
            async_req=async_req
            )