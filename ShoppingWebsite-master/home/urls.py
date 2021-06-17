from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("detail/<str:slug>", views.DetailProduct.as_view(), name="detail"),
    path("search/", views.Search.as_view(), name="search"),
]