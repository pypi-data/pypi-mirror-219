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

class PayoutSuccess(object):
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
        'merchant_invoice_id': 'str',
        'transaction_id': 'str'
    }

    attribute_map = {
        'merchant_invoice_id': 'merchant_invoice_id',
        'transaction_id': 'transaction_id'
    }

    def __init__(self, merchant_invoice_id=None, transaction_id=None):  # noqa: E501
        """PayoutSuccess - a model defined in Swagger"""  # noqa: E501
        self._merchant_invoice_id = None
        self._transaction_id = None
        self.discriminator = None
        if merchant_invoice_id is not None:
            self.merchant_invoice_id = merchant_invoice_id
        if transaction_id is not None:
            self.transaction_id = transaction_id

    @property
    def merchant_invoice_id(self):
        """Gets the merchant_invoice_id of this PayoutSuccess.  # noqa: E501


        :return: The merchant_invoice_id of this PayoutSuccess.  # noqa: E501
        :rtype: str
        """
        return self._merchant_invoice_id

    @merchant_invoice_id.setter
    def merchant_invoice_id(self, merchant_invoice_id):
        """Sets the merchant_invoice_id of this PayoutSuccess.


        :param merchant_invoice_id: The merchant_invoice_id of this PayoutSuccess.  # noqa: E501
        :type: str
        """

        self._merchant_invoice_id = merchant_invoice_id

    @property
    def transaction_id(self):
        """Gets the transaction_id of this PayoutSuccess.  # noqa: E501


        :return: The transaction_id of this PayoutSuccess.  # noqa: E501
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this PayoutSuccess.


        :param transaction_id: The transaction_id of this PayoutSuccess.  # noqa: E501
        :type: str
        """

        self._transaction_id = transaction_id

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
        if issubclass(PayoutSuccess, dict):
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
        if not isinstance(other, PayoutSuccess):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
