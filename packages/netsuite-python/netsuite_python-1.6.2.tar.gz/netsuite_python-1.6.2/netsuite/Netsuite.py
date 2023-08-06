import json
import os.path
import pathlib
import jwt
from datetime import datetime, timedelta
from pathlib import Path
import importlib

import importlib.util
import netsuite.settings
import requests
from netsuite.NetsuiteToken import NetsuiteToken
# from netsuite.swagger_client.restlet_client import RestletClient
from netsuite.settings import APISettings
from netsuite.storages import BaseStorage, JSONStorage
from netsuite import api_clients


# client_exists = False
# try:
#     # base_dir = str(netsuite.settings.NETSUITE_CLIENT_DIR)
#     api_client  = importlib.util.find_spec('netsuite_rest_client', str(netsuite.settings.NETSUITE_CLIENT_DIR))
#     if api_client is None:
#         print("Run 'netsuite generate-rest-client' after getting a token")
#     else:
#         netsuite_rest_client = api_client.loader.load_module()
#     # apis = importlib.import_module('netsuite_rest_client.apis')
#     # print(apis)
#
#     # print(my_module.loader.load_module())
#     # from base_dir import *
#     # import netsuite.netsuite_rest_client
#     # from netsuite.netsuite_rest_client import *
#     client_exists = True
# except ModuleNotFoundError or ImportError as err:
#     print(err)
#     print('Rest Client needs to be generated')



class Netsuite:
    app_name: str = None
    storage: BaseStorage = None
    api_settings: APISettings
    query_client = None
    restlet_client = None

    def __init__(self, config: dict = None, config_file: Path = None):
        if config and config_file:
            raise ValueError("You can only load settings from one source")
        if config_file:
            with open(config_file, 'r') as f:
                config = json.load(f)
        if config is None and config_file is None:
            try:
                with open(pathlib.Path(APISettings().defaults.get("CREDENTIALS_PATH")), 'r') as f:
                    config = json.load(f)
            except Exception as e:
                raise Exception("No Configuration Present. Try Generating one.")


        self.api_settings = APISettings(config)
        if not self.api_settings.CLIENT_ID:
            raise Exception("Missing Client Id")
        if not self.api_settings.NETSUITE_APP_NAME:
            raise Exception("Missing Netsuite App Name")
        if not self.api_settings.NETSUITE_KEY_FILE:
            raise Exception("Missing Netsuite Certificate path.")
        if not self.api_settings.CERT_ID:
            raise Exception("Missing Netsuite Certificate ID.")

        self.app_name = self.api_settings.APP_NAME

        self.netsuite_app_name = self.api_settings.NETSUITE_APP_NAME
        self.netsuite_key_path = self.api_settings.NETSUITE_KEY_FILE
        self.netsuite_cert_id = self.api_settings.CERT_ID
        # self.field_map = None
        # if self.api_settings.NETSUITE_FIELD_MAP:
        #     self.field_map = self.api_settings.NETSUITE_FIELD_MAP

        self.storage = self.api_settings.STORAGE_CLASS()
        if isinstance(self.api_settings.STORAGE_CLASS(), JSONStorage):
            if not self.api_settings.JSON_STORAGE_PATH:
                raise Exception("JSON_STORAGE_PATH must be defined for JSONStorage")
            self.storage.storage_path = self.api_settings.JSON_STORAGE_PATH
        self.rest_url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest" \
                        f"/record/v1/ "
        self.access_token_url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token",


    @property
    def QUERY_CLIENT(self):
        if not self.query_client:
            self.query_client = self.QueryClient(self)
            # if self.token.access_token is not None:
                # self.get_customer_categories()
                # self.get_status_dict()
        return self.query_client


    @property
    def RESTLET_CLIENT(self):
        if not self.restlet_client:
            self.restlet_client = self.RestletClient(self)
        return self.restlet_client

    @property
    def token(self) -> NetsuiteToken:
        return self.storage.get_token(self.app_name)

    def save_token(self, token):
        self.storage.save_token(self.app_name, token)

    def get_jwt(self):
        private_key = ""
        with open(self.netsuite_key_path, "rb") as pemfile:
            private_key = pemfile.read()
        payload = {
            "iss": f"{self.api_settings.CLIENT_ID}",
            "scope": "restlets, rest_webservices",
            "aud": f"{self.access_token_url}",
            "exp": (datetime.now() + timedelta(seconds=3600)).timestamp(),
            "iat": datetime.now().timestamp()
        }

        headers = {
            "typ": "JWT",
            "alg": "RS256",
            "kid": f"{self.netsuite_cert_id}"
        }
        jwt_token = jwt.encode(payload=payload, key=private_key, algorithm='RS256', headers=headers)

        return jwt_token

    def request_access_token(self):
        json_web_token = self.get_jwt()
        data = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': f'{json_web_token}'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        response = requests.post(url, data=data, headers=headers)
        token = NetsuiteToken(**response.json())
        self.save_token(token)
        # if token.access_token is not None:
        #     self.get_customer_categories()
        #     self.get_status_dict()
        return self.token

    def get_netsuite_recordtypes(self):
        url = f"https://{self.netsuite_app_name}.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
        token = self.storage.get_token(self.app_name)
        headers = {
            'Authorization': f'Bearer {token.access_token}'
        }
        response = requests.get(url, headers=headers)
        records = []
        for item in response.json().get('items'):
            records.append(item.get("name"))
        return sorted(records)

    def generate_rest_client(self, record_types=None):

        print("\nGenerating Client....")

        # from urllib.request import urlopen
        # from tempfile import NamedTemporaryFile
        # from shutil import unpack_archive
        import zipfile, shutil
        from io import BytesIO
        token = self.storage.get_token(self.app_name)
        url = f"https://{self.netsuite_app_name}.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
        params = {
            'select': record_types
        }
        headers = {
            'Accept': 'application/swagger+json',
            'Authorization': f'Bearer {token.access_token}'
        }
        response = requests.get(url, headers=headers, params=params)
        # print(token.access_token)
        # print(response.json())
        data = {
            'options': {
                'packageName': 'netsuite_rest_client'
            },
            'generateSourceCodeOnly': 'True',
            'spec': response.json()
        }
        headers2 = {
            'Content-Type': 'application/json'
        }
        result = requests.post('https://api-latest-master.openapi-generator.tech/api/gen/clients/python',headers=headers2, json=data)

        # Defining the zip file URL
        url = result.json().get('link')

        # Split URL to get the file name
        filename = url.split('/')[-1]

        # Downloading the file by sending the request to the URL
        print('Downloading Generated Client....')
        req = requests.get(url)
        print('Client Downloaded.')

        # extracting the zip file contents
        print('Extracting....')
        file = zipfile.ZipFile(BytesIO(req.content))
        file.extractall(path=self.api_settings.NETSUITE_CLIENT_PATH)


        client_src = Path.joinpath(Path(self.api_settings.NETSUITE_CLIENT_PATH), f'python-client/netsuite_rest_client')
        class_src = Path.joinpath(Path(netsuite.settings.PACKAGE_DIR), f'netsuite_rest_client/rest_api_client.py')
        # docs_src = Path.joinpath(Path(self.api_settings.NETSUITE_CLIENT_PATH), f'python-client/docs')
        readme_src = Path.joinpath(Path(self.api_settings.NETSUITE_CLIENT_PATH), f'python-client/README.md')

        dst = Path(f'{self.api_settings.NETSUITE_CLIENT_PATH}')
        # docs_dst = Path.joinpath(Path(self.api_settings.NETSUITE_CLIENT_PATH), f'docs')
        print(f'Copying to: {dst}')
        shutil.copytree(client_src, dst, symlinks=True, ignore=None, ignore_dangling_symlinks=False,
                        dirs_exist_ok=True)
        # shutil.copytree(docs_src, docs_dst, symlinks=True, ignore=None, ignore_dangling_symlinks=False,
        #                 dirs_exist_ok=True)

        shutil.copy(class_src, dst)
        shutil.copy(readme_src, dst)


        shutil.rmtree(Path.joinpath(Path(self.api_settings.NETSUITE_CLIENT_PATH), 'python-client'))
        print('temp folder was removed.')

        print('\nNetsuite client was successfully generated and is ready to use!')
        print('***************************************************************')
        print('\nUSAGE')
        print('----------------------')
        print('from netsuite import Netsuite'
              '\nfrom netsuite_rest_client import apis, rest_api_client'
              '\nnetsuite = Netsuite()'
              '\nrest_client = rest_api_client.RestApiClient(netsuite)'
              '\ncustomer_api = apis.CustomerApi(rest_client)')

    def get_token(self):
        if not self.token.is_expired:
            return self.token
        else:
            return self.request_access_token()


    class QueryClient:
        def __init__(self, netsuite):
            self.netsuite = netsuite
            self.configuration = api_clients.Configuration()
            self.configuration.token = netsuite.storage.get_token(netsuite.app_name)
            self.configuration.token_refresh_hook = self.refresh_token
            self.configuration.app_name = netsuite.netsuite_app_name
            self.configuration.host = f"https://{self.configuration.app_name}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"
            self.query_api_client = api_clients.ApiClient(configuration=self.configuration)
            self.query_api = api_clients.QueryApi(api_client=self.query_api_client)

        def refresh_token(self):
            self.configuration.token = self.netsuite.get_token()
            return self.configuration.token

    class RestletClient:
        def __init__(self, netsuite):
            self.netsuite = netsuite
            self.configuration = api_clients.Configuration()
            self.configuration.token = netsuite.storage.get_token(netsuite.app_name)
            self.configuration.token_refresh_hook = self.refresh_token
            self.configuration.app_name = netsuite.netsuite_app_name
            self.configuration.host = f"https://{self.configuration.app_name}.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
            self.api_client = api_clients.ApiClient(configuration=self.configuration)
            self.restlet_api = api_clients.RestletApi(api_client=self.api_client)

            # self.contact_api = swagger_client.ContactApi(api_client=self.api_client)
            # self.customer_api = swagger_client.CustomerApi(api_client=self.api_client)
            # self.message_api = swagger_client.MessageApi(api_client=self.api_client)

        def refresh_token(self):
            self.configuration.token = self.netsuite.get_token()
            return self.configuration.token
