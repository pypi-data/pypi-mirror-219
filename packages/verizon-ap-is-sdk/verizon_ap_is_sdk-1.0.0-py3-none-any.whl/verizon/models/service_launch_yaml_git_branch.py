# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class ServiceLaunchYamlGitBranch(object):

    """Implementation of the 'ServiceLaunchYamlGitBranch' model.

    TODO: type model description here.

    Attributes:
        branch_name (string): TODO: type description here.
        values_yaml_paths (list of string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "branch_name": 'branchName',
        "values_yaml_paths": 'valuesYamlPaths'
    }

    _optionals = [
        'branch_name',
        'values_yaml_paths',
    ]

    def __init__(self,
                 branch_name=APIHelper.SKIP,
                 values_yaml_paths=APIHelper.SKIP):
        """Constructor for the ServiceLaunchYamlGitBranch class"""

        # Initialize members of the class
        if branch_name is not APIHelper.SKIP:
            self.branch_name = branch_name 
        if values_yaml_paths is not APIHelper.SKIP:
            self.values_yaml_paths = values_yaml_paths 

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

        branch_name = dictionary.get("branchName") if dictionary.get("branchName") else APIHelper.SKIP
        values_yaml_paths = dictionary.get("valuesYamlPaths") if dictionary.get("valuesYamlPaths") else APIHelper.SKIP
        # Return an object of this model
        return cls(branch_name,
                   values_yaml_paths)
