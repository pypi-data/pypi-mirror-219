# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.gpu import GPU


class ComputeResourcesType(object):

    """Implementation of the 'ComputeResourcesType' model.

    Compute resources of a service profile.

    Attributes:
        gpu (GPU): GPU resources of a service profile.
        min_ramgb (int): Minimum RAM required in Gigabytes.
        min_storage_gb (int): Minimum storage requirement in Gigabytes.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "gpu": 'GPU',
        "min_ramgb": 'minRAMGB',
        "min_storage_gb": 'minStorageGB'
    }

    _optionals = [
        'gpu',
        'min_ramgb',
        'min_storage_gb',
    ]

    def __init__(self,
                 gpu=APIHelper.SKIP,
                 min_ramgb=APIHelper.SKIP,
                 min_storage_gb=APIHelper.SKIP):
        """Constructor for the ComputeResourcesType class"""

        # Initialize members of the class
        if gpu is not APIHelper.SKIP:
            self.gpu = gpu 
        if min_ramgb is not APIHelper.SKIP:
            self.min_ramgb = min_ramgb 
        if min_storage_gb is not APIHelper.SKIP:
            self.min_storage_gb = min_storage_gb 

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

        gpu = GPU.from_dictionary(dictionary.get('GPU')) if 'GPU' in dictionary.keys() else APIHelper.SKIP
        min_ramgb = dictionary.get("minRAMGB") if dictionary.get("minRAMGB") else APIHelper.SKIP
        min_storage_gb = dictionary.get("minStorageGB") if dictionary.get("minStorageGB") else APIHelper.SKIP
        # Return an object of this model
        return cls(gpu,
                   min_ramgb,
                   min_storage_gb)
