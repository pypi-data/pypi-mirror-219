from netsuite_rest_client.api_client import ApiClient


class RestApiClient(ApiClient):

    def __init__(self, netsuite):
        super().__init__()
        self.configuration.host = f"https://{netsuite.netsuite_app_name}.suitetalk.api.netsuite.com/services/rest/record/v1"
        self.configuration.api_key['OAuth_1.0_authorization'] = netsuite.get_token().access_token
        self.configuration.api_key_prefix['OAuth_1.0_authorization'] = 'Bearer'
