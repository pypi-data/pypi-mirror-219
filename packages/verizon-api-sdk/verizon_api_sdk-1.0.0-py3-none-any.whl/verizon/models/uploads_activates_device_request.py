# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.device_list import DeviceList


class UploadsActivatesDeviceRequest(object):

    """Implementation of the 'UploadsActivatesDeviceRequest' model.

    The request body identifies the devices to upload.

    Attributes:
        account_name (string): The name of a billing account. An account name
            is usually numeric, and must include any leading zeros.
        email_address (string): The email address that the report should be
            sent to when the upload is complete.
        device_sku (string): The stock keeping unit that identifies the type
            of devices in the upload and activation.
        upload_type (string): The format of the device identifiers in the
            upload and activation.
        service_plan (string): The service plan code that you want to assign
            to all specified devices.
        carrier_ip_pool_name (string): The pool from which your device IP
            addresses is derived.
        mdn_zip_code (string): The Zip code of the location where the line of
            service is primarily used, or a Zip code that you have been told
            to use with these devices.
        devices (list of DeviceList): The devices to upload, specified by
            device IDs in a format matching uploadType.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_name": 'accountName',
        "email_address": 'emailAddress',
        "device_sku": 'deviceSku',
        "upload_type": 'uploadType',
        "service_plan": 'servicePlan',
        "mdn_zip_code": 'mdnZipCode',
        "devices": 'devices',
        "carrier_ip_pool_name": 'carrierIpPoolName'
    }

    _optionals = [
        'carrier_ip_pool_name',
    ]

    def __init__(self,
                 account_name=None,
                 email_address=None,
                 device_sku=None,
                 upload_type=None,
                 service_plan=None,
                 mdn_zip_code=None,
                 devices=None,
                 carrier_ip_pool_name=APIHelper.SKIP):
        """Constructor for the UploadsActivatesDeviceRequest class"""

        # Initialize members of the class
        self.account_name = account_name 
        self.email_address = email_address 
        self.device_sku = device_sku 
        self.upload_type = upload_type 
        self.service_plan = service_plan 
        if carrier_ip_pool_name is not APIHelper.SKIP:
            self.carrier_ip_pool_name = carrier_ip_pool_name 
        self.mdn_zip_code = mdn_zip_code 
        self.devices = devices 

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

        account_name = dictionary.get("accountName") if dictionary.get("accountName") else None
        email_address = dictionary.get("emailAddress") if dictionary.get("emailAddress") else None
        device_sku = dictionary.get("deviceSku") if dictionary.get("deviceSku") else None
        upload_type = dictionary.get("uploadType") if dictionary.get("uploadType") else None
        service_plan = dictionary.get("servicePlan") if dictionary.get("servicePlan") else None
        mdn_zip_code = dictionary.get("mdnZipCode") if dictionary.get("mdnZipCode") else None
        devices = None
        if dictionary.get('devices') is not None:
            devices = [DeviceList.from_dictionary(x) for x in dictionary.get('devices')]
        carrier_ip_pool_name = dictionary.get("carrierIpPoolName") if dictionary.get("carrierIpPoolName") else APIHelper.SKIP
        # Return an object of this model
        return cls(account_name,
                   email_address,
                   device_sku,
                   upload_type,
                   service_plan,
                   mdn_zip_code,
                   devices,
                   carrier_ip_pool_name)
