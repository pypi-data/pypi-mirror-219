API_VERSION = 'v2'
BASE_URL = f'https://the-one-api.dev/{API_VERSION}'
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0


# Filter type definition
class FilterType:
    MATCH = 0
    NEGATE_MATCH = 1
    INCLUDE = 2
    EXCLUDE = 3
    EXISTS = 4
    DOESNT_EXIST = 5
    REGEX = 6
    LT = 7
    LTE = 8
    GT = 9
    GTE = 10


class LotrApiException(Exception):
    """General exception type."""
    pass


class LotrApiInvalidMethodException(Exception):
    """Method not available for a given resource type."""
    pass


class LotrApiResourceNotExistsException(Exception):
    """Resource type doesn't exist."""
    pass
