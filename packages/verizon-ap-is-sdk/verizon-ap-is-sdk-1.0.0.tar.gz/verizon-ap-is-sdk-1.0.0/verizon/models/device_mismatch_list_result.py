# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.mismatched_device import MismatchedDevice


class DeviceMismatchListResult(object):

    """Implementation of the 'DeviceMismatchListResult' model.

    Response to list of all 4G devices with an ICCID (SIM) that was not
    activated with the expected IMEI (hardware) during a specified time
    frame.

    Attributes:
        devices (list of MismatchedDevice): A list of specific devices that
            you want to check, specified by ICCID or MDN.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "devices": 'devices'
    }

    _optionals = [
        'devices',
    ]

    def __init__(self,
                 devices=APIHelper.SKIP):
        """Constructor for the DeviceMismatchListResult class"""

        # Initialize members of the class
        if devices is not APIHelper.SKIP:
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

        devices = None
        if dictionary.get('devices') is not None:
            devices = [MismatchedDevice.from_dictionary(x) for x in dictionary.get('devices')]
        else:
            devices = APIHelper.SKIP
        # Return an object of this model
        return cls(devices)
