# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class DeviceUpgradeHistory(object):

    """Implementation of the 'DeviceUpgradeHistory' model.

    Firmware upgrade information.

    Attributes:
        device_id (string): Device IMEI.
        id (string): The unique identifier for the upgrade.
        account_name (string): The name (number) of the billing account that
            the device belongs to.
        firmware_from (string): The firmware version that was on the device
            before the upgrade.
        firmware_to (string): The name of the firmware version that was on the
            device after the upgrade.
        start_date (string): The date of the upgrade.
        upgrade_start_time (string): The date and time that the upgrade
            actually started for this device.
        status (string): The status of the upgrade for this device.
        reason (string): More information about the status.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "device_id": 'deviceId',
        "id": 'id',
        "account_name": 'accountName',
        "firmware_from": 'firmwareFrom',
        "firmware_to": 'firmwareTo',
        "start_date": 'startDate',
        "upgrade_start_time": 'upgradeStartTime',
        "status": 'status',
        "reason": 'reason'
    }

    _optionals = [
        'device_id',
        'id',
        'account_name',
        'firmware_from',
        'firmware_to',
        'start_date',
        'upgrade_start_time',
        'status',
        'reason',
    ]

    def __init__(self,
                 device_id=APIHelper.SKIP,
                 id=APIHelper.SKIP,
                 account_name=APIHelper.SKIP,
                 firmware_from=APIHelper.SKIP,
                 firmware_to=APIHelper.SKIP,
                 start_date=APIHelper.SKIP,
                 upgrade_start_time=APIHelper.SKIP,
                 status=APIHelper.SKIP,
                 reason=APIHelper.SKIP):
        """Constructor for the DeviceUpgradeHistory class"""

        # Initialize members of the class
        if device_id is not APIHelper.SKIP:
            self.device_id = device_id 
        if id is not APIHelper.SKIP:
            self.id = id 
        if account_name is not APIHelper.SKIP:
            self.account_name = account_name 
        if firmware_from is not APIHelper.SKIP:
            self.firmware_from = firmware_from 
        if firmware_to is not APIHelper.SKIP:
            self.firmware_to = firmware_to 
        if start_date is not APIHelper.SKIP:
            self.start_date = start_date 
        if upgrade_start_time is not APIHelper.SKIP:
            self.upgrade_start_time = upgrade_start_time 
        if status is not APIHelper.SKIP:
            self.status = status 
        if reason is not APIHelper.SKIP:
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

        device_id = dictionary.get("deviceId") if dictionary.get("deviceId") else APIHelper.SKIP
        id = dictionary.get("id") if dictionary.get("id") else APIHelper.SKIP
        account_name = dictionary.get("accountName") if dictionary.get("accountName") else APIHelper.SKIP
        firmware_from = dictionary.get("firmwareFrom") if dictionary.get("firmwareFrom") else APIHelper.SKIP
        firmware_to = dictionary.get("firmwareTo") if dictionary.get("firmwareTo") else APIHelper.SKIP
        start_date = dictionary.get("startDate") if dictionary.get("startDate") else APIHelper.SKIP
        upgrade_start_time = dictionary.get("upgradeStartTime") if dictionary.get("upgradeStartTime") else APIHelper.SKIP
        status = dictionary.get("status") if dictionary.get("status") else APIHelper.SKIP
        reason = dictionary.get("reason") if dictionary.get("reason") else APIHelper.SKIP
        # Return an object of this model
        return cls(device_id,
                   id,
                   account_name,
                   firmware_from,
                   firmware_to,
                   start_date,
                   upgrade_start_time,
                   status,
                   reason)
