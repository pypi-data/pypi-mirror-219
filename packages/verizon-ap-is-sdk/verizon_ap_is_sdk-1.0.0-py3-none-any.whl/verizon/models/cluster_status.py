# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""
from verizon.api_helper import APIHelper
from verizon.models.cluster_status_extra import ClusterStatusExtra
from verizon.models.condition_item import ConditionItem
from verizon.models.node_status_item import NodeStatusItem
from verizon.models.status_project_item import StatusProjectItem


class ClusterStatus(object):

    """Implementation of the 'ClusterStatus' model.

    TODO: type model description here.

    Attributes:
        conditions (list of ConditionItem): TODO: type description here.
        token (string): TODO: type description here.
        published_blueprint (string): TODO: type description here.
        nodes (list of NodeStatusItem): TODO: type description here.
        system_task_count (int): TODO: type description here.
        custom_task_count (int): TODO: type description here.
        auxiliary_task_count (int): TODO: type description here.
        projects (list of StatusProjectItem): TODO: type description here.
        extra (ClusterStatusExtra): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "conditions": 'conditions',
        "token": 'token',
        "published_blueprint": 'publishedBlueprint',
        "nodes": 'nodes',
        "system_task_count": 'systemTaskCount',
        "custom_task_count": 'customTaskCount',
        "auxiliary_task_count": 'auxiliaryTaskCount',
        "projects": 'projects',
        "extra": 'extra'
    }

    _optionals = [
        'conditions',
        'token',
        'published_blueprint',
        'nodes',
        'system_task_count',
        'custom_task_count',
        'auxiliary_task_count',
        'projects',
        'extra',
    ]

    def __init__(self,
                 conditions=APIHelper.SKIP,
                 token=APIHelper.SKIP,
                 published_blueprint=APIHelper.SKIP,
                 nodes=APIHelper.SKIP,
                 system_task_count=APIHelper.SKIP,
                 custom_task_count=APIHelper.SKIP,
                 auxiliary_task_count=APIHelper.SKIP,
                 projects=APIHelper.SKIP,
                 extra=APIHelper.SKIP):
        """Constructor for the ClusterStatus class"""

        # Initialize members of the class
        if conditions is not APIHelper.SKIP:
            self.conditions = conditions 
        if token is not APIHelper.SKIP:
            self.token = token 
        if published_blueprint is not APIHelper.SKIP:
            self.published_blueprint = published_blueprint 
        if nodes is not APIHelper.SKIP:
            self.nodes = nodes 
        if system_task_count is not APIHelper.SKIP:
            self.system_task_count = system_task_count 
        if custom_task_count is not APIHelper.SKIP:
            self.custom_task_count = custom_task_count 
        if auxiliary_task_count is not APIHelper.SKIP:
            self.auxiliary_task_count = auxiliary_task_count 
        if projects is not APIHelper.SKIP:
            self.projects = projects 
        if extra is not APIHelper.SKIP:
            self.extra = extra 

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

        conditions = None
        if dictionary.get('conditions') is not None:
            conditions = [ConditionItem.from_dictionary(x) for x in dictionary.get('conditions')]
        else:
            conditions = APIHelper.SKIP
        token = dictionary.get("token") if dictionary.get("token") else APIHelper.SKIP
        published_blueprint = dictionary.get("publishedBlueprint") if dictionary.get("publishedBlueprint") else APIHelper.SKIP
        nodes = None
        if dictionary.get('nodes') is not None:
            nodes = [NodeStatusItem.from_dictionary(x) for x in dictionary.get('nodes')]
        else:
            nodes = APIHelper.SKIP
        system_task_count = dictionary.get("systemTaskCount") if dictionary.get("systemTaskCount") else APIHelper.SKIP
        custom_task_count = dictionary.get("customTaskCount") if dictionary.get("customTaskCount") else APIHelper.SKIP
        auxiliary_task_count = dictionary.get("auxiliaryTaskCount") if dictionary.get("auxiliaryTaskCount") else APIHelper.SKIP
        projects = None
        if dictionary.get('projects') is not None:
            projects = [StatusProjectItem.from_dictionary(x) for x in dictionary.get('projects')]
        else:
            projects = APIHelper.SKIP
        extra = ClusterStatusExtra.from_dictionary(dictionary.get('extra')) if 'extra' in dictionary.keys() else APIHelper.SKIP
        # Return an object of this model
        return cls(conditions,
                   token,
                   published_blueprint,
                   nodes,
                   system_task_count,
                   custom_task_count,
                   auxiliary_task_count,
                   projects,
                   extra)
