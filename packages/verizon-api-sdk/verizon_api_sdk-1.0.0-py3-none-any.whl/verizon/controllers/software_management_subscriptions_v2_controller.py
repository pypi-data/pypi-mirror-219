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
from verizon.models.fota_v2_subscription import FotaV2Subscription
from verizon.exceptions.fota_v2_result_exception import FotaV2ResultException


class SoftwareManagementSubscriptionsV2Controller(BaseController):

    """A Controller to access Endpoints in the verizon API."""
    def __init__(self, config):
        super(SoftwareManagementSubscriptionsV2Controller, self).__init__(config)

    def get_account_subscription_status(self,
                                        account):
        """Does a GET request to /subscriptions/{account}.

        This endpoint retrieves a FOTA subscription by account.

        Args:
            account (string): Account identifier.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. FOTA
                Subscription.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server(Server.SOFTWARE_MANAGEMENT_V2)
            .path('/subscriptions/{account}')
            .http_method(HttpMethodEnum.GET)
            .template_param(Parameter()
                            .key('account')
                            .value(account)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .deserialize_into(FotaV2Subscription.from_dictionary)
            .is_api_response(True)
            .local_error('400', 'Unexpected error.', FotaV2ResultException)
        ).execute()
