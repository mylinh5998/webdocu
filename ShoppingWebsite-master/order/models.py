from django.db import models
from user.models import MyUser
from products.models import Products
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(MyUser, related_name="haveOrder", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name="inOrder", on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.IntegerField(default=0, choices=(
        (0, "Chưa đặt"),
        (1, "Đã đặt"),
        (2, "Đã chấp nhận"),
        (3, "Đã nhận hàng"),
    ))
    add_info = models.TextField(null=True, default="")

    def __str__(self):
        return str(self.number) + " " + self.product.__str__() + "is ordered by " + self.user.__str__()


class TalkAboutOrder(models.Model):
    user = models.ForeignKey(MyUser, related_name="takeAboutOrder", on_delete=models.CASCADE)
    content = models.TextField()
    order = models.ForeignKey(Order, related_name="haveTalk", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

