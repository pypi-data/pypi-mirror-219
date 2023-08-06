"""
This library contains methods to check and help with http requests.

"""

import json
from rudderclient.request.exceptions import (
    ContentTypeNotSupported,
    MandatoryArgsNotFilled,
)


def check_content_type(request, available_content_type):
    """
    Check if the content_type of the request is the content_type available in the request.

    Parameters:
    ----------
        request: The request.
        available_content_type: The available content type for the request.

    Raise:
    -----
    An exception of type `ContentTypeNotSupported`
    """
    if request.headers.get("Content-Type") != available_content_type:
        raise ContentTypeNotSupported(
            "The request's body should be formatted as a JSON."
        )


def get_params(request, param):
    """
    Returns the value of a specific param in the request.

    Parameters:
    ----------
        request: The request.
        param: The name of the param in the request.

    Raise:
    -----
    An exception of type `MandatoryArgsNotFilled` if the param asked is not in the request.
    """
    data = json.loads(request.data)

    if param in data:
        return data.get(param)
    else:
        raise MandatoryArgsNotFilled("Unexpected body parameters.")
