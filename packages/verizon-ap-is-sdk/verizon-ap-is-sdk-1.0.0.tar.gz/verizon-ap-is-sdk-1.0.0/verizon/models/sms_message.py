# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.device_id import DeviceId


class SMSMessage(object):

    """Implementation of the 'SMSMessage' model.

    SMS messages sent by all M2M devices associated with a billing account.

    Attributes:
        device_ids (list of DeviceId): One or more IDs of the device that sent
            the message.
        message (string): The contents of the SMS message.
        timestamp (string): The date and time that the message was received by
            the Verizon ThingSpace Platform.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "device_ids": 'deviceIds',
        "message": 'message',
        "timestamp": 'timestamp'
    }

    _optionals = [
        'device_ids',
        'message',
        'timestamp',
    ]

    def __init__(self,
                 device_ids=APIHelper.SKIP,
                 message=APIHelper.SKIP,
                 timestamp=APIHelper.SKIP):
        """Constructor for the SMSMessage class"""

        # Initialize members of the class
        if device_ids is not APIHelper.SKIP:
            self.device_ids = device_ids 
        if message is not APIHelper.SKIP:
            self.message = message 
        if timestamp is not APIHelper.SKIP:
            self.timestamp = timestamp 

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

        device_ids = None
        if dictionary.get('deviceIds') is not None:
            device_ids = [DeviceId.from_dictionary(x) for x in dictionary.get('deviceIds')]
        else:
            device_ids = APIHelper.SKIP
        message = dictionary.get("message") if dictionary.get("message") else APIHelper.SKIP
        timestamp = dictionary.get("timestamp") if dictionary.get("timestamp") else APIHelper.SKIP
        # Return an object of this model
        return cls(device_ids,
                   message,
                   timestamp)
