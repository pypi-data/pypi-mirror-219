# coding: utf-8

"""
    NetSuite REST API
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
import json

from netsuite.api_clients.api_client import ApiClient



class RestletApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def execute_restlet(self, path_params, body_params, method='POST', **kwargs):
        all_params = ['script', 'deploy']  # noqa: E501
        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method customer_get" % key
                )
            params[key] = val
        del params['kwargs']

        if path_params is not None:
            path_params = path_params
        else:
            path_params = {}

        if 'script' in params:
            path_params['script'] = params['script']
        else:
            raise ValueError("Script cannot be Null")

        if 'deploy' in params:
            path_params['deploy'] = params['deploy']
        else:
            path_params['deploy'] = '1'

        # Authentication setting
        auth_settings = ['oAuth2ClientCredentials']
        response = self.api_client.call_api('',
                                            method,
                                            query_params=path_params,
                                            _preload_content=False,
                                            _return_http_data_only=True,
                                            auth_settings=auth_settings,
                                            body=body_params)
        if hasattr(response, 'data'):
            if isinstance(response.data, bytes):
                response = response.data.decode('utf8')
                try:
                    response = json.loads(response)
                    if 'results' in response:
                        if type(response.get("results")) is list:
                            return response.get("results")
                        else:
                            items = [response.get("results")]
                            return items
                except ValueError:
                    pass
                except TypeError:
                    pass
        return response
