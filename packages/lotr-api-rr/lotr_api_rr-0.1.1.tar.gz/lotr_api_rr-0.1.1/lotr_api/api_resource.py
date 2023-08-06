import json

import requests

from lotr_api.common import LotrApiInvalidMethodException, LotrApiResourceNotExistsException, DEFAULT_LIMIT, DEFAULT_OFFSET, \
    FilterType
from lotr_api.resource_config import ResourceConfig
from lotr_api.schemas import SchemaType

# Mapping of filter type to an operation
FILTER_TYPE_TO_OP = {
    FilterType.MATCH: '=',
    FilterType.NEGATE_MATCH: '!=',
    FilterType.INCLUDE: '=',
    FilterType.EXCLUDE: '!='
}


class ApiResource:
    """Helper class to encompass REST API resources.

    It can have sub-resources and be used as a single resource or a list of resources.
    """

    def __init__(self, endpoint: str, schema: SchemaType, url: str, headers: dict[str, str],
                 resources: list[ResourceConfig] = None):
        """Initializer for the class.

        :param endpoint: resource endpoint name
        :param schema: resource schema
        :param url: resource's URL relative ot other (parent) resources
        :param headers: headers necessary to make an API call
        :param resources: a list of child resources configurations (optional)
        """
        self.id = None
        self.endpoint = endpoint
        self.schema = schema
        self.url = url
        self.headers = headers
        self.limit = DEFAULT_LIMIT
        self.offset = DEFAULT_OFFSET
        self.resource_by_operation = {}
        self.sort = None
        self.filter = None

        self._parse_resources(resources or [])
        self.response = None

    def __call__(self, resource_id: str = None, limit: int = DEFAULT_LIMIT, offset: int = DEFAULT_OFFSET):
        """Helper method to intercept any parameters that could get passed to a given resource function.

        :param resource_id: use to select given resource by an ID
        :param limit: limits the number of requested resources
        :param offset: defines the start offset for where fetch the resources from
        :return:
        """
        if resource_id:
            self.id = resource_id
        else:
            self.limit = limit
            self.offset = offset
        return self

    def _parse_resources(self, resources: list[ResourceConfig]):
        """Create a resource tree based on the configuration.

        :param resources: list of API resources
        :return: None
        """
        for resource in resources:
            for operation in resource.get_operations():
                self.resource_by_operation[operation] = resource

    def _base_url(self):
        """Helper method to create base URL for a given resource."""
        url = f'{self.url}/{self.endpoint}'
        if self.id:
            url = f'{url}/{self.id}'
        else:
            if self.filter:
                # NOTE: this is a corner being cut - it should be done outside of this method
                url = f'{url}?{self.filter}'
        return url

    def _get(self):
        """Helper method to encapsulate GET call."""
        if not self.response:
            params = {}
            if not self.id:
                params = {'offset': self.offset, 'limit': self.limit}
                if self.sort:
                    params['sort'] = self.sort

            raw_response = requests.get(self._base_url(), headers=self.headers, params=params)
            self.response = json.loads(raw_response.content)

    def _get_response_items(self) -> list[object]:
        """Parses returned data items through a resource scheme."""
        return [self.schema(**d) for d in self.response.get('docs', [])]

    @property
    def item(self) -> object:
        """Get a single resource object parsed through the resource schema.

        :return: resource object
        """
        self._get()
        items = self._get_response_items()
        if len(items):
            return items[0]
        else:
            return None

    @property
    def items(self) -> list[object]:
        """Get a list of resource objects parsed through the resource schema.

        :return: list of resource objects
        """
        if self.id:
            raise LotrApiInvalidMethodException('Method not available for single resource')
        self._get()
        return self._get_response_items()

    @property
    def total(self) -> int:
        """Get a number of resources. If present this will be a number of items matching given filter parameters.

        :return: number of resources
        """
        if self.id:
            raise LotrApiInvalidMethodException('Method not available for single resource')
        self._get()
        return self.response['total']

    def sort_by(self, field: str, sort_dir: str):
        """Method used to add sorting to the API call.

        :param field: field name
        :param sort_dir: sort direction
        :return: ApiResource
        """
        if field is None or sort_dir is None:
            raise ValueError('Invalid sort_by arguments')
        self.sort = f'{field}:{sort_dir}'
        return self

    def filter_with(self, filter_field: str, filter_type: FilterType, values: list[str]) -> object:
        """Method used to add filter parameters to the API call.

        :param filter_field: field to filter for filtering
        :param filter_type: type of the filter
        :param values: list of strings
        :return: ApiResource
        """
        if filter_type in [FilterType.MATCH, FilterType.NEGATE_MATCH, FilterType.INCLUDE, FilterType.EXCLUDE]:
            self.filter = f'{filter_field}{FILTER_TYPE_TO_OP[filter_type]}{",".join(values)}'
        else:
            raise ValueError('Filter not implemented yet')

        return self

    def __getattr__(self, resource_name: str):
        """Helper method to intercept calls to resource methods."""
        if resource_name in self.resource_by_operation:
            if not self.id:
                raise LotrApiInvalidMethodException('Unable to access sub-resource for a list of resources')
            resource = self.resource_by_operation[resource_name]
            sub_resources = resource.sub_resources if resource_name.endswith('_get') else []
            return ApiResource(resource.endpoint, resource.schema, self._base_url(), self.headers, sub_resources)

        if resource_name.endswith('_get') or resource_name.endswith('_list'):
            raise LotrApiResourceNotExistsException(f'Resource {resource_name} does not exist')
