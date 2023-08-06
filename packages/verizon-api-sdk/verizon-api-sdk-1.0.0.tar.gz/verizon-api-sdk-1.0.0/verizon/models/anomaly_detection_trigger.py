# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class AnomalyDetectionTrigger(object):

    """Implementation of the 'AnomalyDetectionTrigger' model.

    Trigger for anomaly detection.

    Attributes:
        trigger_id (string): Trigger ID to identify the request in a
            callback.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "trigger_id": 'triggerId'
    }

    _optionals = [
        'trigger_id',
    ]

    def __init__(self,
                 trigger_id=APIHelper.SKIP):
        """Constructor for the AnomalyDetectionTrigger class"""

        # Initialize members of the class
        if trigger_id is not APIHelper.SKIP:
            self.trigger_id = trigger_id 

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

        trigger_id = dictionary.get("triggerId") if dictionary.get("triggerId") else APIHelper.SKIP
        # Return an object of this model
        return cls(trigger_id)
