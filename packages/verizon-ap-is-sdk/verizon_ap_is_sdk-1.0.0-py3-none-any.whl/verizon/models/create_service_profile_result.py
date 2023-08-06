# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class CreateServiceProfileResult(object):

    """Implementation of the 'CreateServiceProfileResult' model.

    A successful request returns a serviceProfileId that you can use in
    subsequent requests.

    Attributes:
        service_profile_id (string): Unique identifier for a service profile.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "service_profile_id": 'serviceProfileId'
    }

    _optionals = [
        'service_profile_id',
    ]

    def __init__(self,
                 service_profile_id=APIHelper.SKIP):
        """Constructor for the CreateServiceProfileResult class"""

        # Initialize members of the class
        if service_profile_id is not APIHelper.SKIP:
            self.service_profile_id = service_profile_id 

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

        service_profile_id = dictionary.get("serviceProfileId") if dictionary.get("serviceProfileId") else APIHelper.SKIP
        # Return an object of this model
        return cls(service_profile_id)
