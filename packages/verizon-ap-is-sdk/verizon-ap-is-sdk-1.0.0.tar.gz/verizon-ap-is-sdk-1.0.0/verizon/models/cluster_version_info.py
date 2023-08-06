# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper


class ClusterVersionInfo(object):

    """Implementation of the 'ClusterVersionInfo' model.

    TODO: type model description here.

    Attributes:
        cluster_id (string): TODO: type description here.
        kube_version (string): TODO: type description here.
        organization_id (string): TODO: type description here.
        partner_id (string): TODO: type description here.
        created_at (string): TODO: type description here.
        modified_at (string): TODO: type description here.
        id (string): TODO: type description here.
        behind_latest_by (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "cluster_id": 'cluster_id',
        "kube_version": 'kube_version',
        "organization_id": 'organization_id',
        "partner_id": 'partner_id',
        "created_at": 'created_at',
        "modified_at": 'modified_at',
        "id": 'id',
        "behind_latest_by": 'behind_latest_by'
    }

    _optionals = [
        'cluster_id',
        'kube_version',
        'organization_id',
        'partner_id',
        'created_at',
        'modified_at',
        'id',
        'behind_latest_by',
    ]

    def __init__(self,
                 cluster_id=APIHelper.SKIP,
                 kube_version=APIHelper.SKIP,
                 organization_id=APIHelper.SKIP,
                 partner_id=APIHelper.SKIP,
                 created_at=APIHelper.SKIP,
                 modified_at=APIHelper.SKIP,
                 id=APIHelper.SKIP,
                 behind_latest_by=APIHelper.SKIP):
        """Constructor for the ClusterVersionInfo class"""

        # Initialize members of the class
        if cluster_id is not APIHelper.SKIP:
            self.cluster_id = cluster_id 
        if kube_version is not APIHelper.SKIP:
            self.kube_version = kube_version 
        if organization_id is not APIHelper.SKIP:
            self.organization_id = organization_id 
        if partner_id is not APIHelper.SKIP:
            self.partner_id = partner_id 
        if created_at is not APIHelper.SKIP:
            self.created_at = created_at 
        if modified_at is not APIHelper.SKIP:
            self.modified_at = modified_at 
        if id is not APIHelper.SKIP:
            self.id = id 
        if behind_latest_by is not APIHelper.SKIP:
            self.behind_latest_by = behind_latest_by 

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

        cluster_id = dictionary.get("cluster_id") if dictionary.get("cluster_id") else APIHelper.SKIP
        kube_version = dictionary.get("kube_version") if dictionary.get("kube_version") else APIHelper.SKIP
        organization_id = dictionary.get("organization_id") if dictionary.get("organization_id") else APIHelper.SKIP
        partner_id = dictionary.get("partner_id") if dictionary.get("partner_id") else APIHelper.SKIP
        created_at = dictionary.get("created_at") if dictionary.get("created_at") else APIHelper.SKIP
        modified_at = dictionary.get("modified_at") if dictionary.get("modified_at") else APIHelper.SKIP
        id = dictionary.get("id") if dictionary.get("id") else APIHelper.SKIP
        behind_latest_by = dictionary.get("behind_latest_by") if dictionary.get("behind_latest_by") else APIHelper.SKIP
        # Return an object of this model
        return cls(cluster_id,
                   kube_version,
                   organization_id,
                   partner_id,
                   created_at,
                   modified_at,
                   id,
                   behind_latest_by)
