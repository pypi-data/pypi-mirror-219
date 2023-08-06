# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""

from verizon.api_helper import APIHelper
import verizon.exceptions.api_exception


class IntelligenceResultException(verizon.exceptions.api_exception.APIException):
    def __init__(self, reason, response):
        """Constructor for the IntelligenceResultException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            response (HttpResponse): The HttpResponse of the API call.

        """
        super(IntelligenceResultException, self).__init__(reason, response)
        dictionary = APIHelper.json_deserialize(self.response.text)
        if isinstance(dictionary, dict):
            self.unbox(dictionary)

    def unbox(self, dictionary):
        """Populates the properties of this object by extracting them from a dictionary.

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        """
        self.error_code = dictionary.get("errorCode") if dictionary.get("errorCode") else None
        self.error_message = dictionary.get("errorMessage") if dictionary.get("errorMessage") else None
