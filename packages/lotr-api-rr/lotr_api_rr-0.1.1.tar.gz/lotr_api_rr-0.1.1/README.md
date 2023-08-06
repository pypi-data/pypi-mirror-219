# Lord of the Rings SDK

## Installation

For development, make sure to create a virtual environment. Then run. 

```
pip install -r requirements
```

To include in your project simply install it from pip.

```
pip install lotr-rr
```

## Usage

Make sure to obtain your API key first. In order to do so, follow the instructions on https://the-one-api.dev.

Initializing the API client

```

api_client = ApiClient(api_key=os.environ['LOTR_API_KEY'])
```

### Available endpoints

Getting a list of movies
```
GET /movie
```
```
movies = api_client.movies_list().items
```

Getting a single movie
```
GET /movie/{id}
```
```
movie = api_client.movies_get('5cd95395de30eff6ebccde5d').item
```

Getting a quote from a specific movie
```
GET  /movie/{id}/quote
```
```
movie_quotes = api_client.movies_get('5cd95395de30eff6ebccde5d').quotes_list().items
```

Getting a list of quotes
```
GET  /quote
```
```
quotes = api_client.quotes_list().items
```

Getting an individual of quote
```
GET  /quote/{id}
```
```
quote = api_client.quotes_get('5cd96e05de30eff6ebcce7e9').item
```

### In addition, you can paginate, sort and filter the `_list` endpoints

#### Pagination

Use `limit` and `offset` arguments.

```
first_movie = api_client.movies_list(limit=1, offset=0)
```

#### Sorting

Use `sort_by` method that has `sort_field` and `sort_direction` arguments. Default offset is 0 and default pagination is 10.

```
movies = api_client.movies_list().sort_by('name', 'asc')
```

#### Filtering

Filtering is implemented according to the spec in https://the-one-api.dev/documentation. There's a helper `filter_with` method that accepts field name, filter operation type and filter values.
At present only the following filters are implemented: match, negate match, include, exclude.


