# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
import dateutil.parser

from verizon.api_helper import APIHelper


class SoftwarePackage(object):

    """Implementation of the 'SoftwarePackage' model.

    Software package information.

    Attributes:
        software_name (string): Software name.
        launch_date (date): Software launch date.
        release_note (string): Software release note reserved for future use.
        model (string): Software applicable device model.
        make (string): Software applicable device make.
        distribution_type (string): LWM2M, OMD-DM or HTTP.
        device_platform_id (string): The platform (Android, iOS, etc.) that
            the software can be applied to.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "software_name": 'softwareName',
        "launch_date": 'launchDate',
        "model": 'model',
        "make": 'make',
        "distribution_type": 'distributionType',
        "device_platform_id": 'devicePlatformId',
        "release_note": 'releaseNote'
    }

    _optionals = [
        'release_note',
    ]

    def __init__(self,
                 software_name=None,
                 launch_date=None,
                 model=None,
                 make=None,
                 distribution_type=None,
                 device_platform_id=None,
                 release_note=APIHelper.SKIP):
        """Constructor for the SoftwarePackage class"""

        # Initialize members of the class
        self.software_name = software_name 
        self.launch_date = launch_date 
        if release_note is not APIHelper.SKIP:
            self.release_note = release_note 
        self.model = model 
        self.make = make 
        self.distribution_type = distribution_type 
        self.device_platform_id = device_platform_id 

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

        software_name = dictionary.get("softwareName") if dictionary.get("softwareName") else None
        launch_date = dateutil.parser.parse(dictionary.get('launchDate')).date() if dictionary.get('launchDate') else None
        model = dictionary.get("model") if dictionary.get("model") else None
        make = dictionary.get("make") if dictionary.get("make") else None
        distribution_type = dictionary.get("distributionType") if dictionary.get("distributionType") else None
        device_platform_id = dictionary.get("devicePlatformId") if dictionary.get("devicePlatformId") else None
        release_note = dictionary.get("releaseNote") if dictionary.get("releaseNote") else APIHelper.SKIP
        # Return an object of this model
        return cls(software_name,
                   launch_date,
                   model,
                   make,
                   distribution_type,
                   device_platform_id,
                   release_note)
