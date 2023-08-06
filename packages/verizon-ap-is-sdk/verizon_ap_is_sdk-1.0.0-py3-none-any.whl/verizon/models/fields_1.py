# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.search_device_by_property_fields import SearchDeviceByPropertyFields


class Fields1(object):

    """Implementation of the 'Fields1' model.

    TODO: type model description here.

    Attributes:
        item (SearchDeviceByPropertyFields): List of device sensors and their
            most recently reported values.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "item": 'item'
    }

    _optionals = [
        'item',
    ]

    def __init__(self,
                 item=APIHelper.SKIP):
        """Constructor for the Fields1 class"""

        # Initialize members of the class
        if item is not APIHelper.SKIP:
            self.item = item 

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

        item = SearchDeviceByPropertyFields.from_dictionary(dictionary.get('item')) if 'item' in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(item)
