# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.331
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from lusid.api_client import ApiClient
from lusid.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)
from lusid.models.allocation_service_run_response import AllocationServiceRunResponse
from lusid.models.book_transactions_response import BookTransactionsResponse
from lusid.models.lusid_problem_details import LusidProblemDetails
from lusid.models.lusid_validation_problem_details import LusidValidationProblemDetails
from lusid.models.resource_id import ResourceId


class OrderManagementApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def book_transactions(self, resource_id, **kwargs):  # noqa: E501
        """[EXPERIMENTAL] BookTransactions: Books transactions using specific allocations as a source.  # noqa: E501

        Takes a collection of allocation IDs, and maps fields from those allocations and related orders onto new transactions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.book_transactions(resource_id, async_req=True)
        >>> result = thread.get()

        :param resource_id: The allocations to create transactions for (required)
        :type resource_id: list[ResourceId]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: BookTransactionsResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.book_transactions_with_http_info(resource_id, **kwargs)  # noqa: E501

    def book_transactions_with_http_info(self, resource_id, **kwargs):  # noqa: E501
        """[EXPERIMENTAL] BookTransactions: Books transactions using specific allocations as a source.  # noqa: E501

        Takes a collection of allocation IDs, and maps fields from those allocations and related orders onto new transactions.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.book_transactions_with_http_info(resource_id, async_req=True)
        >>> result = thread.get()

        :param resource_id: The allocations to create transactions for (required)
        :type resource_id: list[ResourceId]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (BookTransactionsResponse, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'resource_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method book_transactions" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'resource_id' is set
        if self.api_client.client_side_validation and ('resource_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['resource_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `resource_id` when calling `book_transactions`")  # noqa: E501

        if self.api_client.client_side_validation and ('resource_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['resource_id']) > 5000):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `resource_id` when calling `book_transactions`, number of items must be less than or equal to `5000`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        if 'resource_id' in local_var_params:
            body_params = local_var_params['resource_id']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '1.0.331'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "BookTransactionsResponse",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/ordermanagement/booktransactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def run_allocation_service(self, resource_id, **kwargs):  # noqa: E501
        """[EXPERIMENTAL] RunAllocationService: Runs the Allocation Service  # noqa: E501

        This will allocate executions for a given list of placements back to their originating orders.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_allocation_service(resource_id, async_req=True)
        >>> result = thread.get()

        :param resource_id: The List of Placement IDs for which you wish to allocate executions. (required)
        :type resource_id: list[ResourceId]
        :param allocation_algorithm: A string representation of the allocation algorithm you would like to use to allocate shares from executions e.g. \"PR-FIFO\".  This defaults to \"PR-FIFO\".
        :type allocation_algorithm: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AllocationServiceRunResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.run_allocation_service_with_http_info(resource_id, **kwargs)  # noqa: E501

    def run_allocation_service_with_http_info(self, resource_id, **kwargs):  # noqa: E501
        """[EXPERIMENTAL] RunAllocationService: Runs the Allocation Service  # noqa: E501

        This will allocate executions for a given list of placements back to their originating orders.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_allocation_service_with_http_info(resource_id, async_req=True)
        >>> result = thread.get()

        :param resource_id: The List of Placement IDs for which you wish to allocate executions. (required)
        :type resource_id: list[ResourceId]
        :param allocation_algorithm: A string representation of the allocation algorithm you would like to use to allocate shares from executions e.g. \"PR-FIFO\".  This defaults to \"PR-FIFO\".
        :type allocation_algorithm: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (AllocationServiceRunResponse, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'resource_id',
            'allocation_algorithm'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method run_allocation_service" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'resource_id' is set
        if self.api_client.client_side_validation and ('resource_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['resource_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `resource_id` when calling `run_allocation_service`")  # noqa: E501

        if self.api_client.client_side_validation and ('resource_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['resource_id']) > 100):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `resource_id` when calling `run_allocation_service`, number of items must be less than or equal to `100`")  # noqa: E501
        if self.api_client.client_side_validation and ('allocation_algorithm' in local_var_params and  # noqa: E501
                                                        len(local_var_params['allocation_algorithm']) > 64):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `allocation_algorithm` when calling `run_allocation_service`, length must be less than or equal to `64`")  # noqa: E501
        if self.api_client.client_side_validation and ('allocation_algorithm' in local_var_params and  # noqa: E501
                                                        len(local_var_params['allocation_algorithm']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `allocation_algorithm` when calling `run_allocation_service`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'allocation_algorithm' in local_var_params and not re.search(r'^[a-zA-Z0-9\-_]+$', local_var_params['allocation_algorithm']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `allocation_algorithm` when calling `run_allocation_service`, must conform to the pattern `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'allocation_algorithm' in local_var_params and local_var_params['allocation_algorithm'] is not None:  # noqa: E501
            query_params.append(('allocationAlgorithm', local_var_params['allocation_algorithm']))  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        if 'resource_id' in local_var_params:
            body_params = local_var_params['resource_id']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '1.0.331'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "AllocationServiceRunResponse",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/ordermanagement/allocate', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
