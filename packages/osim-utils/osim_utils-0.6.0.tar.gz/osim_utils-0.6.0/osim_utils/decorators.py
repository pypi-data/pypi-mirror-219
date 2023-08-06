import functools
import json

import osim_utils.exceptions as exc


def check_response(*args):
    """
    Checks that a call to an API client method returned an expected status code.
    Raises an AssertionError if the returned status code is unexpected.

    Args:
        *args (tuple): status codes that should NOT lead to an
            exception

    Returns:
        The response of the decorated method
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*inner_args, **kwargs):
            response = func(*inner_args, **kwargs)
            assert response.status_code in args, (
                f"API call initiated by {func.__module__}.{func.__name__} "
                f"returned error: {response.content}"
            )
            return response

        return wrapper

    return decorator


def process_response(func):
    """
    Processes the response of a call to an API client method
    so that only the body of the response is decoded form json and returned

    Returns:
        The json-decoded body of the response of the decorated method
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            return response.json()
        except json.JSONDecodeError:
            raise exc.ApiClientError(
                f"API call initiated by {func.__module__}.{func.__name__} "
                f"failed with error: {response.text}"
            )

    return wrapper
