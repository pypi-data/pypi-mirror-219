# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class DependentService(object):

    """Implementation of the 'DependentService' model.

    This service is dependent on other service.

    Attributes:
        name (string): Name of the service needs to be deployed.
        version (string): Version of the service being used.
        status (ServiceStatusEnum): Can have any value as - DRAFT_INPROGRESS,
            DRAFT_COMPLETE, DESIGN_INPROGRESS, DESIGN_FAILED,
            DESIGN_COMPLETED, VALIDATION_INPROGRESS,  VALIDATION_FAILED,
            VALIDATION_COMPLETED, TESTING_INPROGRESS, TESTING_FAILED,
            TESTING_COMPLETED, READY_TO_USE_INPROGRESS, READY_TO_USE_FAILED,
            READY_TO_USE_COMPLETED, READY_TO_PRIVATE_USE_INPROGRESS,
            READY_TO_PRIVATE_USE_FAILED, READY_TO_PRIVATE_USE_COMPLETED, 
            PUBLISH_INPROGRESS,  PUBLISH_FAILED,  PUBLISH_COMPLETED, 
            CERTIFY_INPROGRESS,  CERTIFY_FAILED, CERTIFY_COMPLETED,
            DEPRECATE_INPROGRESS,  DEPRECATE_FAILED, DEPRECATE_COMPLETED,
            MARKDELETE_INPROGRESS, MARKDELETE_FAILED, MARKDELETE_COMPLETED.
        mtype (DependentServicesTypeEnum): List of dependent services type.
        created_by (string): User who created the service. Part of response
            only.
        last_modified_by (string): User who last modified the service. Part of
            response only.
        instances (int): Instances of a service.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "name": 'name',
        "version": 'version',
        "status": 'status',
        "mtype": 'type',
        "created_by": 'createdBy',
        "last_modified_by": 'lastModifiedBy',
        "instances": 'Instances'
    }

    _optionals = [
        'name',
        'version',
        'status',
        'mtype',
        'created_by',
        'last_modified_by',
        'instances',
    ]

    _nullables = [
        'mtype',
    ]

    def __init__(self,
                 name=APIHelper.SKIP,
                 version=APIHelper.SKIP,
                 status=APIHelper.SKIP,
                 mtype=APIHelper.SKIP,
                 created_by=APIHelper.SKIP,
                 last_modified_by=APIHelper.SKIP,
                 instances=APIHelper.SKIP):
        """Constructor for the DependentService class"""

        # Initialize members of the class
        if name is not APIHelper.SKIP:
            self.name = name 
        if version is not APIHelper.SKIP:
            self.version = version 
        if status is not APIHelper.SKIP:
            self.status = status 
        if mtype is not APIHelper.SKIP:
            self.mtype = mtype 
        if created_by is not APIHelper.SKIP:
            self.created_by = created_by 
        if last_modified_by is not APIHelper.SKIP:
            self.last_modified_by = last_modified_by 
        if instances is not APIHelper.SKIP:
            self.instances = instances 

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

        name = dictionary.get("name") if dictionary.get("name") else APIHelper.SKIP
        version = dictionary.get("version") if dictionary.get("version") else APIHelper.SKIP
        status = dictionary.get("status") if dictionary.get("status") else APIHelper.SKIP
        mtype = dictionary.get("type") if "type" in dictionary.keys() else APIHelper.SKIP
        created_by = dictionary.get("createdBy") if dictionary.get("createdBy") else APIHelper.SKIP
        last_modified_by = dictionary.get("lastModifiedBy") if dictionary.get("lastModifiedBy") else APIHelper.SKIP
        instances = dictionary.get("Instances") if dictionary.get("Instances") else APIHelper.SKIP
        # Return an object of this model
        return cls(name,
                   version,
                   status,
                   mtype,
                   created_by,
                   last_modified_by,
                   instances)
