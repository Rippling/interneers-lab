from rest_framework.response import Response
def success_response(data_name,data, status_code):
    return Response(
        {
            "success": True,
            data_name : data
        },
        status=status_code,
    )

def error_response(message, status_code):
    return Response(
        {
            "success": False,
            "error": message
        },
        status=status_code,
    )
def invalid_method_response():
    return Response(
        {
            "success": False,
            "error": "Invalid request method"
        },
        status=400,
    )