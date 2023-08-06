# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
import dateutil.parser

from verizon.api_helper import APIHelper


class DeviceSoftwareUpgrade(object):

    """Implementation of the 'DeviceSoftwareUpgrade' model.

    Array of software upgrade objects with the specified status.

    Attributes:
        device_id (string): Device identifier.
        id (string): Upgrade identifier.
        account_name (string): Account identifier.
        software_name (string): Software name.
        start_date (date): Software upgrade start date.
        status (string): Software upgrade status.
        reason (string): Software upgrade result reason.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "device_id": 'deviceId',
        "id": 'id',
        "account_name": 'accountName',
        "start_date": 'startDate',
        "status": 'status',
        "reason": 'reason',
        "software_name": 'softwareName'
    }

    _optionals = [
        'software_name',
    ]

    def __init__(self,
                 device_id=None,
                 id=None,
                 account_name=None,
                 start_date=None,
                 status=None,
                 reason=None,
                 software_name=APIHelper.SKIP):
        """Constructor for the DeviceSoftwareUpgrade class"""

        # Initialize members of the class
        self.device_id = device_id 
        self.id = id 
        self.account_name = account_name 
        if software_name is not APIHelper.SKIP:
            self.software_name = software_name 
        self.start_date = start_date 
        self.status = status 
        self.reason = reason 

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

        device_id = dictionary.get("deviceId") if dictionary.get("deviceId") else None
        id = dictionary.get("id") if dictionary.get("id") else None
        account_name = dictionary.get("accountName") if dictionary.get("accountName") else None
        start_date = dateutil.parser.parse(dictionary.get('startDate')).date() if dictionary.get('startDate') else None
        status = dictionary.get("status") if dictionary.get("status") else None
        reason = dictionary.get("reason") if dictionary.get("reason") else None
        software_name = dictionary.get("softwareName") if dictionary.get("softwareName") else APIHelper.SKIP
        # Return an object of this model
        return cls(device_id,
                   id,
                   account_name,
                   start_date,
                   status,
                   reason,
                   software_name)
