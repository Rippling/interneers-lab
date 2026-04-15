from django.contrib import admin
from django.urls import path , include
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    path('product/',include('product.urls')) ,
    path('product-csr/',include('product_csr.urls'))
]
