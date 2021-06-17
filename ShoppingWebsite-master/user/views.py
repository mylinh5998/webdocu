import json
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from . import forms
from .models import MyUser
from products.models import *
from django.utils import timezone
from django.core.mail import send_mail
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Register(View):
    def get(self, request):
        return render(request, "user/register.html", {"form": forms.RegisterForm()})

    def post(self, request):
        form = forms.RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "user/register.html", {"form": form})
        form.save()
        return redirect("/")


class Login(View):
    def post(self, request):
        username = request.POST.get("username", False)
        password = request.POST.get("password", False)
        dataResponse = {
            "result": "OK",
        }
        # Check if have both username and password
        if (not username) or (not password):
            dataResponse["message"] = "Vui lòng điền đầy đủ các trường"
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        #  Check username and password is TRUE
        user = authenticate(request=request, username=username, password=password)
        if not user:
            dataResponse["message"] = "Tên đăng nhập hoặc mật khẩu không chính xác"
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        login(request=request, user=user)
        dataResponse["message"] = "OK"
        return HttpResponse(json.dumps(dataResponse), content_type="application/json")


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Profile(LoginRequiredMixin, View):
    login_url = "/"
    def get(self, request):
        return render(request, "user/profile.html")


class UpdateProfile(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        form = forms.UpdateProfileForm(data={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "sex": request.user.sex,
            "date_of_birth": request.user.date_of_birth,
            "address": request.user.address,
            "email": request.user.email,
            "phone": request.user.phone,
        })
        return render(request, "user/updateprofile.html", {"form": form})

    def post(self, request):
        form = forms.UpdateProfileForm(request.POST)
        dataResponse = {
            "result": "OK",
            "errors": [],
        }
        # Validate form
        if not form.is_valid():
            for field in form:
                for error in field.errors:
                    dataResponse["errors"].append(error)
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        # Check pasword confirm
        username = request.user.username
        password = form.cleaned_data["password_confirm"]
        user = authenticate(request=request, username=username, password=password)
        if not user:
            dataResponse["errors"].append("Mật khẩu xác nhận không chính xác")
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        # Check unique phone and email
        phone = form.cleaned_data["phone"]
        email = form.cleaned_data["email"]
        listResult = MyUser.objects.filter(phone=phone).exclude(username=username)
        if listResult:
            dataResponse["errors"].append("Số điện thoại đã có người sử dụng")
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        listResult = MyUser.objects.filter(email=email).exclude(username=username)
        if listResult:
            dataResponse["errors"].append("Địa chỉ mail đã có người dử dụng")
            return HttpResponse(json.dumps(dataResponse), content_type="application/json")
        # update profile
        currentUser = MyUser.objects.get(username=username)
        # check if new contact not same old info
        if currentUser.phone != phone:
            currentUser.is_active_phone = False
        if currentUser.email != email:
            currentUser.is_active_email = False
        currentUser.email = email
        currentUser.phone = phone

        currentUser.first_name = form.cleaned_data["first_name"]
        currentUser.last_name = form.cleaned_data["last_name"]
        currentUser.sex = form.cleaned_data["sex"]
        currentUser.date_of_birth = form.cleaned_data["date_of_birth"]
        currentUser.address = form.cleaned_data["address"]
        # if need change password
        newPassword = form.cleaned_data["password"]
        if newPassword:
            currentUser.set_password(newPassword)
        # save all change
        currentUser.save()
        # login again
        user = authenticate(request=request, username=username, password=newPassword)
        login(request=request, user=user)
        return HttpResponse(json.dumps(dataResponse), content_type="application/json")


class UpdateAvatar(LoginRequiredMixin, View):
    login_url = "/"

    def post(self, request):
        form = forms.AvatarForm(request.POST, request.FILES)
        dataResponse = {"result": ""}
        if form.is_valid():
            dataResponse["result"] = "OK"
            user = MyUser.objects.get(username=request.user.username)
            if user.avatar.url.split("/")[-1] != "no-img.png":
                os.remove(BASE_DIR + user.avatar.url)
            user.avatar = request.FILES['avatar']
            user.save()
        else:
            dataResponse["result"] = "NOT OK"
        return HttpResponse(json.dumps(dataResponse), content_type="application/json")


class VerifyEmail(LoginRequiredMixin, View):
    login_url = "/"
    def get(self, request, id):
        user = MyUser.objects.get(id=request.user.id)
        # check sended
        if not user.string_verify_email:
            return redirect("/")
        # check is activate
        if user.is_active_email:
            return redirect("/")
        if (timezone.now() - user.make_verify_email_at).seconds > 300:
            return render(request, "user/verifyEmail.html", {"content": "Liên kết đã hết hạn hoặc không đúng"})
        if id != user.string_verify_email:
            return render(request, "user/verifyEmail.html", {"content": "Liên kết đã hết hạn hoặc không đúng"})
        user.is_active_email = True
        user.save()
        return render(request, "user/verifyEmail.html", {"content": "Xác thực email thành công"})


class SendVerifyEmail(LoginRequiredMixin, View):
    login_url = "/"
    def get(self, request):
        user = MyUser.objects.get(id=request.user.id)
        if user.is_active_email:
            return redirect("/")
        if not user.email:
            return redirect("/")
        if (timezone.now() - user.make_verify_email_at).seconds <= 60 and user.string_verify_email != "":
            context = {
                "content": "Bạn vừa yêu cầu gửi email lúc này"
                           " Vui lòng chỉ yêu cầu sau 1 phút nếu không nhận được email",
            }
            return render(request, "user/verifyEmail.html", context)
        # make random string
        abc = "1234567890qwertyuiopasdfghjklzxcvbnm"
        string = "".join(random.choices(population=abc, k=30))
        # send email
        link = "http://127.0.0.1:8000/user/verifyemail/" + string
        contentEmail = '''
            Bạn vừa yêu cầu xác thực địa chỉ email này cho tài khoản ''' + user.username + '''
             Nếu là bạn, vui lòng click vào link sau để xác minh email.''' + link
        send_mail(
            'Email xác nhận',
            contentEmail,
            'huytuong010101@gmail.com',
            [user.email],
            fail_silently=False,
        )
        # save string
        user.string_verify_email = string
        user.make_verify_email_at = timezone.now()
        user.save()
        context = {
            "content": "Một Email xác thực đã được gửi đến địa chỉ email của bạn."
                       " Vui lòng kiểm tra hộp thử đến để xác thực."
                       " Lưu ý rằng email xác thực chỉ có hiệu lực trong 5 phút",
        }
        return render(request, "user/verifyEmail.html", context)


class MyShop(LoginRequiredMixin, View):
    login_url = "user/login"

    def get(self, request):
        products = Products.objects.filter(created_by=request.user)
        return render(request, "my-shop/my-shop-home.html", {"products": products})




