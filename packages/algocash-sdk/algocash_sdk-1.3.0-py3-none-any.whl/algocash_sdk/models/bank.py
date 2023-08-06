# coding: utf-8

"""
    Algocash API

    This is a Algocash API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: loganph.work@gmail.com
    
"""

import pprint
import re  # noqa: F401
import json

import six

class Bank(object):
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
        'bank_account_number': 'str',
        'bank_code': 'str',
        'bank_beneficiary': 'str',
        'bank_branch': 'str',
        'bank_account_type': 'str'
    }

    attribute_map = {
        'bank_account_number': 'bank_account_number',
        'bank_code': 'bank_code',
        'bank_beneficiary': 'bank_beneficiary',
        'bank_branch': 'bank_branch',
        'bank_account_type': 'bank_account_type'
    }

    def __init__(self, bank_account_number, bank_code, bank_beneficiary, bank_branch=None, bank_account_type=None):  # noqa: E501
        """Bank - a model defined in Swagger"""  # noqa: E501
        self._bank_account_number = None
        self._bank_code = None
        self._bank_beneficiary = None
        self._bank_branch = None
        self._bank_account_type = None
        self.discriminator = None
        self.bank_account_number = bank_account_number
        self.bank_code = bank_code
        self.bank_beneficiary = bank_beneficiary
        if bank_branch is not None:
            self.bank_branch = bank_branch
        if bank_account_type is not None:
            self.bank_account_type = bank_account_type

    @property
    def bank_account_number(self):
        """Gets the bank_account_number of this Bank.  # noqa: E501


        :return: The bank_account_number of this Bank.  # noqa: E501
        :rtype: str
        """
        return self._bank_account_number

    @bank_account_number.setter
    def bank_account_number(self, bank_account_number):
        """Sets the bank_account_number of this Bank.


        :param bank_account_number: The bank_account_number of this Bank.  # noqa: E501
        :type: str
        """
        if bank_account_number is None:
            raise ValueError("Invalid value for `bank_account_number`, must not be `None`")  # noqa: E501

        self._bank_account_number = bank_account_number

    @property
    def bank_code(self):
        """Gets the bank_code of this Bank.  # noqa: E501


        :return: The bank_code of this Bank.  # noqa: E501
        :rtype: str
        """
        return self._bank_code

    @bank_code.setter
    def bank_code(self, bank_code):
        """Sets the bank_code of this Bank.


        :param bank_code: The bank_code of this Bank.  # noqa: E501
        :type: str
        """
        if bank_code is None:
            raise ValueError("Invalid value for `bank_code`, must not be `None`")  # noqa: E501

        self._bank_code = bank_code

    @property
    def bank_beneficiary(self):
        """Gets the bank_beneficiary of this Bank.  # noqa: E501


        :return: The bank_beneficiary of this Bank.  # noqa: E501
        :rtype: str
        """
        return self._bank_beneficiary

    @bank_beneficiary.setter
    def bank_beneficiary(self, bank_beneficiary):
        """Sets the bank_beneficiary of this Bank.


        :param bank_beneficiary: The bank_beneficiary of this Bank.  # noqa: E501
        :type: str
        """
        if bank_beneficiary is None:
            raise ValueError("Invalid value for `bank_beneficiary`, must not be `None`")  # noqa: E501

        self._bank_beneficiary = bank_beneficiary

    @property
    def bank_branch(self):
        """Gets the bank_branch of this Bank.  # noqa: E501


        :return: The bank_branch of this Bank.  # noqa: E501
        :rtype: str
        """
        return self._bank_branch

    @bank_branch.setter
    def bank_branch(self, bank_branch):
        """Sets the bank_branch of this Bank.


        :param bank_branch: The bank_branch of this Bank.  # noqa: E501
        :type: str
        """

        self._bank_branch = bank_branch

    @property
    def bank_account_type(self):
        """Gets the bank_account_type of this Bank.  # noqa: E501


        :return: The bank_account_type of this Bank.  # noqa: E501
        :rtype: str
        """
        return self._bank_account_type

    @bank_account_type.setter
    def bank_account_type(self, bank_account_type):
        """Sets the bank_account_type of this Bank.


        :param bank_account_type: The bank_account_type of this Bank.  # noqa: E501
        :type: str
        """

        self._bank_account_type = bank_account_type

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
        if issubclass(Bank, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return json.dumps(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Bank):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other