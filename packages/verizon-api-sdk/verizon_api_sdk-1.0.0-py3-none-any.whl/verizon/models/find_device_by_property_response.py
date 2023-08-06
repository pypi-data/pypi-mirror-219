# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class FindDeviceByPropertyResponse(object):

    """Implementation of the 'FindDeviceByPropertyResponse' model.

    Change Configuration resource definition.

    Attributes:
        billingaccountid (string): Billing account ID of the resource.
        createdon (string): The date the resource was created.
        eventretention (string): TODO: type description here.
        iccid (string): Cellular SIM card identifier.
        id (string): ThingSpace unique ID for the device that was added.
        imei (string): 4G hardware device identifier.
        kind (string): Identifies the resource kind.
        lastupdated (string): The date the resource was last updated.
        providerid (string): The device’s service provider.
        refid (string): The value of the refidtype identifier.
        refidtype (string): The device identifier type used to refer to this
            device.
        state (string): Service state of the device.
        version (string): Version of the underlying schema resource.
        versionid (string): The version of the resource.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "billingaccountid": 'billingaccountid',
        "createdon": 'createdon',
        "eventretention": 'eventretention',
        "iccid": 'iccid',
        "id": 'id',
        "imei": 'imei',
        "kind": 'kind',
        "lastupdated": 'lastupdated',
        "providerid": 'providerid',
        "refid": 'refid',
        "refidtype": 'refidtype',
        "state": 'state',
        "version": 'version',
        "versionid": 'versionid'
    }

    _optionals = [
        'billingaccountid',
        'createdon',
        'eventretention',
        'iccid',
        'id',
        'imei',
        'kind',
        'lastupdated',
        'providerid',
        'refid',
        'refidtype',
        'state',
        'version',
        'versionid',
    ]

    def __init__(self,
                 billingaccountid=APIHelper.SKIP,
                 createdon=APIHelper.SKIP,
                 eventretention=APIHelper.SKIP,
                 iccid=APIHelper.SKIP,
                 id=APIHelper.SKIP,
                 imei=APIHelper.SKIP,
                 kind=APIHelper.SKIP,
                 lastupdated=APIHelper.SKIP,
                 providerid=APIHelper.SKIP,
                 refid=APIHelper.SKIP,
                 refidtype=APIHelper.SKIP,
                 state=APIHelper.SKIP,
                 version=APIHelper.SKIP,
                 versionid=APIHelper.SKIP):
        """Constructor for the FindDeviceByPropertyResponse class"""

        # Initialize members of the class
        if billingaccountid is not APIHelper.SKIP:
            self.billingaccountid = billingaccountid 
        if createdon is not APIHelper.SKIP:
            self.createdon = createdon 
        if eventretention is not APIHelper.SKIP:
            self.eventretention = eventretention 
        if iccid is not APIHelper.SKIP:
            self.iccid = iccid 
        if id is not APIHelper.SKIP:
            self.id = id 
        if imei is not APIHelper.SKIP:
            self.imei = imei 
        if kind is not APIHelper.SKIP:
            self.kind = kind 
        if lastupdated is not APIHelper.SKIP:
            self.lastupdated = lastupdated 
        if providerid is not APIHelper.SKIP:
            self.providerid = providerid 
        if refid is not APIHelper.SKIP:
            self.refid = refid 
        if refidtype is not APIHelper.SKIP:
            self.refidtype = refidtype 
        if state is not APIHelper.SKIP:
            self.state = state 
        if version is not APIHelper.SKIP:
            self.version = version 
        if versionid is not APIHelper.SKIP:
            self.versionid = versionid 

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

        billingaccountid = dictionary.get("billingaccountid") if dictionary.get("billingaccountid") else APIHelper.SKIP
        createdon = dictionary.get("createdon") if dictionary.get("createdon") else APIHelper.SKIP
        eventretention = dictionary.get("eventretention") if dictionary.get("eventretention") else APIHelper.SKIP
        iccid = dictionary.get("iccid") if dictionary.get("iccid") else APIHelper.SKIP
        id = dictionary.get("id") if dictionary.get("id") else APIHelper.SKIP
        imei = dictionary.get("imei") if dictionary.get("imei") else APIHelper.SKIP
        kind = dictionary.get("kind") if dictionary.get("kind") else APIHelper.SKIP
        lastupdated = dictionary.get("lastupdated") if dictionary.get("lastupdated") else APIHelper.SKIP
        providerid = dictionary.get("providerid") if dictionary.get("providerid") else APIHelper.SKIP
        refid = dictionary.get("refid") if dictionary.get("refid") else APIHelper.SKIP
        refidtype = dictionary.get("refidtype") if dictionary.get("refidtype") else APIHelper.SKIP
        state = dictionary.get("state") if dictionary.get("state") else APIHelper.SKIP
        version = dictionary.get("version") if dictionary.get("version") else APIHelper.SKIP
        versionid = dictionary.get("versionid") if dictionary.get("versionid") else APIHelper.SKIP
        # Return an object of this model
        return cls(billingaccountid,
                   createdon,
                   eventretention,
                   iccid,
                   id,
                   imei,
                   kind,
                   lastupdated,
                   providerid,
                   refid,
                   refidtype,
                   state,
                   version,
                   versionid)
