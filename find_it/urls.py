from django.urls import path
from find_it.views import index, ProductListView, StoreManagementView, StoreUpdateView, StoreDeleteView, ProductDetailView, ProductUpdateView, ProductsManagementView, ProductDeleteView


urlpatterns = [
    path("", index, name = "index"),
    path("products_list/", ProductListView.as_view(), name= "list-product"),
    path('<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('products/manage/', ProductsManagementView.as_view(), name='products-management'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('stores/manage/', StoreManagementView.as_view(), name='store-management'),
    path('stores/<int:pk>/update/', StoreUpdateView.as_view(), name='store-update'),
    path('stores/<int:pk>/delete/', StoreDeleteView.as_view(), name='store-delete'),
]

app_name = "find_it"