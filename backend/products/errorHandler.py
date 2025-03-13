from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound
from rest_framework import status

class ProductNotFound(NotFound):
    default_detail = {"error": "Product not found"}
    default_code = "not_found"

def handle_exception(exception):
    if isinstance(exception, ProductNotFound):
        return Response(exception.default_detail, status=status.HTTP_404_NOT_FOUND)
    
    if isinstance(exception, APIException):
        return Response({"error": str(exception)}, status=exception.status_code)

    return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
