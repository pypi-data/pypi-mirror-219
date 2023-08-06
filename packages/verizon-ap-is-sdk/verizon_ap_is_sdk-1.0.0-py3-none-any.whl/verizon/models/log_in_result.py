# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class LogInResult(object):

    """Implementation of the 'LogInResult' model.

    Response to initiate a Connectivity Management session and returns a
    VZ-M2M session token that is required in subsequent API requests.

    Attributes:
        session_token (string): The identifier for the session that was
            created by the request. Store the sessionToken for use in the
            header of all other API requests.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "session_token": 'sessionToken'
    }

    _optionals = [
        'session_token',
    ]

    def __init__(self,
                 session_token=APIHelper.SKIP):
        """Constructor for the LogInResult class"""

        # Initialize members of the class
        if session_token is not APIHelper.SKIP:
            self.session_token = session_token 

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

        session_token = dictionary.get("sessionToken") if dictionary.get("sessionToken") else APIHelper.SKIP
        # Return an object of this model
        return cls(session_token)
