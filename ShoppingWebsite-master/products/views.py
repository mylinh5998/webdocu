from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *


# Create your views here.
class AddNewProduct(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        category = Category.objects.all()
        context = {
            "category": category,
        }
        return render(request, "products/addNewProduct.html", context)

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            # create new product
            newProduct = Products.objects.create(
                name_product=request.POST["name"],
                describe=request.POST["describe"],
                content=request.POST["content"],
                price=request.POST["price"],
                discount=request.POST["discount"],
                num_available=request.POST["available"],
                created_by=request.user,
            )
            # add main picture
            if request.FILES.get("mainPicture"):
                newProduct.main_picture = request.FILES.get("mainPicture")
            # add category
            for category in request.POST.getlist("category"):
                newProduct.category.add(Category.objects.get(pk=category))
            # upload picture

            for picture in request.FILES.getlist("pictures"):
                ProductPictures.objects.create(image_product=picture, product=newProduct).save()
            # let's save...
            newProduct.save()
        return redirect("/user/profile/shop/")


class UpdateProduct(View):
    def get(self, request, id):
        product = get_object_or_404(Products, pk=id)
        # not allow product of other
        if product.created_by != request.user:
            return HttpResponseNotFound("Wrong!")
        category = Category.objects.all()
        categorySelected = product.category.all()
        categorySelected = [item.id for item in categorySelected]
        return render(request, "products/updateProduct.html", {
            "category": category,
            "product": product,
            "categorySelected": categorySelected,
        })

    def post(self, request, id):
        product = get_object_or_404(Products, pk=id)
        if product.created_by != request.user:
            return HttpResponseNotFound("Wrong!")
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            # update info
            product.name_product = request.POST["name"]
            product.describe = request.POST["describe"]
            product.content = request.POST["content"]
            product.price = request.POST["price"]
            product.discount = request.POST["discount"]
            product.num_available = request.POST["available"]
            # add category
            product.category.clear()
            for category in request.POST.getlist("category"):
                product.category.add(Category.objects.get(pk=category))
            product.save()

        else:
            return HttpResponseNotFound("Wrong!")
        return redirect("/user/profile/shop/")


class DeleteProduct(LoginRequiredMixin, View):
    login_url = "/"

    def post(self, request, id):
        product = get_object_or_404(Products, pk=id)
        if product.created_by != request.user:
            return HttpResponseNotFound("Wrong!")
        product.delete()
        return redirect("/user/profile/shop/")

