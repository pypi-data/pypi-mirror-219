# coding: utf-8

"""
    Algocash API

    This is a Algocash API  

    OpenAPI spec version: 1.0.0
    Contact: loganph.work@gmail.com
"""

import pprint
import re  # noqa: F401

import six

class PayoutStatusResponse(object):
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
        'response': 'str',
        'info': 'PayoutStatusInfo',
    }

    attribute_map = {
        'response': 'response',
        'info': 'info'
    }

    def __init__(self, response=None, info=None):  
        """PayoutStatusResponse - a model defined"""  
        self._response = None
        self._info = None
        self.discriminator = None
        if response is not None:
            self._response = response
        if info is not None:
            self._info = info

    @property
    def response(self):
        """Gets the response of this PayoutStatusResponse.  


        :return: The response of this PayoutStatusResponse.  
        :rtype: str
        """
        return self._response

    @response.setter
    def response(self, response):
        """Sets the response of this PayoutStatusResponse.


        :param response: The response of this PayoutStatusResponse.  
        :type: str
        """

        self._response = response

    @property
    def info(self):
        """Gets the info of this PayoutStatusResponse.  


        :return: The info of this PayoutStatusResponse.  
        :rtype: PayoutStatusInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this PayoutStatusResponse.


        :param info: The info of this PayoutStatusResponse.  
        :type: PayoutStatusInfo
        """

        self._info = info

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
        if issubclass(PayoutStatusResponse, dict):
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
        if not isinstance(other, PayoutStatusResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
