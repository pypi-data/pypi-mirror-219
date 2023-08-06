from lotr_api.api_resource import ApiResource
from lotr_api.common import BASE_URL, LotrApiException
from lotr_api.resource_config import ResourceConfig
from lotr_api.resources import API_CLIENT_RESOURCES


class ApiClient:
    """Lord of the Rings API client."""

    def __init__(self, api_key=None, resources: list[ResourceConfig] = API_CLIENT_RESOURCES):
        """Class initializer.

        :param api_key: private API token
        :param resources: list of resource configurations
        """
        self.api_key = api_key
        self._headers = {}
        if api_key:
            self._headers['Authorization'] = f'Bearer {api_key}'

        self.resource_by_operation = {}
        self._parse_resources(resources or [])

    def _parse_resources(self, resources: list[ResourceConfig]):
        """Create a resource tree based on the configuration.

        :param resources: list of API resources
        :return: None
        """
        for resource in resources:
            for operation in resource.get_operations():
                self.resource_by_operation[operation] = resource

    def __getattr__(self, item: str):
        """Helper method to intercept calls to single and list-based resource calls."""
        if item in self.resource_by_operation:
            resource = self.resource_by_operation[item]
            sub_resources = resource.sub_resources if item.endswith('_get') else []
            return ApiResource(resource.endpoint, resource.schema, BASE_URL, self._headers, sub_resources)

        raise LotrApiException('Invalid method')
