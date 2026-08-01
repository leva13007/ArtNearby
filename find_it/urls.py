from django.urls import path
from find_it.views import index, ProductListView, ProductCreateView, StoreManagementView, StoreUpdateView, StoreDeleteView, ProductDetailView


urlpatterns = [
    path("", index, name = "index"),
    path("products_list/", ProductListView.as_view(), name= "list-product"),
    path('<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('stores/manage/', StoreManagementView.as_view(), name='store-management'),
    path('stores/<int:pk>/update/', StoreUpdateView.as_view(), name='store-update'),
    path('stores/<int:pk>/delete/', StoreDeleteView.as_view(), name='store-delete'),
]

app_name = "find_it"