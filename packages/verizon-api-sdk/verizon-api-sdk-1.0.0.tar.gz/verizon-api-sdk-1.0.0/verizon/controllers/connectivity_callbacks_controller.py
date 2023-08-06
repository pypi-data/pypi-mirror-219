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
from verizon.models.connectivity_management_callback import ConnectivityManagementCallback
from verizon.models.callback_action_result import CallbackActionResult
from verizon.exceptions.connectivity_management_result_exception import ConnectivityManagementResultException


class ConnectivityCallbacksController(BaseController):

    """A Controller to access Endpoints in the verizon API."""
    def __init__(self, config):
        super(ConnectivityCallbacksController, self).__init__(config)

    def list_registered_callbacks(self,
                                  aname):
        """Does a GET request to /v1/callbacks/{aname}.

        Returns the name and endpoint URL of the callback listening services
        registered for a given account.

        Args:
            aname (string): Account name.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. A list of
                callback listeners.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server(Server.M2M)
            .path('/v1/callbacks/{aname}')
            .http_method(HttpMethodEnum.GET)
            .template_param(Parameter()
                            .key('aname')
                            .value(aname)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .deserialize_into(ConnectivityManagementCallback.from_dictionary)
            .is_api_response(True)
            .local_error('400', 'Error response.', ConnectivityManagementResultException)
        ).execute()

    def register_callback(self,
                          aname,
                          body):
        """Does a POST request to /v1/callbacks/{aname}.

        You are responsible for creating and running a listening process on
        your server at that URL.

        Args:
            aname (string): Account name.
            body (RegisterCallbackRequest): Request to register a callback.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. A success
                response for registering a callback.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server(Server.M2M)
            .path('/v1/callbacks/{aname}')
            .http_method(HttpMethodEnum.POST)
            .template_param(Parameter()
                            .key('aname')
                            .value(aname)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .deserialize_into(CallbackActionResult.from_dictionary)
            .is_api_response(True)
            .local_error('400', 'Error response.', ConnectivityManagementResultException)
        ).execute()

    def deregister_callback(self,
                            aname,
                            sname):
        """Does a DELETE request to /v1/callbacks/{aname}/name/{sname}.

        Stops ThingSpace from sending callback messages for the specified
        account and service.

        Args:
            aname (string): Account name.
            sname (string): Service name.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Response
                for a request to deregister a callback.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server(Server.M2M)
            .path('/v1/callbacks/{aname}/name/{sname}')
            .http_method(HttpMethodEnum.DELETE)
            .template_param(Parameter()
                            .key('aname')
                            .value(aname)
                            .should_encode(True))
            .template_param(Parameter()
                            .key('sname')
                            .value(sname)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .deserialize_into(CallbackActionResult.from_dictionary)
            .is_api_response(True)
            .local_error('400', 'Error response.', ConnectivityManagementResultException)
        ).execute()
