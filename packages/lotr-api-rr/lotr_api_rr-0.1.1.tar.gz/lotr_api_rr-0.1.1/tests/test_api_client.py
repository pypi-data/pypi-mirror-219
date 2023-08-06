from vcr.unittest import VCRTestCase
import os

from lotr_api.api_client import ApiClient
from lotr_api.common import LotrApiResourceNotExistsException, FilterType
from lotr_api.resource_config import ResourceConfig, OperationType
from lotr_api.schemas import Movie, Quote


class TestApiClient(VCRTestCase):
    api_key = os.environ['LOTR_API_KEY']
    only_top_level_resources = [
        ResourceConfig('movies', 'movie', Movie, [OperationType.GET_ONE, OperationType.GET_MANY], []),
        ResourceConfig('quotes', 'quote', Quote, [OperationType.GET_ONE, OperationType.GET_MANY], [])
    ]

    nested_resources = [
        ResourceConfig(
            'movies', 'movie', Movie, [OperationType.GET_ONE, OperationType.GET_MANY],
            [ResourceConfig('quotes', 'quote', Quote, [OperationType.GET_MANY], [])]
        ),
        ResourceConfig('quotes', 'quote', Quote, [OperationType.GET_ONE, OperationType.GET_MANY], [])
    ]

    def test_basic_resource_operations(self):
        api_client = ApiClient(None, self.only_top_level_resources)

        self.assertEqual(
            ['movies_get', 'movies_list', 'quotes_get', 'quotes_list'], list(api_client.resource_by_operation.keys()),
        )

    def test_sub_resource_operations(self):
        api_client = ApiClient(None, self.nested_resources)

        movie = api_client.movies_get(1)

        self.assertEqual(['quotes_list'], list(movie.resource_by_operation.keys()))

    def test_url_top_level(self):
        api_client = ApiClient(None, self.only_top_level_resources)

        movie = api_client.movies_get(1)

        self.assertEqual('https://the-one-api.dev/v2/movie/1', movie._base_url())

    def test_url_nested(self):
        api_client = ApiClient(None, self.nested_resources)

        movie = api_client.movies_get(1).quotes_list()

        self.assertEqual('https://the-one-api.dev/v2/movie/1/quote', movie._base_url())

    def test_get_movie(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movie = api_client.movies_get('5cd95395de30eff6ebccde56')

        self.assertEqual(30, movie.item.academyAwardNominations)

    def test_get_non_existing_movie(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movie = api_client.movies_get('non-existing')

        self.assertEqual(None, movie.item)

    def test_get_movies(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movies = api_client.movies_list()

        self.assertEqual(8, len(movies.items))
        self.assertEqual(8, movies.total)

    def test_get_quotes(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        quotes = api_client.quotes_list()

        self.assertEqual(10, len(quotes.items))
        self.assertEqual(2384, quotes.total)

    def test_get_movie_quotes(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        quotes = api_client.movies_get('5cd95395de30eff6ebccde5d').quotes_list()

        self.assertEqual(10, len(quotes.items))

    def test_invalid_sub_resource(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        with self.assertRaises(LotrApiResourceNotExistsException):
            _ = api_client.movies_get('5cd95395de30eff6ebccde5d').elements_list()

    def test_movie_pagination(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        first_movie = api_client.movies_list(limit=1, offset=0)
        second_movie = api_client.movies_list(limit=1, offset=1)

        self.assertNotEqual(first_movie.item.name, second_movie.item.name)

    def test_movie_pagination_over_offset(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movie = api_client.movies_list(offset=100)

        self.assertEqual(None, movie.item)

    def test_movie_sorting(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movies = api_client.movies_list(limit=2).sort_by('name', 'asc')
        self.assertEqual(['The Battle of the Five Armies', 'The Desolation of Smaug'], [i.name for i in movies.items])

        movies = api_client.movies_list(limit=2).sort_by('name', 'desc')
        self.assertEqual(['The Unexpected Journey', 'The Two Towers'], [i.name for i in movies.items])

    def test_movie_filtering(self):
        api_client = ApiClient(api_key=self.api_key, resources=self.nested_resources)

        movies = api_client.movies_list().filter_with('name', FilterType.MATCH, ['The Battle of the Five Armies'])

        self.assertEqual(1, len(movies.items))
        self.assertEqual('The Battle of the Five Armies', movies.items[0].name)

        movies = api_client.movies_list().filter_with('name', FilterType.MATCH, ['The Battle'])
        self.assertEqual(0, len(movies.items))

        movies = api_client.movies_list().filter_with('name', FilterType.NEGATE_MATCH, ['The Battle'])
        self.assertEqual(8, len(movies.items))

        movies = api_client.movies_list().filter_with('name', FilterType.EXCLUDE, ['The Battle of the Five Armies'])
        self.assertEqual(7, len(movies.items))


