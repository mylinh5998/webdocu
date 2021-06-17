from django.urls import path
from . import views
urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("profile/", views.Profile.as_view(), name="profile"),
    path("profile/edit/", views.UpdateProfile.as_view(), name="edit"),
    path("profile/updateavatar/", views.UpdateAvatar.as_view(), name="update_avatar"),
    path("verifyemail/<str:id>", views.VerifyEmail.as_view(), name="verify_email"),
    path("sendemail/", views.SendVerifyEmail.as_view(), name="send_email"),
    path("profile/shop/", views.MyShop.as_view(), name="my shop"),
]