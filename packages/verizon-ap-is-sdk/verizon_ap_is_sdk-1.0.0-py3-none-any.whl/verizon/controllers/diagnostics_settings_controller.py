# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""

from verizon.api_helper import APIHelper
from verizon.configuration import Server
from verizon.http.api_response import ApiResponse
from verizon.controllers.base_controller import BaseController
from apimatic_core.request_builder import RequestBuilder
from apimatic_core.response_handler import ResponseHandler
from apimatic_core.types.parameter import Parameter
from verizon.http.http_method_enum import HttpMethodEnum
from apimatic_core.authentication.multiple.single_auth import Single
from apimatic_core.authentication.multiple.and_auth_group import And
from apimatic_core.authentication.multiple.or_auth_group import Or
from verizon.models.diagnostic_observation_setting import DiagnosticObservationSetting
from verizon.exceptions.device_diagnostics_result_exception import DeviceDiagnosticsResultException


class DiagnosticsSettingsController(BaseController):

    """A Controller to access Endpoints in the verizon API."""
    def __init__(self, config):
        super(DiagnosticsSettingsController, self).__init__(config)

    def list_diagnostics_settings(self,
                                  account_name,
                                  devices):
        """Does a GET request to /devices/settings.

        This endpoint retrieves diagnostics settings synchronously.

        Args:
            account_name (string): Account identifier.
            devices (string): Devices list format:
                [{"id":"{imei1}","kind":"imei"},{"id":"{imei2}","kind":"imei"}]
                .

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers.
                Diagnostic settings.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server(Server.DEVICE_DIAGNOSTICS)
            .path('/devices/settings')
            .http_method(HttpMethodEnum.GET)
            .query_param(Parameter()
                         .key('accountName')
                         .value(account_name))
            .query_param(Parameter()
                         .key('devices')
                         .value(devices))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .deserialize_into(DiagnosticObservationSetting.from_dictionary)
            .is_api_response(True)
            .local_error('default', 'Error response.', DeviceDiagnosticsResultException)
        ).execute()
