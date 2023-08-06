# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class CategoryList(object):

    """Implementation of the 'CategoryList' model.

    Response to get category list.

    Attributes:
        categories (list of string): Can be any name just to define it under a
            category.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "categories": 'categories'
    }

    _optionals = [
        'categories',
    ]

    def __init__(self,
                 categories=APIHelper.SKIP):
        """Constructor for the CategoryList class"""

        # Initialize members of the class
        if categories is not APIHelper.SKIP:
            self.categories = categories 

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

        categories = dictionary.get("categories") if dictionary.get("categories") else APIHelper.SKIP
        # Return an object of this model
        return cls(categories)
