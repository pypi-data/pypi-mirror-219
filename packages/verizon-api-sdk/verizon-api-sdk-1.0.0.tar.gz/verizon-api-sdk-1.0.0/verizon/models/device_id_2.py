# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class DeviceId2(object):

    """Implementation of the 'DeviceId2' model.

    TODO: type model description here.

    Attributes:
        id (string): TODO: type description here.
        kind (Kind1Enum): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "id": 'id',
        "kind": 'kind'
    }

    _optionals = [
        'id',
        'kind',
    ]

    def __init__(self,
                 id=APIHelper.SKIP,
                 kind=APIHelper.SKIP):
        """Constructor for the DeviceId2 class"""

        # Initialize members of the class
        if id is not APIHelper.SKIP:
            self.id = id 
        if kind is not APIHelper.SKIP:
            self.kind = kind 

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

        id = dictionary.get("id") if dictionary.get("id") else APIHelper.SKIP
        kind = dictionary.get("kind") if dictionary.get("kind") else APIHelper.SKIP
        # Return an object of this model
        return cls(id,
                   kind)
