# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class EdgeDiscoveryResultData(object):

    """Implementation of the 'EdgeDiscoveryResultData' model.

    For cases where user input exceeds the boundary values an additional
    'data' key will be returned with a relevant description.

    Attributes:
        additional_message (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_message": 'additionalMessage'
    }

    _optionals = [
        'additional_message',
    ]

    def __init__(self,
                 additional_message=APIHelper.SKIP):
        """Constructor for the EdgeDiscoveryResultData class"""

        # Initialize members of the class
        if additional_message is not APIHelper.SKIP:
            self.additional_message = additional_message 

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

        additional_message = dictionary.get("additionalMessage") if dictionary.get("additionalMessage") else APIHelper.SKIP
        # Return an object of this model
        return cls(additional_message)
