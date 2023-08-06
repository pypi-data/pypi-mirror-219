# coding: utf-8

"""
    Algocash API

    This is a Algocash API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: loganph.work@gmail.com
    
"""

import pprint
import re  # noqa: F401

import six

class DepositRequest(object):
    """.

    Do not edit the class manually.
    """
    """
    Attributes:
      attribute_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    attribute_types = {
        'invoice_id': 'str',
        'amount': 'str',
        'payer': 'Payer',
        'payment_method': 'str',
        'url': 'Url'
    }

    attribute_map = {
        'invoice_id': 'invoice_id',
        'amount': 'amount',
        'payer': 'payer',
        'payment_method': 'payment_method',
        'url': 'url'
    }

    def __init__(self, invoice_id=None, amount=None, payer=None, payment_method=None, url=None):  # noqa: E501
        """DepositRequest - a model defined in Swagger"""  # noqa: E501
        self._invoice_id = None
        self._amount = None
        self._payer = None
        self._payment_method = None
        self._url = None
        self.discriminator = None
        self.invoice_id = invoice_id
        self.amount = amount
        self.payer = payer
        if payment_method is not None:
            self.payment_method = payment_method
        if url is not None:
            self.url = url

    @property
    def invoice_id(self):
        """Gets the invoice_id of this DepositRequest.  # noqa: E501

        Unique transaction ID (on the merchant end)  # noqa: E501

        :return: The invoice_id of this DepositRequest.  # noqa: E501
        :rtype: str
        """
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, invoice_id):
        """Sets the invoice_id of this DepositRequest.

        Unique transaction ID (on the merchant end)  # noqa: E501

        :param invoice_id: The invoice_id of this DepositRequest.  # noqa: E501
        :type: str
        """
        if invoice_id is None:
            raise ValueError("Invalid value for `invoice_id`, must not be `None`")  # noqa: E501

        self._invoice_id = invoice_id

    @property
    def amount(self):
        """Gets the amount of this DepositRequest.  # noqa: E501


        :return: The amount of this DepositRequest.  # noqa: E501
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this DepositRequest.


        :param amount: The amount of this DepositRequest.  # noqa: E501
        :type: str
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def payer(self):
        """Gets the payer of this DepositRequest.  # noqa: E501


        :return: The payer of this DepositRequest.  # noqa: E501
        :rtype: Payer
        """
        return self._payer

    @payer.setter
    def payer(self, payer):
        """Sets the payer of this DepositRequest.


        :param payer: The payer of this DepositRequest.  # noqa: E501
        :type: Payer
        """
        if payer is None:
            raise ValueError("Invalid value for `payer`, must not be `None`")  # noqa: E501

        self._payer = payer

    @property
    def payment_method(self):
        """Gets the payment_method of this DepositRequest.  # noqa: E501


        :return: The payment_method of this DepositRequest.  # noqa: E501
        :rtype: str
        """
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        """Sets the payment_method of this DepositRequest.


        :param payment_method: The payment_method of this DepositRequest.  # noqa: E501
        :type: str
        """

        self._payment_method = payment_method

    @property
    def url(self):
        """Gets the url of this DepositRequest.  # noqa: E501


        :return: The url of this DepositRequest.  # noqa: E501
        :rtype: Url
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this DepositRequest.


        :param url: The url of this DepositRequest.  # noqa: E501
        :type: Url
        """

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.attribute_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(DepositRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DepositRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
