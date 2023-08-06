# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class SensitivityParameters(object):

    """Implementation of the 'SensitivityParameters' model.

    Details for sensitivity parameters.

    Attributes:
        abnormal_max_value (float): The maximum value of the threshold in the
            units being measured.
        enable_abnormal (bool): If abnormal values are being monitored.<br
            />true - Monitor for abnormal values<br />false - Do not monitor
            for abnormal values.
        enable_very_abnormal (bool): If very abnormal values are being
            monitored.<br />true - Monitor for very abnormal values<br />false
            - Do not monitor for very abnormal values.
        very_abnormal_max_value (float): The maximum value of the threshold in
            the units being measured.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "abnormal_max_value": 'abnormalMaxValue',
        "enable_abnormal": 'enableAbnormal',
        "enable_very_abnormal": 'enableVeryAbnormal',
        "very_abnormal_max_value": 'veryAbnormalMaxValue'
    }

    _optionals = [
        'abnormal_max_value',
        'enable_abnormal',
        'enable_very_abnormal',
        'very_abnormal_max_value',
    ]

    def __init__(self,
                 abnormal_max_value=APIHelper.SKIP,
                 enable_abnormal=APIHelper.SKIP,
                 enable_very_abnormal=APIHelper.SKIP,
                 very_abnormal_max_value=APIHelper.SKIP):
        """Constructor for the SensitivityParameters class"""

        # Initialize members of the class
        if abnormal_max_value is not APIHelper.SKIP:
            self.abnormal_max_value = abnormal_max_value 
        if enable_abnormal is not APIHelper.SKIP:
            self.enable_abnormal = enable_abnormal 
        if enable_very_abnormal is not APIHelper.SKIP:
            self.enable_very_abnormal = enable_very_abnormal 
        if very_abnormal_max_value is not APIHelper.SKIP:
            self.very_abnormal_max_value = very_abnormal_max_value 

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

        abnormal_max_value = dictionary.get("abnormalMaxValue") if dictionary.get("abnormalMaxValue") else APIHelper.SKIP
        enable_abnormal = dictionary.get("enableAbnormal") if "enableAbnormal" in dictionary.keys() else APIHelper.SKIP
        enable_very_abnormal = dictionary.get("enableVeryAbnormal") if "enableVeryAbnormal" in dictionary.keys() else APIHelper.SKIP
        very_abnormal_max_value = dictionary.get("veryAbnormalMaxValue") if dictionary.get("veryAbnormalMaxValue") else APIHelper.SKIP
        # Return an object of this model
        return cls(abnormal_max_value,
                   enable_abnormal,
                   enable_very_abnormal,
                   very_abnormal_max_value)
