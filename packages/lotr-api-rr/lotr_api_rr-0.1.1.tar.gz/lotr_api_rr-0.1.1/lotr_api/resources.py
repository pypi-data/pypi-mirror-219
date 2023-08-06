from lotr_api.resource_config import ResourceConfig, OperationType
from lotr_api.schemas import Movie, Quote


API_CLIENT_RESOURCES = [
    ResourceConfig(
        'movies', 'movie', Movie, [OperationType.GET_ONE, OperationType.GET_MANY],
        [ResourceConfig('quotes', 'quote', Quote, [OperationType.GET_MANY], [])]
    ),
    ResourceConfig('quotes', 'quote', Quote, [OperationType.GET_ONE, OperationType.GET_MANY], [])
]
