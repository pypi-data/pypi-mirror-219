# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class ConsentRequest(object):

    """Implementation of the 'ConsentRequest' model.

    TODO: type model description here.

    Attributes:
        account_name (string): Account identifier in "##########-#####".
        all_device (bool): Exclude all devices or not.
        mtype (string): The change to make: append or replace.
        exclusion (list of string): Device ID list.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_name": 'accountName',
        "all_device": 'allDevice',
        "mtype": 'type',
        "exclusion": 'exclusion'
    }

    _optionals = [
        'account_name',
        'all_device',
        'mtype',
        'exclusion',
    ]

    def __init__(self,
                 account_name=APIHelper.SKIP,
                 all_device=APIHelper.SKIP,
                 mtype=APIHelper.SKIP,
                 exclusion=APIHelper.SKIP):
        """Constructor for the ConsentRequest class"""

        # Initialize members of the class
        if account_name is not APIHelper.SKIP:
            self.account_name = account_name 
        if all_device is not APIHelper.SKIP:
            self.all_device = all_device 
        if mtype is not APIHelper.SKIP:
            self.mtype = mtype 
        if exclusion is not APIHelper.SKIP:
            self.exclusion = exclusion 

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

        account_name = dictionary.get("accountName") if dictionary.get("accountName") else APIHelper.SKIP
        all_device = dictionary.get("allDevice") if "allDevice" in dictionary.keys() else APIHelper.SKIP
        mtype = dictionary.get("type") if dictionary.get("type") else APIHelper.SKIP
        exclusion = dictionary.get("exclusion") if dictionary.get("exclusion") else APIHelper.SKIP
        # Return an object of this model
        return cls(account_name,
                   all_device,
                   mtype,
                   exclusion)
