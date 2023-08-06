"""
Response module for PyResponse package.
"""

import logging
from typing import Any


class Response:
    def __init__(self, data: Any, status: int):
        self.data = data
        self.status_code = status


def create_success_response(data=None, message=None, status_code=None, serializer=None, **kwargs):
    """
    Create a success response.

    This function generates a success response with the provided data, message,
    and status code. It supports optional serialization using the specified
    serializer, if provided.

    Args:
        data (Any): The data to be included in the response.
        message (str): The message associated with the response.
        status_code (int): The HTTP status code for the response.
        serializer (Serializer): The serializer instance to use for serialization.
        kwargs (dict): Additional keyword arguments for customization.

    Returns:
        Response: The success response.

    """
    response_data = {
        'success': True,
        'message': message,
        'data': data or []
    }
    response_data.update(kwargs)

    if serializer:
        serialized_data = serializer(response_data).data
    else:
        serialized_data = response_data

    logger = logging.getLogger(__name__)
    logger.info('Success Response: %s', response_data)

    return Response(serialized_data, status=status_code)


def create_error_response(message=None, data=None, status_code=None, serializer=None, **kwargs):
    """
    Create an error response.

    This function generates an error response with the provided message,
    data, and status code. It supports optional serialization using the
    specified serializer, if provided.

    Args:
        message (str): The error message.
        data (Any): Additional data related to the error.
        status_code (int): The HTTP status code for the error response.
        serializer (Serializer): The serializer instance to use for serialization.
        kwargs (dict): Additional keyword arguments for customization.

    Returns:
        Response: The error response.

    """
    response_data = {
        'success': False,
        'message': message,
        'data': data or []
    }
    response_data.update(kwargs)

    if serializer:
        serialized_data = serializer(response_data).data
    else:
        serialized_data = response_data

    logger = logging.getLogger(__name__)
    logger.error('Error Response: %s', response_data)

    return Response(serialized_data, status=status_code)
