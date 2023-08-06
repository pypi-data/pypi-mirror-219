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

class DepositStatusInfo(object):

    """
    Attributes:
      attribute_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    attribute_types = {
        'id': 'str',
        'status': 'str',
        'merchant_tx_id': 'str',
        'request_amount': 'str',
        'request_dt': 'str',
        'collected_amount': 'str',
        'fee_amount': 'str',
        'chargeback_status': 'str',
    }

    attribute_map = {
        'id': 'id',
        'status': 'status',
        'merchant_tx_id': 'merchant_tx_id',
        'request_amount': 'request_amount',
        'request_dt': 'request_dt',
        'collected_amount': 'collected_amount',
        'fee_amount': 'fee_amount',
        'chargeback_status': 'chargeback_status',
    }

    def __init__(self, id=None, status=None, merchant_tx_id=None, request_amount=None, request_dt=None, collected_amount=None, fee_amount=None, chargeback_status=None):  
        """DepositStatusInfo"""  
        self._id = None
        self._status = None
        self._merchant_tx_id = None
        self._request_amount = None
        self._request_dt = None
        self._collected_amount = None
        self._fee_amount = None
        self._chargeback_status = None
        self.discriminator = None
        if id is not None:
            self._id = id
        if status is not None:
            self._status = status
        if merchant_tx_id is not None:
            self._merchant_tx_id = merchant_tx_id
        if request_amount is not None:
            self._request_amount = request_amount
        if request_dt is not None:
            self._request_dt = request_dt
        if collected_amount is not None:
            self._collected_amount = collected_amount
        if fee_amount is not None:
            self._fee_amount = fee_amount
        if chargeback_status is not None:
            self._chargeback_status = chargeback_status

    @property
    def id(self):
        """Gets the id of this DepositStatusInfo.  


        :return: The id of this DepositStatusInfo.  
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DepositStatusInfo.


        :param id: The id of this DepositStatusInfo.  
        :type: str
        """

        self._id = id

    @property
    def status(self):
        """Gets the status of this DepositStatusInfo.  


        :return: The status of this DepositStatusInfo.  
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DepositStatusInfo.


        :param status: The status of this DepositStatusInfo.  
        :type: str
        """

        self._status = status

    @property
    def merchant_tx_id(self):
        """Gets the merchant_tx_id of this DepositStatusInfo.  


        :return: The merchant_tx_id of this DepositStatusInfo.  
        :rtype: str
        """
        return self._merchant_tx_id

    @merchant_tx_id.setter
    def merchant_tx_id(self, merchant_tx_id):
        """Sets the merchant_tx_id of this DepositStatusInfo.


        :param merchant_tx_id: The merchant_tx_id of this DepositStatusInfo.  
        :type: str
        """

        self._merchant_tx_id = merchant_tx_id
        
    @property
    def request_amount(self):
        """Gets the request_amount of this DepositStatusInfo.  


        :return: The request_amount of this DepositStatusInfo.  
        :rtype: str
        """
        return self._request_amount

    @request_amount.setter
    def request_amount(self, request_amount):
        """Sets the request_amount of this DepositStatusInfo.


        :param request_amount: The request_amount of this DepositStatusInfo.  
        :type: str
        """

        self._request_amount = request_amount
        
    @property
    def request_dt(self):
        """Gets the request_dt of this DepositStatusInfo.  


        :return: The request_dt of this DepositStatusInfo.  
        :rtype: str
        """
        return self._request_dt

    @request_dt.setter
    def request_dt(self, request_dt):
        """Sets the request_dt of this DepositStatusInfo.


        :param request_dt: The request_dt of this DepositStatusInfo.  
        :type: str
        """

        self._request_dt = request_dt
        
    @property
    def collected_amount(self):
        """Gets the collected_amount of this DepositStatusInfo.  


        :return: The collected_amount of this DepositStatusInfo.  
        :rtype: str
        """
        return self._collected_amount

    @collected_amount.setter
    def collected_amount(self, collected_amount):
        """Sets the collected_amount of this DepositStatusInfo.


        :param collected_amount: The collected_amount of this DepositStatusInfo.  
        :type: str
        """

        self._collected_amount = collected_amount
        
    @property
    def fee_amount(self):
        """Gets the fee_amount of this DepositStatusInfo.  


        :return: The fee_amount of this DepositStatusInfo.  
        :rtype: str
        """
        return self._fee_amount

    @fee_amount.setter
    def fee_amount(self, fee_amount):
        """Sets the fee_amount of this DepositStatusInfo.


        :param fee_amount: The fee_amount of this DepositStatusInfo.  
        :type: str
        """

        self._fee_amount = fee_amount
        
    @property
    def chargeback_status(self):
        """Gets the chargeback_status of this DepositStatusInfo.  


        :return: The chargeback_status of this DepositStatusInfo.  
        :rtype: str
        """
        return self._chargeback_status

    @chargeback_status.setter
    def chargeback_status(self, chargeback_status):
        """Sets the chargeback_status of this DepositStatusInfo.


        :param chargeback_status: The chargeback_status of this DepositStatusInfo.  
        :type: str
        """

        self._chargeback_status = chargeback_status

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
        if issubclass(DepositStatusInfo, dict):
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
        if not isinstance(other, DepositStatusInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
