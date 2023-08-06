# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class AnomalyTriggerRequest(object):

    """Implementation of the 'AnomalyTriggerRequest' model.

    The details of the UsageAnomaly trigger.

    Attributes:
        account_names (string): The Verizon billing accounts associated with
            the anomaly triggers for this trigger to be active for devices in
            those accounts. An account name is usually numeric, and must
            include any leading zeros.
        include_abnormal (bool): Whether or not to include anomalies
            classified as 'abnormal'.<br />true<br />false<br />Classification
            is set as part of ThingSpace Intelligence anomaly detection
            settings.
        include_very_abnormal (bool): Whether or not to include anomalies
            classified as 'very abnormal'.<br />true<br />false<br
            />Classification is set as part of ThingSpace Intelligence anomaly
            detection settings.
        include_under_expected_usage (bool): Whether or not to include
            anomalies that are directionally under the expected usage.<br
            />true<br />false.
        include_over_expected_usage (bool): Whether or not to include
            anomalies that are directionally over the expected usage. <br
            />true<br />false.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_names": 'accountNames',
        "include_abnormal": 'includeAbnormal',
        "include_very_abnormal": 'includeVeryAbnormal',
        "include_under_expected_usage": 'includeUnderExpectedUsage',
        "include_over_expected_usage": 'includeOverExpectedUsage'
    }

    _optionals = [
        'account_names',
        'include_abnormal',
        'include_very_abnormal',
        'include_under_expected_usage',
        'include_over_expected_usage',
    ]

    def __init__(self,
                 account_names=APIHelper.SKIP,
                 include_abnormal=APIHelper.SKIP,
                 include_very_abnormal=APIHelper.SKIP,
                 include_under_expected_usage=APIHelper.SKIP,
                 include_over_expected_usage=APIHelper.SKIP):
        """Constructor for the AnomalyTriggerRequest class"""

        # Initialize members of the class
        if account_names is not APIHelper.SKIP:
            self.account_names = account_names 
        if include_abnormal is not APIHelper.SKIP:
            self.include_abnormal = include_abnormal 
        if include_very_abnormal is not APIHelper.SKIP:
            self.include_very_abnormal = include_very_abnormal 
        if include_under_expected_usage is not APIHelper.SKIP:
            self.include_under_expected_usage = include_under_expected_usage 
        if include_over_expected_usage is not APIHelper.SKIP:
            self.include_over_expected_usage = include_over_expected_usage 

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

        account_names = dictionary.get("accountNames") if dictionary.get("accountNames") else APIHelper.SKIP
        include_abnormal = dictionary.get("includeAbnormal") if "includeAbnormal" in dictionary.keys() else APIHelper.SKIP
        include_very_abnormal = dictionary.get("includeVeryAbnormal") if "includeVeryAbnormal" in dictionary.keys() else APIHelper.SKIP
        include_under_expected_usage = dictionary.get("includeUnderExpectedUsage") if "includeUnderExpectedUsage" in dictionary.keys() else APIHelper.SKIP
        include_over_expected_usage = dictionary.get("includeOverExpectedUsage") if "includeOverExpectedUsage" in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(account_names,
                   include_abnormal,
                   include_very_abnormal,
                   include_under_expected_usage,
                   include_over_expected_usage)
