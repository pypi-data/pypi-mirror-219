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

class Payer(object):
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
        'email': 'str',
        'phone': 'str',
        'id': 'str',
        'document': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'address': 'Address'
    }

    attribute_map = {
        'email': 'email',
        'phone': 'phone',
        'id': 'id',
        'document': 'document',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'address': 'address'
    }

    def __init__(self, email, phone, id=None, document=None, first_name=None, last_name=None, address=None):  # noqa: E501
        """Payer - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._document = None
        self._first_name = None
        self._last_name = None
        self._phone = None
        self._email = None
        self._address = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if document is not None:
            self.document = document
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.phone = phone
        self.email = email
        if address is not None:
            self.address = address

    @property
    def id(self):
        """Gets the id of this Payer.  # noqa: E501

        Customer's ID generated on merchant’s end  # noqa: E501

        :return: The id of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Payer.

        Customer's ID generated on merchant’s end  # noqa: E501

        :param id: The id of this Payer.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def document(self):
        """Gets the document of this Payer.  # noqa: E501


        :return: The document of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._document

    @document.setter
    def document(self, document):
        """Sets the document of this Payer.


        :param document: The document of this Payer.  # noqa: E501
        :type: str
        """

        self._document = document

    @property
    def first_name(self):
        """Gets the first_name of this Payer.  # noqa: E501


        :return: The first_name of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this Payer.


        :param first_name: The first_name of this Payer.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this Payer.  # noqa: E501


        :return: The last_name of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this Payer.


        :param last_name: The last_name of this Payer.  # noqa: E501
        :type: str
        """

        self._last_name = last_name

    @property
    def phone(self):
        """Gets the phone of this Payer.  # noqa: E501


        :return: The phone of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this Payer.


        :param phone: The phone of this Payer.  # noqa: E501
        :type: str
        """
        if phone is None:
            raise ValueError("Invalid value for `phone`, must not be `None`")  # noqa: E501

        self._phone = phone

    @property
    def email(self):
        """Gets the email of this Payer.  # noqa: E501


        :return: The email of this Payer.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Payer.


        :param email: The email of this Payer.  # noqa: E501
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def address(self):
        """Gets the address of this Payer.  # noqa: E501


        :return: The address of this Payer.  # noqa: E501
        :rtype: Address
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Payer.


        :param address: The address of this Payer.  # noqa: E501
        :type: Address
        """

        self._address = address

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
        if issubclass(Payer, dict):
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
        if not isinstance(other, Payer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
