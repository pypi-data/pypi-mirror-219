# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.models.device_list import DeviceList


class NotificationReportRequest(object):

    """Implementation of the 'NotificationReportRequest' model.

    TODO: type model description here.

    Attributes:
        account_name (string): TODO: type description here.
        request_type (string): TODO: type description here.
        devices (list of DeviceList): TODO: type description here.
        monitor_expiration_time (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_name": 'accountName',
        "request_type": 'requestType',
        "devices": 'devices',
        "monitor_expiration_time": 'monitorExpirationTime'
    }

    def __init__(self,
                 account_name=None,
                 request_type=None,
                 devices=None,
                 monitor_expiration_time=None):
        """Constructor for the NotificationReportRequest class"""

        # Initialize members of the class
        self.account_name = account_name 
        self.request_type = request_type 
        self.devices = devices 
        self.monitor_expiration_time = monitor_expiration_time 

    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary

        account_name = dictionary.get("accountName") if dictionary.get("accountName") else None
        request_type = dictionary.get("requestType") if dictionary.get("requestType") else None
        devices = None
        if dictionary.get('devices') is not None:
            devices = [DeviceList.from_dictionary(x) for x in dictionary.get('devices')]
        monitor_expiration_time = dictionary.get("monitorExpirationTime") if dictionary.get("monitorExpirationTime") else None
        # Return an object of this model
        return cls(account_name,
                   request_type,
                   devices,
                   monitor_expiration_time)
