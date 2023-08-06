# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.download_time_window import DownloadTimeWindow


class UploadAndScheduleFileRequest(object):

    """Implementation of the 'UploadAndScheduleFileRequest' model.

    TODO: type model description here.

    Attributes:
        campaign_name (string): The campaign name.
        file_name (string): The name of the file you are upgrading to.
        file_version (string): The version of the file you are upgrading to.
        distribution_type (string): Valid values
        start_date (string): Campaign start date.
        end_date (string): Campaign end date.
        download_after_date (string): Specifies the starting date the client
            should download the package. If null, client downloads as soon as
            possible.
        download_time_window_list (list of DownloadTimeWindow): List of
            allowed download time windows.
        install_after_date (string): The date after which you install the
            package. If null, install as soon as possible.
        install_time_window_list (list of DownloadTimeWindow): List of allowed
            install time windows.
        device_list (list of string): Device IMEI list.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "campaign_name": 'campaignName',
        "file_name": 'fileName',
        "file_version": 'fileVersion',
        "distribution_type": 'distributionType',
        "start_date": 'startDate',
        "end_date": 'endDate',
        "download_after_date": 'downloadAfterDate',
        "download_time_window_list": 'downloadTimeWindowList',
        "install_after_date": 'installAfterDate',
        "install_time_window_list": 'installTimeWindowList',
        "device_list": 'deviceList'
    }

    _optionals = [
        'campaign_name',
        'file_name',
        'file_version',
        'distribution_type',
        'start_date',
        'end_date',
        'download_after_date',
        'download_time_window_list',
        'install_after_date',
        'install_time_window_list',
        'device_list',
    ]

    def __init__(self,
                 campaign_name=APIHelper.SKIP,
                 file_name=APIHelper.SKIP,
                 file_version=APIHelper.SKIP,
                 distribution_type=APIHelper.SKIP,
                 start_date=APIHelper.SKIP,
                 end_date=APIHelper.SKIP,
                 download_after_date=APIHelper.SKIP,
                 download_time_window_list=APIHelper.SKIP,
                 install_after_date=APIHelper.SKIP,
                 install_time_window_list=APIHelper.SKIP,
                 device_list=APIHelper.SKIP):
        """Constructor for the UploadAndScheduleFileRequest class"""

        # Initialize members of the class
        if campaign_name is not APIHelper.SKIP:
            self.campaign_name = campaign_name 
        if file_name is not APIHelper.SKIP:
            self.file_name = file_name 
        if file_version is not APIHelper.SKIP:
            self.file_version = file_version 
        if distribution_type is not APIHelper.SKIP:
            self.distribution_type = distribution_type 
        if start_date is not APIHelper.SKIP:
            self.start_date = start_date 
        if end_date is not APIHelper.SKIP:
            self.end_date = end_date 
        if download_after_date is not APIHelper.SKIP:
            self.download_after_date = download_after_date 
        if download_time_window_list is not APIHelper.SKIP:
            self.download_time_window_list = download_time_window_list 
        if install_after_date is not APIHelper.SKIP:
            self.install_after_date = install_after_date 
        if install_time_window_list is not APIHelper.SKIP:
            self.install_time_window_list = install_time_window_list 
        if device_list is not APIHelper.SKIP:
            self.device_list = device_list 

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

        campaign_name = dictionary.get("campaignName") if dictionary.get("campaignName") else APIHelper.SKIP
        file_name = dictionary.get("fileName") if dictionary.get("fileName") else APIHelper.SKIP
        file_version = dictionary.get("fileVersion") if dictionary.get("fileVersion") else APIHelper.SKIP
        distribution_type = dictionary.get("distributionType") if dictionary.get("distributionType") else APIHelper.SKIP
        start_date = dictionary.get("startDate") if dictionary.get("startDate") else APIHelper.SKIP
        end_date = dictionary.get("endDate") if dictionary.get("endDate") else APIHelper.SKIP
        download_after_date = dictionary.get("downloadAfterDate") if dictionary.get("downloadAfterDate") else APIHelper.SKIP
        download_time_window_list = None
        if dictionary.get('downloadTimeWindowList') is not None:
            download_time_window_list = [DownloadTimeWindow.from_dictionary(x) for x in dictionary.get('downloadTimeWindowList')]
        else:
            download_time_window_list = APIHelper.SKIP
        install_after_date = dictionary.get("installAfterDate") if dictionary.get("installAfterDate") else APIHelper.SKIP
        install_time_window_list = None
        if dictionary.get('installTimeWindowList') is not None:
            install_time_window_list = [DownloadTimeWindow.from_dictionary(x) for x in dictionary.get('installTimeWindowList')]
        else:
            install_time_window_list = APIHelper.SKIP
        device_list = dictionary.get("deviceList") if dictionary.get("deviceList") else APIHelper.SKIP
        # Return an object of this model
        return cls(campaign_name,
                   file_name,
                   file_version,
                   distribution_type,
                   start_date,
                   end_date,
                   download_after_date,
                   download_time_window_list,
                   install_after_date,
                   install_time_window_list,
                   device_list)
