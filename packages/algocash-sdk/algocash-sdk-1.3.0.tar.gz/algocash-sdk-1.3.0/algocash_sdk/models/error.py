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

class Error(object):
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
        'code': 'str',
        'description': 'str',
        'type': 'str'
    }

    attribute_map = {
        'code': 'code',
        'description': 'description',
        'type': 'type'
    }

    def __init__(self, code=None, description=None, type=None):  # noqa: E501
        """Error - a model defined in Swagger"""  # noqa: E501
        self._code = None
        self._description = None
        self._type = None
        self.discriminator = None
        if code is not None:
            self.code = code
        if description is not None:
            self.description = description
        if type is not None:
            self.type = type

    @property
    def code(self):
        """Gets the code of this Error.  # noqa: E501


        :return: The code of this Error.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Error.


        :param code: The code of this Error.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def description(self):
        """Gets the description of this Error.  # noqa: E501


        :return: The description of this Error.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Error.


        :param description: The description of this Error.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def type(self):
        """Gets the type of this Error.  # noqa: E501


        :return: The type of this Error.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Error.


        :param type: The type of this Error.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(Error, dict):
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
        if not isinstance(other, Error):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
