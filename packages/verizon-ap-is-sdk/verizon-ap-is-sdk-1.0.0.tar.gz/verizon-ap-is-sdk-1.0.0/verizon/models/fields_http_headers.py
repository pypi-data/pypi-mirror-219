# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class FieldsHttpHeaders(object):

    """Implementation of the 'FieldsHttpHeaders' model.

    TODO: type model description here.

    Attributes:
        authorization (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "authorization": 'Authorization'
    }

    _optionals = [
        'authorization',
    ]

    def __init__(self,
                 authorization=APIHelper.SKIP):
        """Constructor for the FieldsHttpHeaders class"""

        # Initialize members of the class
        if authorization is not APIHelper.SKIP:
            self.authorization = authorization 

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

        authorization = dictionary.get("Authorization") if dictionary.get("Authorization") else APIHelper.SKIP
        # Return an object of this model
        return cls(authorization)
