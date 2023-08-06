# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class IPPool(object):

    """Implementation of the 'IPPool' model.

    IP pool that is available to the account.

    Attributes:
        pool_name (string): The name of the IP pool.
        pool_type (string): The type of IP pool, such as “Static IP” or
            “Dynamic IP.”
        is_default_pool (bool): True if this is the default IP pool for the
            account.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "pool_name": 'poolName',
        "pool_type": 'poolType',
        "is_default_pool": 'isDefaultPool'
    }

    _optionals = [
        'pool_name',
        'pool_type',
        'is_default_pool',
    ]

    def __init__(self,
                 pool_name=APIHelper.SKIP,
                 pool_type=APIHelper.SKIP,
                 is_default_pool=APIHelper.SKIP):
        """Constructor for the IPPool class"""

        # Initialize members of the class
        if pool_name is not APIHelper.SKIP:
            self.pool_name = pool_name 
        if pool_type is not APIHelper.SKIP:
            self.pool_type = pool_type 
        if is_default_pool is not APIHelper.SKIP:
            self.is_default_pool = is_default_pool 

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

        pool_name = dictionary.get("poolName") if dictionary.get("poolName") else APIHelper.SKIP
        pool_type = dictionary.get("poolType") if dictionary.get("poolType") else APIHelper.SKIP
        is_default_pool = dictionary.get("isDefaultPool") if "isDefaultPool" in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(pool_name,
                   pool_type,
                   is_default_pool)
