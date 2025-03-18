from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .views import ProductListCreateView,ProductDetailView
def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server. THis has been edited")


from django.contrib import admin
from django.urls import path
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
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),

]
