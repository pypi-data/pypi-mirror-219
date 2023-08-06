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

class CallbackPayload(object):
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
        'status': 'str',
        'transaction_id': 'str',
        'merchant_invoice_id': 'str',
        'amount': 'str',
        'currency': 'str',
        'fee_amount': 'str',
        'fee_currency': 'str'
    }

    attribute_map = {
        'status': 'status',
        'transaction_id': 'transaction_id',
        'merchant_invoice_id': 'merchant_invoice_id',
        'amount': 'amount',
        'currency': 'currency',
        'fee_amount': 'fee_amount',
        'fee_currency': 'fee_currency'
    }

    def __init__(self, status=None, transaction_id=None, merchant_invoice_id=None, amount=None, currency=None, fee_amount=None, fee_currency=None):  # noqa: E501
        """CallbackPayload - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._transaction_id = None
        self._merchant_invoice_id = None
        self._amount = None
        self._currency = None
        self._fee_amount = None
        self._fee_currency = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if transaction_id is not None:
            self.transaction_id = transaction_id
        if merchant_invoice_id is not None:
            self.merchant_invoice_id = merchant_invoice_id
        if amount is not None:
            self.amount = amount
        if currency is not None:
            self.currency = currency
        if fee_amount is not None:
            self.fee_amount = fee_amount
        if fee_currency is not None:
            self.fee_currency = fee_currency

    @property
    def status(self):
        """Gets the status of this CallbackPayload.  # noqa: E501

        created, pending, expired, canceled, completed, failed, rejected  # noqa: E501

        :return: The status of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CallbackPayload.

        created, pending, expired, canceled, completed, failed, rejected  # noqa: E501

        :param status: The status of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def transaction_id(self):
        """Gets the transaction_id of this CallbackPayload.  # noqa: E501

        Your merchant ID  # noqa: E501

        :return: The transaction_id of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this CallbackPayload.

        Your merchant ID  # noqa: E501

        :param transaction_id: The transaction_id of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._transaction_id = transaction_id

    @property
    def merchant_invoice_id(self):
        """Gets the merchant_invoice_id of this CallbackPayload.  # noqa: E501

        Unique deposit ID on the merchant’s end from request  # noqa: E501

        :return: The merchant_invoice_id of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._merchant_invoice_id

    @merchant_invoice_id.setter
    def merchant_invoice_id(self, merchant_invoice_id):
        """Sets the merchant_invoice_id of this CallbackPayload.

        Unique deposit ID on the merchant’s end from request  # noqa: E501

        :param merchant_invoice_id: The merchant_invoice_id of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._merchant_invoice_id = merchant_invoice_id

    @property
    def amount(self):
        """Gets the amount of this CallbackPayload.  # noqa: E501

        Deposit fee amount in the currency specified  # noqa: E501

        :return: The amount of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this CallbackPayload.

        Deposit fee amount in the currency specified  # noqa: E501

        :param amount: The amount of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._amount = amount

    @property
    def currency(self):
        """Gets the currency of this CallbackPayload.  # noqa: E501

        Currency code of the amount in ISO 4217 format  # noqa: E501

        :return: The currency of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this CallbackPayload.

        Currency code of the amount in ISO 4217 format  # noqa: E501

        :param currency: The currency of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def fee_amount(self):
        """Gets the fee_amount of this CallbackPayload.  # noqa: E501

        Deposit fee amount in the currency specified  # noqa: E501

        :return: The fee_amount of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._fee_amount

    @fee_amount.setter
    def fee_amount(self, fee_amount):
        """Sets the fee_amount of this CallbackPayload.

        Deposit fee amount in the currency specified  # noqa: E501

        :param fee_amount: The fee_amount of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._fee_amount = fee_amount

    @property
    def fee_currency(self):
        """Gets the fee_currency of this CallbackPayload.  # noqa: E501

        Currency code of the amount in ISO 4217 format  # noqa: E501

        :return: The fee_currency of this CallbackPayload.  # noqa: E501
        :rtype: str
        """
        return self._fee_currency

    @fee_currency.setter
    def fee_currency(self, fee_currency):
        """Sets the fee_currency of this CallbackPayload.

        Currency code of the amount in ISO 4217 format  # noqa: E501

        :param fee_currency: The fee_currency of this CallbackPayload.  # noqa: E501
        :type: str
        """

        self._fee_currency = fee_currency

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
        if issubclass(CallbackPayload, dict):
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
        if not isinstance(other, CallbackPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
