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

class Url(object):
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
        'callback_url': 'str',
        'pending_url': 'str',
        'success_url': 'str',
        'error_url': 'str',
        'back_url': 'str'
    }

    attribute_map = {
        'callback_url': 'callback_url',
        'pending_url': 'pending_url',
        'success_url': 'success_url',
        'error_url': 'error_url',
        'back_url': 'back_url'
    }

    def __init__(self, callback_url, pending_url=None, success_url=None, error_url=None, back_url=None):  # noqa: E501
        """Url - a model defined in Swagger"""  # noqa: E501
        self._callback_url = None
        self._pending_url = None
        self._success_url = None
        self._error_url = None
        self._back_url = None
        self.discriminator = None
        self.callback_url = callback_url
        if pending_url is not None:
            self.pending_url = pending_url
        if success_url is not None:
            self.success_url = success_url
        if error_url is not None:
            self.error_url = error_url
        if back_url is not None:
            self.back_url = back_url

    @property
    def callback_url(self):
        """Gets the callback_url of this Url.  # noqa: E501

        Valid URL over HTTPS used to receive the notifications about the deposit's changes of status  # noqa: E501

        :return: The callback_url of this Url.  # noqa: E501
        :rtype: str
        """
        return self._callback_url

    @callback_url.setter
    def callback_url(self, callback_url):
        """Sets the callback_url of this Url.

        Valid URL over HTTPS used to receive the notifications about the deposit's changes of status  # noqa: E501

        :param callback_url: The callback_url of this Url.  # noqa: E501
        :type: str
        """
        if callback_url is None:
            raise ValueError("Invalid value for `callback_url`, must not be `None`")  # noqa: E501

        self._callback_url = callback_url

    @property
    def pending_url(self):
        """Gets the pending_url of this Url.  # noqa: E501


        :return: The pending_url of this Url.  # noqa: E501
        :rtype: str
        """
        return self._pending_url

    @pending_url.setter
    def pending_url(self, pending_url):
        """Sets the pending_url of this Url.


        :param pending_url: The pending_url of this Url.  # noqa: E501
        :type: str
        """

        self._pending_url = pending_url

    @property
    def success_url(self):
        """Gets the success_url of this Url.  # noqa: E501


        :return: The success_url of this Url.  # noqa: E501
        :rtype: str
        """
        return self._success_url

    @success_url.setter
    def success_url(self, success_url):
        """Sets the success_url of this Url.


        :param success_url: The success_url of this Url.  # noqa: E501
        :type: str
        """

        self._success_url = success_url

    @property
    def error_url(self):
        """Gets the error_url of this Url.  # noqa: E501


        :return: The error_url of this Url.  # noqa: E501
        :rtype: str
        """
        return self._error_url

    @error_url.setter
    def error_url(self, error_url):
        """Sets the error_url of this Url.


        :param error_url: The error_url of this Url.  # noqa: E501
        :type: str
        """

        self._error_url = error_url

    @property
    def back_url(self):
        """Gets the back_url of this Url.  # noqa: E501


        :return: The back_url of this Url.  # noqa: E501
        :rtype: str
        """
        return self._back_url

    @back_url.setter
    def back_url(self, back_url):
        """Sets the back_url of this Url.


        :param back_url: The back_url of this Url.  # noqa: E501
        :type: str
        """

        self._back_url = back_url

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
        if issubclass(Url, dict):
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
        if not isinstance(other, Url):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other