# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class ServiceLaunchTerraformGitTag(object):

    """Implementation of the 'ServiceLaunchTerraformGitTag' model.

    TODO: type model description here.

    Attributes:
        tag_name (string): TODO: type description here.
        terraform_path (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "tag_name": 'tagName',
        "terraform_path": 'terraformPath'
    }

    _optionals = [
        'tag_name',
        'terraform_path',
    ]

    def __init__(self,
                 tag_name=APIHelper.SKIP,
                 terraform_path=APIHelper.SKIP):
        """Constructor for the ServiceLaunchTerraformGitTag class"""

        # Initialize members of the class
        if tag_name is not APIHelper.SKIP:
            self.tag_name = tag_name 
        if terraform_path is not APIHelper.SKIP:
            self.terraform_path = terraform_path 

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

        tag_name = dictionary.get("tagName") if dictionary.get("tagName") else APIHelper.SKIP
        terraform_path = dictionary.get("terraformPath") if dictionary.get("terraformPath") else APIHelper.SKIP
        # Return an object of this model
        return cls(tag_name,
                   terraform_path)
