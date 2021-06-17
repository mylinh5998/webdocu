from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from products.models import Products
from user.models import MyUser
from order.models import Order
# Create your views here.


class NewOrder(LoginRequiredMixin, View):
    login_url = "/user/login"

    def post(self, request):
        product = Products.objects.get(id=request.POST.get("id"))
        if len(Order.objects.filter(product=product, user=request.user)) != 0:
            context = {
            "result": "Not OK",
            "message": "Bạn đã đặt mặt hàng này rồi!"
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        number = request.POST.get("number", 1)
        if not number:
            number = 1
        if int(number) > product.num_available or int(number) <= 0:
            context = {
            "result": "Not OK",
            "message": "Dử liệu không hợp lệ!"
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        order = Order.objects.create(user=request.user, product=product, number=number)
        order.save()
        return HttpResponse(json.dumps({"result": "OK"}), content_type="application/json")


class ShowMyOrder(LoginRequiredMixin, View):
    login_url = "/user/login"

    def get(self, request):
        order = Order.objects.filter(user=request.user)
        return render(request, "user/my-order.html", {"order": order})


class DeleteOrder(LoginRequiredMixin, View):
    def post(self, request):
        orders = request.POST.getlist("orders[]")
        for item in orders:
            order = get_object_or_404(Order, id=item)
            if order.mode != 2 and order.user == request.user:
                order.delete()
            else:
                return HttpResponse(json.dumps({
                    "result": "Not OK",
                    "error": "Bạn không thể xóa sản phẩm đã được chấp nhận."
                }), content_type="json/application")

        return HttpResponse(json.dumps({
            "result": "OK",
        }), content_type="json/application")


class UpdateOrder(LoginRequiredMixin, View):
    def post(self, request):
        data = list(request.POST.dict().items())
        for item in data:
            if item[0] == "csrfmiddlewaretoken": continue
            order = get_object_or_404(Order, id=item[0])
            if order.user == request.user and order.mode < 2 and int(item[1]) <= order.product.num_available:
                order.number = int(item[1])
                order.save()
        return HttpResponse(json.dumps({
            "result": "OK",
        }), content_type="json/application")


class HandleOrder(LoginRequiredMixin, View):
    def post(self, request):
        orders = request.POST.getlist("orders[]")
        for item in orders:
            order = get_object_or_404(Order, id=item)
            if order.mode < 2 and order.user == request.user:
                order.mode = 1
                order.save()
            else:
                return HttpResponse(json.dumps({
                    "result": "Not OK",
                    "error": "Bạn không thể đặt sản phẩm đã được chấp nhận."
                }), content_type="json/application")

        return HttpResponse(json.dumps({
            "result": "OK",
        }), content_type="json/application")


class GetAddInfo(LoginRequiredMixin, View):
    def get(self, request):
        order = get_object_or_404(Order, id=request.GET["id"])
        return HttpResponse(json.dumps({
            "result": "OK",
            "content": order.add_info,
        }), content_type="json/application")


class UpdateAddInfo(LoginRequiredMixin, View):
    def post(self, request):
        order = get_object_or_404(Order, id=request.POST["id"])
        if order.user != request.user or order.mode != 0:
            return HttpResponse(json.dumps({
                "result": "not OK"
            }), content_type="json/application")
        order.add_info = request.POST["content"]
        order.save()
        return HttpResponse(json.dumps({
            "result": "OK"
        }), content_type="json/application")


class ShowMySelling(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(product__created_by=request.user).exclude(mode=0)
        return render(request, "user/selling.html", {"orders": orders})


class AcceptOrder(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get("id")
        order = get_object_or_404(Order, id=id)
        if order.product.created_by != request.user:
            return HttpResponse(json.dumps({
                "result": "Not OK",
                "error": "Lỗi xác thực",
            }), content_type="application/json")
        if order.mode == 1:
            order.mode = 2
        order.save()
        return HttpResponse(json.dumps({
            "result": "OK",
        }), content_type="application/json")


class MarkReceived(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get("id")
        order = get_object_or_404(Order, id=id)
        if order.user != request.user or order.mode != 2:
            return HttpResponse(json.dumps({
                "result": "Not OK",
                "error": "",
            }), content_type="application/json")
        order.mode = 3
        order.save()
        return HttpResponse(json.dumps({
            "result": "OK",
        }), content_type="application/json")