from django.urls import path
from .views import *

urlpatterns = [
    path("add-new/", AddNewProduct.as_view(), name="addNewProduct"),
    path("<int:id>/update", UpdateProduct.as_view(), name="updateProduct"),
    path("<int:id>/delete", DeleteProduct.as_view(), name="deleteProduct"),
]