# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class MECPlatformsAdditionalSupportInfoData(object):

    """Implementation of the 'MECPlatformsAdditionalSupportInfoData' model.

    Data about additional service support information for the MEC platform.

    Attributes:
        additional_info (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_info": 'additionalInfo'
    }

    _optionals = [
        'additional_info',
    ]

    def __init__(self,
                 additional_info=APIHelper.SKIP):
        """Constructor for the MECPlatformsAdditionalSupportInfoData class"""

        # Initialize members of the class
        if additional_info is not APIHelper.SKIP:
            self.additional_info = additional_info 

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

        additional_info = dictionary.get("additionalInfo") if dictionary.get("additionalInfo") else APIHelper.SKIP
        # Return an object of this model
        return cls(additional_info)
