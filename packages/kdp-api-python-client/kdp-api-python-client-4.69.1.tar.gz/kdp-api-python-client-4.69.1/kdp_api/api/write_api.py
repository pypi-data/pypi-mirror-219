"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces  # noqa: E501

    The version of the OpenAPI document: 4.69.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from kdp_api.api_client import ApiClient, Endpoint as _Endpoint
from kdp_api.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from kdp_api.model.api_error import ApiError
from kdp_api.model.batch_write_request import BatchWriteRequest
from kdp_api.model.json_record import JsonRecord
from kdp_api.model.write_batch_response import WriteBatchResponse


class WriteApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.post_v2_write_id_endpoint = _Endpoint(
            settings={
                'response_type': (WriteBatchResponse,),
                'auth': [
                    'Bearer'
                ],
                'endpoint_path': '/v2/write/{datasetId}',
                'operation_id': 'post_v2_write_id',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'dataset_id',
                    'batch_write_request',
                    'is_async',
                ],
                'required': [
                    'dataset_id',
                    'batch_write_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'dataset_id':
                        (str,),
                    'batch_write_request':
                        (BatchWriteRequest,),
                    'is_async':
                        (bool,),
                },
                'attribute_map': {
                    'dataset_id': 'datasetId',
                    'is_async': 'isAsync',
                },
                'location_map': {
                    'dataset_id': 'path',
                    'batch_write_request': 'body',
                    'is_async': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    '*/*',
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.post_write_id_endpoint = _Endpoint(
            settings={
                'response_type': (WriteBatchResponse,),
                'auth': [
                    'Bearer'
                ],
                'endpoint_path': '/write/{datasetId}',
                'operation_id': 'post_write_id',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'dataset_id',
                    'json_record',
                    'is_async',
                ],
                'required': [
                    'dataset_id',
                    'json_record',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'dataset_id':
                        (str,),
                    'json_record':
                        ([JsonRecord],),
                    'is_async':
                        (bool,),
                },
                'attribute_map': {
                    'dataset_id': 'datasetId',
                    'is_async': 'isAsync',
                },
                'location_map': {
                    'dataset_id': 'path',
                    'json_record': 'body',
                    'is_async': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    '*/*',
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )

    def post_v2_write_id(
        self,
        dataset_id,
        batch_write_request,
        **kwargs
    ):
        """Write records (v2)  # noqa: E501

        Writes a batch of records to random partitions with the option of configuring security label parser and returns the list of partitions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_v2_write_id(dataset_id, batch_write_request, async_req=True)
        >>> result = thread.get()

        Args:
            dataset_id (str):
            batch_write_request (BatchWriteRequest):

        Keyword Args:
            is_async (bool): [optional] if omitted the server will use the default value of False
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            WriteBatchResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['dataset_id'] = \
            dataset_id
        kwargs['batch_write_request'] = \
            batch_write_request
        return self.post_v2_write_id_endpoint.call_with_http_info(**kwargs)

    def post_write_id(
        self,
        dataset_id,
        json_record,
        **kwargs
    ):
        """Write records  # noqa: E501

        Writes a batch of records to random partitions and returns the list of partitions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_write_id(dataset_id, json_record, async_req=True)
        >>> result = thread.get()

        Args:
            dataset_id (str):
            json_record ([JsonRecord]):

        Keyword Args:
            is_async (bool): [optional] if omitted the server will use the default value of False
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            WriteBatchResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['dataset_id'] = \
            dataset_id
        kwargs['json_record'] = \
            json_record
        return self.post_write_id_endpoint.call_with_http_info(**kwargs)

