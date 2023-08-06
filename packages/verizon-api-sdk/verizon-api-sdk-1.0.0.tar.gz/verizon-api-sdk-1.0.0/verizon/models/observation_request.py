# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.device import Device
from verizon.models.numerical_data import NumericalData
from verizon.models.observation_request_attribute import ObservationRequestAttribute


class ObservationRequest(object):

    """Implementation of the 'ObservationRequest' model.

    Used to define callbacks including the device identity, the attribute
    names, corresponding attribute values and the date/timestamp of when the
    observation was made.

    Attributes:
        account_name (string): Account identifier in "##########-#####".
        devices (list of Device): List of devices.
        attributes (list of ObservationRequestAttribute): Attributes are
            streaming RF parameters that you want to observe.
        frequency (NumericalData): Describes value and unit of time.
        duration (NumericalData): Describes value and unit of time.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_name": 'accountName',
        "devices": 'devices',
        "attributes": 'attributes',
        "frequency": 'frequency',
        "duration": 'duration'
    }

    _optionals = [
        'frequency',
        'duration',
    ]

    def __init__(self,
                 account_name=None,
                 devices=None,
                 attributes=None,
                 frequency=APIHelper.SKIP,
                 duration=APIHelper.SKIP):
        """Constructor for the ObservationRequest class"""

        # Initialize members of the class
        self.account_name = account_name 
        self.devices = devices 
        self.attributes = attributes 
        if frequency is not APIHelper.SKIP:
            self.frequency = frequency 
        if duration is not APIHelper.SKIP:
            self.duration = duration 

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
        devices = None
        if dictionary.get('devices') is not None:
            devices = [Device.from_dictionary(x) for x in dictionary.get('devices')]
        attributes = None
        if dictionary.get('attributes') is not None:
            attributes = [ObservationRequestAttribute.from_dictionary(x) for x in dictionary.get('attributes')]
        frequency = NumericalData.from_dictionary(dictionary.get('frequency')) if 'frequency' in dictionary.keys() else APIHelper.SKIP
        duration = NumericalData.from_dictionary(dictionary.get('duration')) if 'duration' in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(account_name,
                   devices,
                   attributes,
                   frequency,
                   duration)
