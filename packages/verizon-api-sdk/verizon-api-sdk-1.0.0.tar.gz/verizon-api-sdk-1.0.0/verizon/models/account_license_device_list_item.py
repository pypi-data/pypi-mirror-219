# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class AccountLicenseDeviceListItem(object):

    """Implementation of the 'AccountLicenseDeviceListItem' model.

    The list of devices that have licenses assigned, including the date and
    time of when each license was assigned.

    Attributes:
        device_id (string): Device IMEI.
        assignment_time (datetime): Timestamp of when a license was assigned
            to the device.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "device_id": 'deviceId',
        "assignment_time": 'assignmentTime'
    }

    _optionals = [
        'device_id',
        'assignment_time',
    ]

    def __init__(self,
                 device_id=APIHelper.SKIP,
                 assignment_time=APIHelper.SKIP):
        """Constructor for the AccountLicenseDeviceListItem class"""

        # Initialize members of the class
        if device_id is not APIHelper.SKIP:
            self.device_id = device_id 
        if assignment_time is not APIHelper.SKIP:
            self.assignment_time = APIHelper.RFC3339DateTime(assignment_time) if assignment_time else None 

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

        device_id = dictionary.get("deviceId") if dictionary.get("deviceId") else APIHelper.SKIP
        assignment_time = APIHelper.RFC3339DateTime.from_value(dictionary.get("assignmentTime")).datetime if dictionary.get("assignmentTime") else APIHelper.SKIP
        # Return an object of this model
        return cls(device_id,
                   assignment_time)
