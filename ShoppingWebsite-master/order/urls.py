from django.urls import path
from . import views

urlpatterns = [
    path('new-order/', views.NewOrder.as_view(), name="newOrder"),
    path('my-order/', views.ShowMyOrder.as_view(), name="myOrder"),
    path('delete/', views.DeleteOrder.as_view(), name="deleteOrder"),
    path('update/', views.UpdateOrder.as_view(), name="updateOrder"),
    path('handle-order/', views.HandleOrder.as_view(), name="handleOrder"),
    path('get-info/', views.GetAddInfo.as_view(), name="getInfo"),
    path('update-info/', views.UpdateAddInfo.as_view(), name="updateInfo"),
    path('selling/', views.ShowMySelling.as_view(), name="ShowMySelling"),
    path('accept/', views.AcceptOrder.as_view(), name="AcceptOrder"),
    path('received/', views.MarkReceived.as_view(), name="MarkReceived"),
]