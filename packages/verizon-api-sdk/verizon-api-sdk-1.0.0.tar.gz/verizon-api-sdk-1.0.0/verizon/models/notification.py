# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.sms_number import SMSNumber


class Notification(object):

    """Implementation of the 'Notification' model.

    The notification details of the trigger.

    Attributes:
        notification_type (string): The type of notification, i.e.
            'DailySummary'.
        callback (bool): Whether or not the notification should be sent via
            callback.<br />true<br />false.
        email_notification (bool): Whether or not the notification should be
            sent via e-mail.<br />true<br />false.
        notification_group_name (string): Name for the notification group.
        notification_frequency_factor (int): Frequency factor for
            notification.
        notification_frequency_interval (string): Frequency interval for
            notification.
        external_email_recipients (string): E-mail address(es) where the
            notification should be delivered.
        sms_notification (bool): SMS notification.
        sms_numbers (list of SMSNumber): List of SMS numbers.
        reminder (bool): TODO: type description here.
        severity (string): Severity level associated with the notification.
            Examples would be:<br />Major<br />Minor<br />Critical<br
            />NotApplicable.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "notification_type": 'notificationType',
        "callback": 'callback',
        "email_notification": 'emailNotification',
        "notification_group_name": 'notificationGroupName',
        "notification_frequency_factor": 'notificationFrequencyFactor',
        "notification_frequency_interval": 'notificationFrequencyInterval',
        "external_email_recipients": 'externalEmailRecipients',
        "sms_notification": 'smsNotification',
        "sms_numbers": 'smsNumbers',
        "reminder": 'reminder',
        "severity": 'severity'
    }

    _optionals = [
        'notification_type',
        'callback',
        'email_notification',
        'notification_group_name',
        'notification_frequency_factor',
        'notification_frequency_interval',
        'external_email_recipients',
        'sms_notification',
        'sms_numbers',
        'reminder',
        'severity',
    ]

    def __init__(self,
                 notification_type=APIHelper.SKIP,
                 callback=APIHelper.SKIP,
                 email_notification=APIHelper.SKIP,
                 notification_group_name=APIHelper.SKIP,
                 notification_frequency_factor=APIHelper.SKIP,
                 notification_frequency_interval=APIHelper.SKIP,
                 external_email_recipients=APIHelper.SKIP,
                 sms_notification=APIHelper.SKIP,
                 sms_numbers=APIHelper.SKIP,
                 reminder=APIHelper.SKIP,
                 severity=APIHelper.SKIP):
        """Constructor for the Notification class"""

        # Initialize members of the class
        if notification_type is not APIHelper.SKIP:
            self.notification_type = notification_type 
        if callback is not APIHelper.SKIP:
            self.callback = callback 
        if email_notification is not APIHelper.SKIP:
            self.email_notification = email_notification 
        if notification_group_name is not APIHelper.SKIP:
            self.notification_group_name = notification_group_name 
        if notification_frequency_factor is not APIHelper.SKIP:
            self.notification_frequency_factor = notification_frequency_factor 
        if notification_frequency_interval is not APIHelper.SKIP:
            self.notification_frequency_interval = notification_frequency_interval 
        if external_email_recipients is not APIHelper.SKIP:
            self.external_email_recipients = external_email_recipients 
        if sms_notification is not APIHelper.SKIP:
            self.sms_notification = sms_notification 
        if sms_numbers is not APIHelper.SKIP:
            self.sms_numbers = sms_numbers 
        if reminder is not APIHelper.SKIP:
            self.reminder = reminder 
        if severity is not APIHelper.SKIP:
            self.severity = severity 

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

        notification_type = dictionary.get("notificationType") if dictionary.get("notificationType") else APIHelper.SKIP
        callback = dictionary.get("callback") if "callback" in dictionary.keys() else APIHelper.SKIP
        email_notification = dictionary.get("emailNotification") if "emailNotification" in dictionary.keys() else APIHelper.SKIP
        notification_group_name = dictionary.get("notificationGroupName") if dictionary.get("notificationGroupName") else APIHelper.SKIP
        notification_frequency_factor = dictionary.get("notificationFrequencyFactor") if dictionary.get("notificationFrequencyFactor") else APIHelper.SKIP
        notification_frequency_interval = dictionary.get("notificationFrequencyInterval") if dictionary.get("notificationFrequencyInterval") else APIHelper.SKIP
        external_email_recipients = dictionary.get("externalEmailRecipients") if dictionary.get("externalEmailRecipients") else APIHelper.SKIP
        sms_notification = dictionary.get("smsNotification") if "smsNotification" in dictionary.keys() else APIHelper.SKIP
        sms_numbers = None
        if dictionary.get('smsNumbers') is not None:
            sms_numbers = [SMSNumber.from_dictionary(x) for x in dictionary.get('smsNumbers')]
        else:
            sms_numbers = APIHelper.SKIP
        reminder = dictionary.get("reminder") if "reminder" in dictionary.keys() else APIHelper.SKIP
        severity = dictionary.get("severity") if dictionary.get("severity") else APIHelper.SKIP
        # Return an object of this model
        return cls(notification_type,
                   callback,
                   email_notification,
                   notification_group_name,
                   notification_frequency_factor,
                   notification_frequency_interval,
                   external_email_recipients,
                   sms_notification,
                   sms_numbers,
                   reminder,
                   severity)
