"""
Contains all logic for error message generation and error handling
"""

from datetime import datetime
from django.http import JsonResponse, HttpRequest

ERROR_CODES={
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_FOUND"
}

ERROR_MESSAGES={
    400: "The server cannot process this request",
    401: "Need Authorization to process this request",
    403: "The request is forbidden",
    404: "The requested resource was not found",
    405: "The resource does not support this method"
}

def generate_error_response(request: HttpRequest, code: int, details: str, suggestion: str) \
    -> JsonResponse:
    """
    Creates a JsonResponse object for a error message.

    This is used whenever an error message is to be returned to the client as response.
    It is advisable to use this method, to maintain consistency in error responses. 
    The format of the error message is as follows:
    {
        "code": <string> The error code string, such as "NOT_FOUND",
        "message": <string> The meaning associated with the error code,
        "details": <string> Details of what the error is,
        "timestamp": <string> Timestamp generated when the error response was being generated,
        "request": <string> HTTP method and the target URI,
        "suggestion": <string> Suggestion to client to fix the error,
    }

    Args:
        request: The HttpRequest instance associated with the request that generated the error
        code: The error code (status code) as per HTTP standards
        details: As given in the format
        suggestion: As given in the format
    
    Returns:
        JsonResponse instance with the error message
    """
    response= JsonResponse({
        "code": ERROR_CODES[code],
        "message": ERROR_MESSAGES[code],
        "details": details,
        "timestamp": f"{datetime.now()} GMT+0:00",
        "request": f"{request.method} {request.path}",
        "suggestion": suggestion,
    })
    response.status_code= code

    return response
