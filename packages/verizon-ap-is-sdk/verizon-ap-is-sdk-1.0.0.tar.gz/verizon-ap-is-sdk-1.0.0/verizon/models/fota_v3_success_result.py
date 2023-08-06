# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""


class FotaV3SuccessResult(object):

    """Implementation of the 'FotaV3SuccessResult' model.

    Cancelation status.

    Attributes:
        success (bool): True or false.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "success": 'success'
    }

    def __init__(self,
                 success=None):
        """Constructor for the FotaV3SuccessResult class"""

        # Initialize members of the class
        self.success = success 

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

        success = dictionary.get("success") if "success" in dictionary.keys() else None
        # Return an object of this model
        return cls(success)
