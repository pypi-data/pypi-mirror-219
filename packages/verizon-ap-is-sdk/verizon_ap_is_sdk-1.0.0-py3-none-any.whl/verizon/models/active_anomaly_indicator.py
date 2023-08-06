# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class ActiveAnomalyIndicator(object):

    """Implementation of the 'ActiveAnomalyIndicator' model.

    Whether the anomaly detection is active or not.

    Attributes:
        active (bool): Indicates anomaly detection is active<br />True -
            Anomaly detection is active.<br />False - Anomaly detection is not
            active.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "active": 'active'
    }

    _optionals = [
        'active',
    ]

    def __init__(self,
                 active=APIHelper.SKIP):
        """Constructor for the ActiveAnomalyIndicator class"""

        # Initialize members of the class
        if active is not APIHelper.SKIP:
            self.active = active 

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

        active = dictionary.get("active") if "active" in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(active)
