from django.urls import path
from find_it.views import index, ProductListView, ProductDetailView


urlpatterns = [
    path("", index, name = "index"),
    path("products_list/", ProductListView.as_view(), name= "list-product"),
    path('<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
]

app_name = "find_it"