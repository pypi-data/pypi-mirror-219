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

class Address(object):
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
        'street': 'str',
        'city': 'str',
        'state': 'str',
        'zip_code': 'str'
    }

    attribute_map = {
        'street': 'street',
        'city': 'city',
        'state': 'state',
        'zip_code': 'zip_code'
    }

    def __init__(self, street=None, city=None, state=None, zip_code=None):  # noqa: E501
        """Address - a model defined in Swagger"""  # noqa: E501
        self._street = None
        self._city = None
        self._state = None
        self._zip_code = None
        self.discriminator = None
        if street is not None:
            self.street = street
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if zip_code is not None:
            self.zip_code = zip_code

    @property
    def street(self):
        """Gets the street of this Address.  # noqa: E501


        :return: The street of this Address.  # noqa: E501
        :rtype: str
        """
        return self._street

    @street.setter
    def street(self, street):
        """Sets the street of this Address.


        :param street: The street of this Address.  # noqa: E501
        :type: str
        """

        self._street = street

    @property
    def city(self):
        """Gets the city of this Address.  # noqa: E501


        :return: The city of this Address.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this Address.


        :param city: The city of this Address.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def state(self):
        """Gets the state of this Address.  # noqa: E501


        :return: The state of this Address.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Address.


        :param state: The state of this Address.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def zip_code(self):
        """Gets the zip_code of this Address.  # noqa: E501


        :return: The zip_code of this Address.  # noqa: E501
        :rtype: str
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        """Sets the zip_code of this Address.


        :param zip_code: The zip_code of this Address.  # noqa: E501
        :type: str
        """

        self._zip_code = zip_code

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
        if issubclass(Address, dict):
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
        if not isinstance(other, Address):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
