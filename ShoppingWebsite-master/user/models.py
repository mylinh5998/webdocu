from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):

    sex_choice = ((0, "Không xác định"), (-1, "Nữ"), (1, "Nam"))

    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=15, default="", null=True, blank=True)
    sex = models.IntegerField(choices=sex_choice, default=0)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=500, default="", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", default="avatar/no-img.png")
    is_active_email = models.BooleanField(default=False)
    string_verify_email = models.CharField(default="", null=True, max_length=100)
    make_verify_email_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active_phone = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()